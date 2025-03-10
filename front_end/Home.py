#main app file
from back_end import main
import streamlit as st
import json

path = '/home/badri/mine/ser/gnd/capstone_project/Back_end/back_end/data/feedback_interval.json'
with open(path, 'r') as f:
    values = json.load(f)

if "predicted" not in st.session_state:
    st.session_state.predicted = values['predicted']
# -------------------- Streamlit App Layout -------------------- #
st.set_page_config(page_title="Speech Emotion Recognition", layout="wide")
print("title set")
st.title("🎙️ Speech Emotion Recognition System")
st.markdown(f"**Threshold:** {values['threshold']}")

st.subheader("🔼 Upload an Audio File")
uploaded_file = st.file_uploader("Choose a WAV file", type=["wav", "mp3"])

if uploaded_file:
    print("file_uploaded")
    st.audio(uploaded_file, format="audio/wav")
    prediction, conf = main.prediction(uploaded_file)
    st.session_state.predicted += 1
    values['predicted'] = st.session_state.predicted
    # Simulate Audio Processing

    # Display Prediction Result
    st.success(f"Predicted Emotion: **{prediction}** 😊")
    st.metric(label="Confidence Score", value=f"{conf:2f}%")
    st.markdown(f"**Predicted:** {st.session_state.predicted}")
