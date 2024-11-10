import streamlit as st
import openai
import os
import tempfile
import speech_recognition as sr
from flask import Flask, request, jsonify
from threading import Thread
import requests

# Initialize Flask app
flask_app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = 'Liv Assist'

# Transcribe audio function
def transcribe_audio(audio_file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Audio not clear enough for transcription."
    except sr.RequestError:
        return "Could not request transcription service."

# Summarize text using OpenAI API
def summarize_text(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Summarize this text:\n\n{text}",
        max_tokens=100
    )
    return response.choices[0].text.strip()

# Flask route to handle audio uploads
@flask_app.route('/upload_audio', methods=['POST', 'GET'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file found"}), 400
    
    file = request.files['file']
    temp_audio_file_path = os.path.join(tempfile.gettempdir(), "uploaded_audio.wav")
    file.save(temp_audio_file_path)  # Save the audio file temporarily

    # Process the uploaded audio file
    transcription = transcribe_audio(temp_audio_file_path)
    summary = summarize_text(transcription)

    # Clean up the temporary audio file
    os.remove(temp_audio_file_path)

    # Store the results for display in Streamlit
    global latest_transcription, latest_summary
    latest_transcription = transcription
    latest_summary = summary

    # Return the processed results as JSON
    return jsonify({
        "transcription": transcription,
        "summary": summary
    }), 200

# Initialize global variables for displaying in Streamlit
latest_transcription = ""
latest_summary = ""

# Function to run the Flask app in a separate thread
def run_flask():
    flask_app.run(port=5000)

# Streamlit app layout
def streamlit_app():
    st.title("Audio Summarization and Strategy Planner")

    # File uploader for audio
    uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])

    if uploaded_file is not None:
        # Save the uploaded audio file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            temp_audio_file.write(uploaded_file.read())
            temp_audio_file_path = temp_audio_file.name

        # Send audio file to Flask API
        with open(temp_audio_file_path, 'rb') as audio_file:
            response = requests.post("http://localhost:5000/upload_audio", files={"file": audio_file})
            if response.status_code == 200:
                data = response.json()
                st.subheader("Transcription")
                st.write(data["transcription"])
                st.subheader("Summary")
                st.write(data["summary"])
            else:
                st.error("Error processing audio file.")

        # Clean up the temporary audio file
        os.remove(temp_audio_file_path)

    # Display the latest results fetched from Flask API
    st.subheader("Latest Transcription (Automatic)")
    st.write(latest_transcription)
    st.subheader("Latest Summary (Automatic)")
    st.write(latest_summary)

# Run both Flask and Streamlit apps in parallel
if __name__ == "__main__":
    # Start Flask app in a separate thread
    Thread(target=run_flask).start()
    # Run Streamlit app
    streamlit_app()
