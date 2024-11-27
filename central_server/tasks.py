# tasks.py

from celery import Celery
from celery.schedules import crontab
import os
from tasks_shared import process_audio_file

app = Celery('tasks', broker='redis://localhost:6379/0')

# Schedule the task to run daily at 5 PM
app.conf.beat_schedule = {
    'queue-tasks-everyday-at-5pm': {
        'task': 'tasks.queue_tasks',
        'schedule': crontab(hour=17, minute=0),
    },
}
app.conf.timezone = 'UTC'  # Set this to your local timezone

@app.task
def queue_tasks():
    upload_dir = 'uploads'
    for filename in os.listdir(upload_dir):
        if filename.endswith(('.mp3', '.wav', '.wma', '.aac', '.m4a', '.flac', '.ogg')):
            # Enqueue the task for workers to process
            process_audio_file.delay(filename)
