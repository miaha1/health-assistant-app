# File to test local functionalities
import json
import logging
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
from app.llm_handler import lambda_handler

# Set up logging
logging.basicConfig(level=logging.INFO)

# Simulate S3 event
fake_event = {
  "Records": [
    {
      "s3": {
        "bucket": {
          "name": "health-assistant-data" 
        },
        "object": {
          "key": "inputs/test.txt"        
        }
      }
    }
  ]
}

print(" Starting Local Test")
response = lambda_handler(fake_event, None)

print("\n Result ")
print(json.dumps(response, indent=2))

