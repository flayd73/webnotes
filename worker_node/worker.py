# worker.py

from celery import Celery
import os
from scripts.transcribe import transcribe_audio
from scripts.summarize import summarize_with_syllabus
from scripts.generate_pdf import generate_pdf
from scripts.syllabus_index import build_syllabus_index
from scripts.subject_detection import detect_subject_and_topic, find_syllabus

from transformers import PegasusTokenizer, PegasusForConditionalGeneration
import torch
import whisper

# Configure the broker to point to the central server
# Replace 'central_server_ip' with the actual IP address of the central server
app = Celery('worker', broker='redis://central_server_ip:6379/0')

# Load models globally
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Whisper model
whisper_model = whisper.load_model("base")

# Pegasus model
pegasus_model_name = 'google/pegasus-xsum'
pegasus_tokenizer = PegasusTokenizer.from_pretrained(pegasus_model_name)
pegasus_model = PegasusForConditionalGeneration.from_pretrained(pegasus_model_name).to(device)

@app.task(bind=True, max_retries=3)
def process_audio_file(self, filename):
    try:
        # Paths to shared directories (mounted network shares)
        upload_dir = r'\\central_server_ip\uploads'     # Adjust this path
        processed_dir = r'\\central_server_ip\processed'  # Adjust this path

        # Construct file paths
        file_path = os.path.join(upload_dir, filename)
        processed_filename = os.path.splitext(filename)[0] + '.pdf'
        output_path = os.path.join(processed_dir, processed_filename)

        if not os.path.exists(file_path):
            return 'File does not exist'

        # Transcribe audio
        transcript = transcribe_audio(file_path, model=whisper_model)

        # Detect subject and topic
        subject, topic = detect_subject_and_topic(transcript)

        # Build syllabus index if applicable
        vectorizer, syllabus_index = None, None
        if subject:
            syllabus_path = find_syllabus(subject, 'resources')  # Adjust if resources are local
            if syllabus_path:
                vectorizer, syllabus_index, _ = build_syllabus_index(syllabus_path)

        # Summarize transcript
        summary = summarize_with_syllabus(
            transcript,
            vectorizer,
            syllabus_index,
            tokenizer=pegasus_tokenizer,
            model=pegasus_model
        )

        # Generate PDF
        generate_pdf(summary, output_path)

        return 'Success'

    except Exception as exc:
        # Retry the task if an exception occurs
        raise self.retry(exc=exc, countdown=60)
