# Adaptive Speech Emotion Recognition (SER) System

This repository contains the implementation of an **Adaptive Speech Emotion Recognition (SER) System** that dynamically learns from user feedback and optimizes its performance based on system resource availability.

## 🧩 System Architecture

![Adaptive SER Architecture](images/architecture.png)

The system comprises the following core components:

### 🧠 DL Model
A Convolutional Neural Network (CNN)-based model trained on speech features such as:
- Spectrograms
- Mel-Frequency Cepstral Coefficients (MFCCs)

This model performs real-time emotion classification from speech input.

### 📊 Feedback Manager
- Captures and stores user feedback on predictions.
- Maintains a feedback history database with corrected labels.
- Dynamically adjusts the **feedback threshold** and **learning rate** based on feedback trends.

### 🖥️ CPU Monitor
- Continuously monitors system CPU usage.
- Ensures efficient resource usage and prevents overloading.

### 🔄 Fine-Tuning Manager
- Automatically triggers retraining of the DL model during low CPU usage periods.
- Incorporates user feedback into the training data to enhance model accuracy over time.

---

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/adaptive-ser-system.git
   cd adaptive-ser-system
