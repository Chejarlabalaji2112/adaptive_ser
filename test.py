# app.py - Main Flask App
from flask import Flask, render_template, request, redirect, url_for, jsonify
import numpy as np
import sounddevice as sd
import wave
import time
import json
import psutil
import matplotlib.pyplot as plt
import librosa.display
import os
import tempfile # we can just use the tempfile if we need it.
from backend import main
from backend.adaptive_learning import feed_back_manager
from backend.adaptive_learning.fine_tuning_manager import fine_tune

app = Flask(__name__)

# Load feedback values
json_path = '/home/badri/mine/ser/capstone_project/backend_lib/backend/data/feedback_interval.json'
audio_path = '/home/badri/mine/ser/capstone_project/backend_lib/backend/data/user_audio/'
with open(json_path, 'r') as f:
    values = json.load(f)

@app.route('/')
def home():
    cpu_usage = psutil.cpu_percent()
    mem_usage = psutil.virtual_memory().percent
    return render_template('home.html', threshold=values['threshold'], cpu=cpu_usage, memory=mem_usage)

@app.route('/record', methods=['POST'])
def record_audio():
    audio_data = sd.rec(int(2.5 * 22050), samplerate=22050, channels=1, dtype='float32')
    sd.wait()
    audio_data = (audio_data * 32767).astype(np.int16)
    current_audio = audio_path + 'recorded_audio' + time.strftime('%H-%Y-%S') + '.wav'
    with wave.open(current_audio, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(22050)
        wf.writeframes(audio_data.tobytes())
    prediction, conf = main.prediction(current_audio)
    values['predicted'] += 1
    with open(json_path, 'w') as f:
        json.dump(values, f, indent=4)
    return jsonify({'emotion': prediction, 'confidence': conf})

@app.route('/upload', methods=['POST'])
def upload_audio():
    file = request.files['file']
    file_path = os.path.join(audio_path, file.filename)
    file.save(file_path)
    prediction, conf = main.prediction(file_path)
    values['predicted'] += 1
    with open(json_path, 'w') as f:
        json.dump(values, f, indent=4)
    return jsonify({'emotion': prediction, 'confidence': conf})

@app.route('/visualize', methods=['POST'])
def visualize():
    file_path = request.form.get('file_path')
    y, sr = main.load_fixed_audio(file_path)
    fig, ax = plt.subplots(figsize=(10, 3))
    librosa.display.waveshow(y, sr=sr, ax=ax, alpha=0.7)
    ax.set_title('Waveform')
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Amplitude')
    image_path = os.path.join(audio_path, 'waveform.png')
    plt.savefig(image_path)
    plt.close()
    return jsonify({'image_path': image_path})

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        correct_emotion = request.form.get('correct_emotion')
        file_path = request.form.get('file_path')
        feed_back_manager.save_feedback(file_path, correct_emotion)
        return 'Feedback received!'
    return render_template('feedback.html')

@app.route('/fine_tune', methods=['POST'])
def fine_tune_model():
    fine_tune()
    return 'Fine-tuning started!'

if __name__ == '__main__':
    app.run(debug=True)
