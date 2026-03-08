# AI Voice Triage Assistant (Serverless)
A serverless, AI-powered patient triage system that processes patient symptoms (text/voice), analyzes severity using LLMs, and automatically books medical appointments based on urgency and availability.

Built with AWS Lambda (Docker), Amazon Bedrock (Claude 3 Haiku), and LangChain.

# Architecture
The system follows an Event-Driven Architecture:

Trigger: A patient transcript (or audio) is uploaded to an S3 Bucket (inputs/).

Orchestration: This triggers an AWS Lambda function packaged as a Docker Container.

Intelligence: Lambda invokes Amazon Bedrock (Claude 3 Haiku) via LangChain.

Intent Classification: Determines if the user wants to book, reschedule, or triage.

Entity Extraction: Extracts symptoms, duration, and severity using Pydantic validation.

State Management: The system reads/writes mock patient and schedule data stored in S3 JSON files (acting as a serverless NoSQL database).

Action: If a slot is suggested and valid, the system automatically updates the database to book the appointment.

# Tech Stack
Cloud: AWS (Lambda, S3, ECR, Bedrock, IAM)

AI/LLM: Anthropic Claude 3 Haiku (via Amazon Bedrock)

Frameworks: LangChain, Pydantic (for structured JSON output)

Infrastructure: Docker (Containerized Lambda), AWS SAM/CLI

Language: Python 3.12

# Project Structure
```text
health-triage-assistant/
├── lambda/
│   ├── llm_handler.py       # Main Logic: LangChain pipeline & Booking logic
│   └── utils/
│       ├── db.py            # S3 Wrapper: Reads/Writes JSON "database"
│       └── config.py        # Environment configuration
├── data/
│   ├── patients.json        # Mock patient database
│   └── appointment_slots.json # Mock calendar (Doctor availability)
├── generate_data.py         # Script to generate synthetic patient/slot data
├── Dockerfile               # AWS Lambda Docker definition (ARM64 optimized)
└── README.md
```
# Features
Structured AI Output: Uses LangChain OutputParsers to guarantee strict JSON responses (Severity Score 1-10, Symptoms List).

Smart Triage Logic: The AI analyzes medical history + current symptoms to decide urgency (e.g., "Chest pain + Diabetes" = Emergency).

Auto-Booking: Automatically locks the best available appointment slot in the database upon successful triage.

Cross-Platform Deployment: Solves the "Mac vs. Linux" dependency issue using Docker containers for AWS Lambda.

# Testing
Upload a text file to the inputs/ folder in S3 to simulate a patient request.

Input (test.txt):

"I have had a throbbing migraine for 3 days and I am feeling very dizzy."

Output (CloudWatch Logs):

JSON

{
  "intent": "symptom_triage",
  "symptoms": ["migraine", "dizziness"],
  "severity_score": 8,
  "reasoning": "Prolonged migraine with neurological symptoms.",
  "suggested_slot_id": "s-2045",
  "booking_confirmation": true
}
# Future Improvements
Voice Integration: Add Amazon Transcribe to handle raw .mp3 audio files.

Frontend: Build a simple React/Streamlit frontend for users to record voice.

Real Database: Migrate from S3 JSON files to DynamoDB for better concurrency.
