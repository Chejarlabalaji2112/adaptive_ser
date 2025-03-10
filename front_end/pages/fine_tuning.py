import streamlit as st
import psutil
from back_end.adaptive_learning.fine_tuning_manager import fine_tune
st.subheader("Fine-Tuning")
fine_tune_now = st.radio("do you want a force fine-tune now?", ["YES", "NO"])

if fine_tune_now =="YES":
    fine_tune()

st.subheader("📊 System Performance")
cpu_usage = psutil.cpu_percent()
mem_usage = psutil.virtual_memory().percent
st.metric(label="CPU Usage", value=f"{cpu_usage}%")
st.metric(label="Memory Usage", value=f"{mem_usage}%")