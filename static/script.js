let audioContext, recorder, audioChunks = [];

// 📌 Upload & Predict Audio
function uploadAudio() {
    let fileInput = document.getElementById("audioUpload");
    if (!fileInput.files.length) {
        alert("Please upload an audio file.");
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch("/predict", { method: "POST", body: formData })
        .then(response => response.json())
        .then(data => {
            document.getElementById("predictionResult").innerHTML =
                `<h3>Predicted Emotion: ${data.emotion} 😃</h3>
                 <p>Confidence: ${data.confidence.toFixed(2)}%</p>`;
            drawWaveform(URL.createObjectURL(fileInput.files[0]));
        })
        .catch(error => console.error("Error:", error));
}

// 📌 Start Recording
function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            audioContext = new AudioContext();
            let input = audioContext.createMediaStreamSource(stream);
            recorder = new MediaRecorder(stream);

            recorder.ondataavailable = event => audioChunks.push(event.data);
            recorder.start();

            document.getElementById("recordBtn").disabled = true;
            document.getElementById("stopBtn").disabled = false;
        })
        .catch(error => console.error("Error accessing microphone:", error));
}

// 📌 Stop Recording & Send Audio
function stopRecording() {
    recorder.stop();
    recorder.onstop = () => {
        let audioBlob = new Blob(audioChunks, { type: "audio/wav" });
        let formData = new FormData();
        formData.append("file", audioBlob, "recorded_audio.wav");

        fetch("/predict", { method: "POST", body: formData })
            .then(response => response.json())
            .then(data => {
                document.getElementById("predictionResult").innerHTML =
                    `<h3>Predicted Emotion: ${data.emotion} 😃</h3>
                     <p>Confidence: ${data.confidence.toFixed(2)}%</p>`;
                drawWaveform(URL.createObjectURL(audioBlob));
            })
            .catch(error => console.error("Error:", error));

        audioChunks = [];
        document.getElementById("recordBtn").disabled = false;
        document.getElementById("stopBtn").disabled = true;
    };
}

document.addEventListener("DOMContentLoaded", function () {
    const noFeedback = document.getElementById("no_feedback");
    const correctEmotionDropdown = document.getElementById("correct_emotion_dropdown");

    // Get all radio buttons
    const feedbackOptions = document.getElementsByName("feedback");

    feedbackOptions.forEach(option => {
        option.addEventListener("change", function () {
            if (noFeedback.checked) {
                correctEmotionDropdown.style.display = "block"; // Show dropdown
            } else {
                correctEmotionDropdown.style.display = "none"; // Hide dropdown
            }
        });
    });
});


