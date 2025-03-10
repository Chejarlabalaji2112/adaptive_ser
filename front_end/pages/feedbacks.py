import streamlit as st
import psutil
from back_end.adaptive_learning import feed_back_manager
st.subheader("📢 Provide Feedback")
user_feedback = st.radio(f"Is the predicted emotion ['{st.session_state.prediction}'] correct?", ["Yes", "No"])
if user_feedback == "No":
    correct_emotion = st.radio("Select the correct emotion", ["neutral", "happy", "sad", "angry", "surprise", "fear", "disgust"])
    if st.button("submit"):
        feed_back_manager.save_feedback(st.session_state.path, correct_emotion)
        st.success(f"Thanks! We will use '{correct_emotion}' for model fine-tuning.")

# CPU Monitor
st.subheader("📊 System Performance")
cpu_usage = psutil.cpu_percent()
mem_usage = psutil.virtual_memory().percent
st.metric(label="CPU Usage", value=f"{cpu_usage}%")
st.metric(label="Memory Usage", value=f"{mem_usage}%")
