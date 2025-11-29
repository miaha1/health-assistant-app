# Coordinator Lambda Function to handle incoming S3 events and manual test events
import json
import logging
import urllib.parse
from utils import db 

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    
    try:
        # Check if this is an S3 Event (File Uploaded)
        if 'Records' in event:
            bucket_name = event['Records'][0]['s3']['bucket']['name']
            file_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
            
            logger.info(f"New input file detected: {file_key}")
            
            # get data from S3
            logger.info("Attempting to read database...")
            
            # Get Patients
            patients = db.get_all_patients()
            patient_count = len(patients)
            
            # Get Open Slots
            slots = db.get_available_slots()
            slot_count = len(slots)
            
            # Log the result
            msg = f"DB Connection Success! Found {patient_count} patients and {slot_count} open slots."
            logger.info(msg)
            
            return {
                'statusCode': 200,
                'body': json.dumps(msg)
            }
            
        else:
            # Fallback for manual testing button
            return {'statusCode': 200, 'body': json.dumps("Manual test complete.")}

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {'statusCode': 500, 'body': json.dumps("Error processing event")}