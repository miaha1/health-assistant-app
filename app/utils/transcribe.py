"""Utility functions for transcribing audio files using AWS Transcribe."""
""" Wait Loop Logic for AWS Transcribe Job Completion """
import boto3
import uuid
import time
import urllib.request
import json
import logging

transcribe = boto3.client('transcribe')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def transcribe_audio(bucket,key):
    """Submit an audio to Transribe and wait"""
    job_name = f"triage-job-{uuid.uuid4()}"
    file_url = f"s3://{bucket}/{key}"

    transcribe.start_transcription_job(
        TransciptionJobName=job_name,
        Media={'MediaFileUri': file_url},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )

    # Wait for the job to complete
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        job_status = status['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            break
        print("Waiting for job to complete...")
        time.sleep(2)
    
    if job_status == 'COMPLETED':
            transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
            # Download JSON result from AWS
            with urllib.request.urlopen(transcript_uri) as response:
                data = json.loads(response.read())
                return data['results']['transcripts'][0]['transcript']
            
    return None
