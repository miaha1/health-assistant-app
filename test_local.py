# File to test local functionalities
import json
import logging
import os
import sys
# This makes Python see 'utils' as if it were in the top folder
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
from app.llm_handler import lambda_handler

# Set up logging
logging.basicConfig(level=logging.INFO)

# Simulate S3 event (JSON structure)
fake_event = {
  "Records": [
    {
      "s3": {
        "bucket": {
          "name": "health-assistant-data" # <--- CHECK YOUR BUCKET NAME
        },
        "object": {
          "key": "inputs/test.txt"        # <--- Make sure this file exists in S3
        }
      }
    }
  ]
}

print("--- 🚀 Starting Local Test ---")
response = lambda_handler(fake_event, None)

# 3. Print the result
print("\n--- ✅ Result ---")
print(json.dumps(response, indent=2))

