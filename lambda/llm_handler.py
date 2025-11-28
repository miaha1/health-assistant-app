# import json
# import logging
# import time

# # Configure Logging
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

# def lambda_handler(event, context):
#     """
#     Standard AWS Lambda Handler.
#     """
    
#     # Log the incoming event
#     print(f"Received event: {json.dumps(event)}")

#     start_time = time.time()

#     try:
#         # If the user sent a message, we grab it. If not, use default.
#         user_input = event.get('message', 'No message provided')
        
#         # Simulate processing time
#         response_data = {
#             "echo": user_input,
#             "processed_at": start_time,
#             "status": "success"
#         }

#         # Log the result
#         print(f"Response generated: {json.dumps(response_data)}")

#         return {
#             'statusCode': 200,
#             'body': json.dumps(response_data)
#         }

#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return {
#             'statusCode': 500,
#             'body': json.dumps({"error": "Internal Server Error"})
#         }

# if __name__ == "__main__":
#     # Simulate an event that AWS would send
#     fake_event = {"message": "Hello from my laptop!"}
#     fake_context = None
    
#     # Run the function
#     print("--- Starting Local Test ---")
#     result = lambda_handler(fake_event, fake_context)
#     print("--- Test Result ---")
#     print(result)

import json
import logging
import urllib.parse
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    
    try:
        # 1. Check if this is an S3 Event
        if 'Records' in event:
            # Get the bucket name and file key (filename)
            bucket_name = event['Records'][0]['s3']['bucket']['name']
            file_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
            
            logger.info(f"New file detected! Bucket: {bucket_name}, Key: {file_key}")
            
            return {
                'statusCode': 200,
                'body': json.dumps(f"Successfully saw file: {file_key}")
            }
            
        else:
            # Fallback for manual testing (The "Echo" logic)
            msg = event.get('message', 'No message')
            return {'statusCode': 200, 'body': json.dumps(f"Echo: {msg}")}

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {'statusCode': 500, 'body': json.dumps("Error processing event")}