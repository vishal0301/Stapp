let mediaRecorder;
let audioChunks = [];

document.getElementById("record-btn").onclick = async () => {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);
  mediaRecorder.start();

  mediaRecorder.ondataavailable = (event) => {
    audioChunks.push(event.data);
  };

  mediaRecorder.onstop = async () => {
    const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
    const formData = new FormData();
    formData.append("file", audioBlob, "recording.wav");

    // Send the audio to the Flask backend
    fetch("http://localhost:5000/upload_audio", {
      method: "POST",
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      console.log("Summarized data:", data);
      alert("Audio summarized successfully.");
    })
    .catch(error => console.error("Error:", error));
  };

  document.getElementById("record-btn").disabled = true;
  document.getElementById("stop-btn").disabled = false;
};

document.getElementById("stop-btn").onclick = () => {
  mediaRecorder.stop();
  document.getElementById("record-btn").disabled = false;
  document.getElementById("stop-btn").disabled = true;
};
