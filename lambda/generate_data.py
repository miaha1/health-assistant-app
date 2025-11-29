from faker import Faker
import json
import random
from datetime import datetime, timedelta 

fake = Faker()

# Configure
NUM_RECORDS = 50
DAYS = 7
SLOTS_PER_DAY = 24 # 10 in-person, 10 virtual


def generate_user_data():
    """
    Generate a list of fake user data records.
    Each record contains a name, email, and phone number.
    """
    user_data = []
    conditions = ["Diabetes", "Hypertension", "Asthma", 
                  "None", "Allergies", "Heart_Disease", "allergy_penicillin"]
    
    for _ in range(NUM_RECORDS):
        record = {
            "patient_id": fake.uuid4(),
            "name": fake.name(),
            "email": fake.email(),
            "dob": fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat(),
            # Randomly assign 0 to 2 conditions
            "condition": random.sample(conditions, k=random.randint(0, 2)),
            "phone_number": fake.phone_number()
        }
        user_data.append(record)
    return user_data

def generate_slots():
    """
    Generate appointment slots for a given number of days.
    """
    slots = []
    start_date = datetime.now()+ timedelta(days=1)  # Start from tomorrow
    for day in range(DAYS):
        current_day = start_date + timedelta(days=day)

        for slot in range(SLOTS_PER_DAY):
            # Slots from 9 AM onwards, 30 minutes each
            slot_time = current_day + timedelta(hours=9,minutes=slot * 30)
            is_virtual = slot >= SLOTS_PER_DAY // 2
            provider = "Dr. Pink(Virtual)" if is_virtual else "Dr. Blue(In-Person)"
            slot = {
                "slot_id": fake.uuid4(),
                "datetime": slot_time.isoformat(),
                "provider": provider,
                "type": "in-person" if slot < SLOTS_PER_DAY // 2 else "virtual",
                "is_booked": False
            }
            slots.append(slot)
        
    return slots
if __name__ == "__main__":
    # Generate user data
    user_data = generate_user_data()
    with open("data/patients.json", "w") as f:
        json.dump(user_data, f, indent=2)
    print(f"Generated {len(user_data)} user records in data/patients.json")

    # Generate appointment slots
    appointment_slots = generate_slots()
    with open("data/appointment_slots.json", "w") as f:
            json.dump(appointment_slots, f, indent=2)
    print(f"Generated {len(appointment_slots)} appointment slots in data/appointment_slots.json")