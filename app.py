from flask import Flask, request, jsonify, render_template, send_file
import os
import json
import numpy as np
import librosa
import librosa.display
import sounddevice as sd
import wave
import time
import matplotlib.pyplot as plt
from backend import main
from backend.adaptive_learning import feed_back_manager
from backend.adaptive_learning.fine_tuning_manager import fine_tune
import scipy.io.wavfile as wav


app = Flask(__name__)

# Paths
JSON_PATH = '/home/badri/mine/ser/capstone_project/backend_lib/backend/data/feedback_interval.json'
AUDIO_PATH = '/home/badri/mine/ser/capstone_project/backend_lib/backend/data/user_audio/'

# Load threshold values
with open(JSON_PATH, 'r') as f:
    values = json.load(f)


# 📌 Serve Pages
@app.route('/')
def home():
    return render_template('index.html', threshold=values['threshold'])


@app.route('/feedback')
def feedback_page():
    return render_template('feedback.html')


@app.route('/fine-tune')
def fine_tune_page():
    return render_template('fine_tune.html')


@app.route('/about')
def about_page():
    return render_template('about.html')


# 📌 Predict Emotion (for upload & recorded audio)
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    file_path = os.path.join(AUDIO_PATH, file.filename)
    file.save(file_path)

    prediction, conf = main.prediction(file_path)
    values['predicted'] += 1

    with open(JSON_PATH, 'w') as f:
        json.dump(values, f, indent=4)

    return jsonify({'emotion': prediction, 'confidence': conf, 'file_path': file_path})





@app.route('/record', methods=['POST'])
def record():
    duration = 2.5  # seconds
    sample_rate = 22050  # Hz
    file_path = os.path.join(AUDIO_PATH, f'recorded_audio_{time.strftime("%H-%M-%S")}.wav')

    print(f"Recording audio for {duration} seconds...")

    # Record audio
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()

    # Save using scipy to ensure correct WAV format
    wav.write(file_path, sample_rate, audio_data)

    print(f"Audio recorded and saved to {file_path}")

    # Predict Emotion
    prediction, conf = main.prediction(file_path)
    values['predicted'] += 1

    with open(JSON_PATH, 'w') as f:
        json.dump(values, f, indent=4)

    return jsonify({'emotion': prediction, 'confidence': conf, 'file_path': file_path})

# @app.route('/waveform', methods=['GET'])
# def generate_waveform():
#     if not file_path or not os.path.exists(file_path):
#         return jsonify({'error': 'Invalid file path'}), 400
#
#     y, sr = librosa.load(file_path, sr=22050)
#     fig, ax = plt.subplots(figsize=(10, 3))
#     plt.figure(figsize=(10, 3))
#     librosa.display.waveshow(y, sr=sr,ax= ax ,alpha=0.7)
#     plt.title("Waveform")
#     plt.xlabel("Time (seconds)")
#     plt.ylabel("Amplitude")
#     plt.savefig("/home/badri/Pictures")
#     print('saved')
#     waveform_path = os.path.join(AUDIO_PATH, "waveform.png")
#     plt.savefig(waveform_path, bbox_inches='tight')
#     plt.close()
#
#     return send_file(waveform_path, mimetype='image/png')



@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.json
    file_path = data.get('file_path')
    correct_emotion = data.get('correct_emotion')

    if not file_path or not correct_emotion:
        return jsonify({'error': 'Invalid data'}), 400

    feed_back_manager.save_feedback(file_path, correct_emotion)
    return jsonify({'message': 'Feedback saved'})


@app.route('/fine-tune', methods=['POST'])
def fine_tune_model():
    fine_tune()
    return jsonify({'message': 'Model fine-tuned successfully'})


if __name__ == '__main__':
    app.run(debug=True)
