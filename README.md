# health-assistant-app
Healthcare Appointment &amp; Symptom Triage Voice Assistant
- Patients call or speak via mic.
- Assistant:
    - Takes **voice input** (symptoms, needs).
    - Uses **Transcribe** → text.
    - Uses **Comprehend / LLM** to extract symptoms & intent.
    - Suggests **appointment type + urgency** (e.g., telehealth vs in-person, PCP vs urgent care).
    - Books or proposes time slots using **mock appointment DB**.
- Everything logged to **CloudWatch**, experiments tracked with **SageMaker Experiments / W&B**.
- Has an **evaluation suite** for safety & correctness of triage
