import os

# Define S3 Bucket Name
# If not found, default to your specific bucket name
BUCKET_NAME = os.environ.get("BUCKET_NAME", "health-assistant-data")

# file paths in S3
PATIENTS_KEY = "data/patients.json"
SLOTS_KEY = "data/appointment_slots.json"