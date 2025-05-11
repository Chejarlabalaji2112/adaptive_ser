# Adaptive Speech Emotion Recognition (SER) System

## Table of Contents
1. [System Overview](#system-overview)
2. [System Architecture](#system-architecture)
3. [DL Model](#dl-model)
4. [Feedback Manager](#feedback-manager)
5. [CPU Monitor](#cpu-monitor)
6. [Fine-Tuning Manager](#fine-tuning-manager)

<a name="system-overview"></a>
## System Overview

This repository contains the implementation of an **Adaptive Speech Emotion Recognition (SER) System** that dynamically learns from user feedback and optimizes its performance based on system resource availability.

<a name="system-architecture"></a>
## 🧩 System Architecture

![Adaptive SER Architecture](./images/architecture.jpg)

The system comprises the following core components:

<a name="dl-model"></a>
### 🧠 DL Model
A Convolutional Neural Network (CNN)-based model trained on speech features such as:
- Spectrograms
- Mel-Frequency Cepstral Coefficients (MFCCs)

This model performs real-time emotion classification from speech input.

<a name="feedback-manager"></a>
### 📊 Feedback Manager
- Captures and stores user feedback on predictions.
- Maintains a feedback history database with corrected labels.
- Dynamically adjusts the **feedback threshold** and **learning rate** based on feedback trends.

<a name="cpu-monitor"></a>
### 🖥️ CPU Monitor
- Continuously monitors system CPU usage.
- Ensures efficient resource usage and prevents overloading.

<a name="fine-tuning-manager"></a>
### 🔄 Fine-Tuning Manager
- Automatically triggers retraining of the DL model during low CPU usage periods.
- Incorporates user feedback into the training data to enhance model accuracy over time.

---
