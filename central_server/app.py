# app.py

from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'
app.config['ALLOWED_EXTENSIONS'] = {'mp3', 'wav', 'wma', 'aac', 'm4a', 'flac', 'ogg'}

# Ensure necessary directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'audio_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['audio_file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Save the uploaded file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            flash('File uploaded successfully.')
            return render_template('index.html', filename=filename)
        else:
            flash('Invalid file type.')
            return redirect(request.url)
    return render_template('index.html')

@app.route('/status/<filename>')
def status(filename):
    processed_filename = os.path.splitext(filename)[0] + '.pdf'
    if os.path.exists(os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)):
        return jsonify({'status': 'Processed'})
    else:
        return jsonify({'status': 'Pending'})

@app.route('/download/<filename>')
def download(filename):
    processed_filename = os.path.splitext(filename)[0] + '.pdf'
    return send_from_directory(app.config['PROCESSED_FOLDER'], processed_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
