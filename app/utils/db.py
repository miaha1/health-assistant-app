import json
import boto3
from .config import BUCKET_NAME, PATIENTS_KEY, SLOTS_KEY

s3 = boto3.client('s3')

def load_json_from_s3(key):
    """Downloads a JSON file from S3 and returns it as a Python list/dict."""
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        content = response['Body'].read().decode('utf-8')
        return json.loads(content)
    except Exception as e:
        print(f"Error loading {key}: {e}")
        return []

def save_json_to_s3(key, data):
    """Uploads a Python list/dict to S3 as a JSON file."""
    try:
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=json.dumps(data, indent=2),
            ContentType='application/json'
        )
        return True
    except Exception as e:
        print(f"Error saving {key}: {e}")
        return False

# --- Public Functions (The "Interface") ---

def get_all_patients():
    return load_json_from_s3(PATIENTS_KEY)

def get_available_slots():
    """Returns only slots where is_booked is False."""
    all_slots = load_json_from_s3(SLOTS_KEY)
    return [s for s in all_slots if not s.get('is_booked')]

def book_slot(slot_id):
    """Finds a slot, marks it as booked, and saves the file back to S3."""
    all_slots = load_json_from_s3(SLOTS_KEY)
    
    found = False
    for slot in all_slots:
        if slot['slot_id'] == slot_id:
            if slot['is_booked']:
                return False  # Already booked
            slot['is_booked'] = True
            found = True
            break
            
    if found:
        # Commit the change to S3
        return save_json_to_s3(SLOTS_KEY, all_slots)
    return False