# scripts/transcribe.py

def transcribe_audio(file_path, model):
    # Use the provided model
    result = model.transcribe(file_path)
    transcript = result['text']
    return transcript
