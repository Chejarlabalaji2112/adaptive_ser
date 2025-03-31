from flask import Flask, request, jsonify, render_template
import os
import json
import numpy as np
import librosa.display
import sounddevice as sd
import wave
import time
from backend import main
from backend.adaptive_learning import feed_back_manager
from backend.adaptive_learning.fine_tuning_manager import fine_tune

app = Flask(__name__)

# Paths
JSON_PATH = '/home/badri/mine/ser/capstone_project/backend_lib/backend/data/feedback_interval.json'
AUDIO_PATH = '/home/badri/mine/ser/capstone_project/backend_lib/backend/data/user_audio/'

# Load threshold values
with open(JSON_PATH, 'r') as f:
    values = json.load(f)


@app.route('/')
def home():
    return render_template('index.html', threshold=values['threshold'])


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

    return jsonify({'emotion': prediction, 'confidence': conf, 'predicted_count': values['predicted']})


@app.route('/record', methods=['POST'])
def record():
    duration = 2.5
    sample_rate = 22050

    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()

    audio_data = (audio_data * 32767).astype(np.int16)
    file_path = AUDIO_PATH + 'recorded_audio' + time.strftime("%H-%Y-%S") + '.wav'

    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())

    prediction, conf = main.prediction(file_path)
    values['predicted'] += 1

    with open(JSON_PATH, 'w') as f:
        json.dump(values, f, indent=4)

    return jsonify({'emotion': prediction, 'confidence': conf, 'file_path': file_path})


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
