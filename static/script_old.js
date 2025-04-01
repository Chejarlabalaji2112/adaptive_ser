async function uploadAudio() {
    let fileInput = document.getElementById("audioFile");
    if (!fileInput.files.length) {
        alert("Please select a WAV file.");
        return;
    }
    
    let formData = new FormData();
    formData.append("file", fileInput.files[0]);
    
    let response = await fetch("/predict", { method: "POST", body: formData });
    let result = await response.json();
    
    document.getElementById("predictedEmotion").innerText = result.emotion;
    document.getElementById("confidence").innerText = result.confidence.toFixed(2) + "%";
    document.getElementById("feedbackSection").style.display = "block";
}

async function recordAudio() {
    let response = await fetch("/record", { method: "POST" });
    let result = await response.json();
    
    document.getElementById("predictedEmotion").innerText = result.emotion;
    document.getElementById("confidence").innerText = result.confidence.toFixed(2) + "%";
    document.getElementById("feedbackSection").style.display = "block";
}

async function submitFeedback(response) {
    if (response === "Yes") {
        alert("Thanks for confirming!");
    } else {
        let correctEmotion = prompt("Enter the correct emotion (neutral, happy, sad, angry, surprise, fear, disgust):");
        if (!correctEmotion) return;
        
        let feedbackData = { file_path: "", correct_emotion: correctEmotion };
        await fetch("/feedback", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(feedbackData) });
        alert("Thanks for the feedback!");
    }
}

