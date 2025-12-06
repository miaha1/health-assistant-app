# Coordinator Lambda Function to handle incoming S3 events and manual test events
# This file uses LangChain and Bedrock to analyze medical transcripts and suggest triage actions
import json
import random
import os
import boto3
import logging
import urllib.parse
from utils import db
from utils import transcribe, voice

# Langchain
# use ChatBedrock client to talk to Claude
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List, Optional

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

# Define the Data Structure
class TriageResponse(BaseModel):
    intent: str = Field(description="The user's intent: book_appointment, reschedule, symptom_triage")
    symptoms: List[str] = Field(description="List of physical symptoms extracted")
    duration: Optional[str] = Field(description="How long the symptoms have lasted")
    severity_score: int = Field(description="1-10 scale where 10 is emergency")
    reasoning: str = Field(description="Brief reason for the severity score")
    suggested_slot_id: Optional[str] = Field(description="The ID of the best appointment slot to book")

def get_file_content(bucket, key):
    response = s3.get_object(Bucket=bucket, Key=key)
    return response['Body'].read().decode('utf-8')

def analyze_with_langchain(patient, transcript, slots):
    # Setup the Brain (Claude 3 Haiku)
    llm = ChatBedrock(
        model_id="anthropic.claude-3-haiku-20240307-v1:0",
        client=boto3.client("bedrock-runtime", region_name="us-east-1"),
        model_kwargs={"max_tokens": 1000}
    )

    # Setup the Parser (Enforces JSON)
    parser = JsonOutputParser(pydantic_object=TriageResponse)

    # Create the Prompt
    system_template = """
    You are a medical triage assistant.
    Patient Name: {patient_name} 
    Patient History: {history}
    
    Available Appointment Slots: 
    {slots}
    
    Analyze the transcript below and provide a structured triage decision.
    If the severity is high (>7), suggest a slot with 'In-Person' type if available.
    
    {format_instructions}
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("user", "{transcript}")
    ])

    # The Chain (Prompt -> Brain -> Formatter)
    chain = prompt | llm | parser

    # Run
    result = chain.invoke({
        "patient_name": patient['name'],
        "history": ", ".join(patient['medical_history']),
        "slots": json.dumps(slots[:5]), # Only show first 5 slots to save tokens
        "transcript": transcript,
        "format_instructions": parser.get_format_instructions()
    })
    
    return result

def lambda_handler(event, context):
    try:
        if 'Records' not in event:
            return {'statusCode': 200, 'body': "Manual Test (No S3)"}

        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
        
        if key.endswith('.mp3'):
            # Voice file uploaded, transcribe it
            logger.info("Voice file detected. Starting transcription...")
            transcript_text = transcribe.transcribe_audio(bucket, key)
        else:
            logger.info("Text file detected. Reading content...")
            transcript_text = get_file_content(bucket, key)
        
        #logger.info(f"Input Text: {transcript_text}")

        # simulate context
        patient = random.choice(db.get_all_patients())
        slots = db.get_available_slots()

        # Run the Chain
        logger.info("Invoking LangChain...")
        response_data = analyze_with_langchain(patient, transcript_text, slots)
        logger.info(f"LangChain Result: {response_data}")

        # Auto booking logic
        #booking_status = "No booking suggested."
        try: 
            audio_response_key = voice.generate_audio_response(
                text=response_data['reasoning'], # Speak the reasoning
                bucket=bucket
            )
            response_data['audio_response_key'] = audio_response_key
        except Exception as e:
            logger.error(f"Failed to generate voice response: {e}")
            response_data['audio_response_key'] = None
            
        # Check if AI suggested a slot
        slot_id = response_data.get('suggested_slot_id')
        if slot_id:
            logger.info(f"AI suggested slot {slot_id}. Attempting to book...")
            success = db.book_slot(slot_id)
            response_data['booking_confirmed'] = success
        else:
            response_data['booking_confirmed'] = False
        return {
            'statusCode': 200,
            'body': json.dumps(response_data)
        }

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return {'statusCode': 500, 'body': str(e)}