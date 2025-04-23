import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace
import random
import whisper
import sounddevice as sd
import scipy.io.wavfile as wav
import time
import os
from textblob import TextBlob
from datetime import datetime
import pygame
from plyer import notification
from twilio.rest import Client
import pyttsx3
import matplotlib.pyplot as plt

# Twilio Credentials (Replace with your own credentials)
TWILIO_SID = "ACcbb156d81cb7c87e50ccf9101939809f"
TWILIO_AUTH_TOKEN = "978d7bc167e57d28f0e94a052dc804fc"
TWILIO_PHONE_NUMBER = "+19202899277"
USER_PHONE_NUMBER = "+916369311554"

# Load Whisper model
model = whisper.load_model("base")

# Initialize Streamlit app
st.title("AI Stress & Sleep Assistant 🧠💤")

# Text-to-Speech Function
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Initialize session state for stress trends
if 'stress_trends' not in st.session_state:
    st.session_state.stress_trends = []
if 'analysis_completed' not in st.session_state:
    st.session_state.analysis_completed = False

# Function to plot stress trends
def plot_stress_trends():
    if st.session_state.stress_trends:
        timestamps, stress_levels = zip(*st.session_state.stress_trends)
        plt.figure(figsize=(10, 5))
        plt.plot(timestamps, stress_levels, marker='o')
        plt.title("Stress Trends Over Time")
        plt.xlabel("Time")
        plt.ylabel("Stress Level")
        plt.xticks(rotation=45)
        plt.grid(True)
        st.pyplot(plt)

# Real-Time Speech Analysis
st.header("🎤 Speech-to-Text Analysis")
if st.button("Start Recording & Analyze Stress"):
    def record_audio(filename="audio.wav", duration=5, fs=44100):
        st.write("🎙️ Recording audio... Speak now!")
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype=np.int16)
        sd.wait()
        wav.write(filename, fs, audio)
        st.write("✅ Recording complete!")

    def analyze_speech():
        result = model.transcribe("audio.wav", language="en")
        transcribed_text = result["text"].strip()
        blob = TextBlob(transcribed_text)
        polarity = blob.sentiment.polarity
        stress_keywords = ["stressed", "depressed", "anxious", "overwhelmed", "frustrated", "exhausted"]
        if any(word in transcribed_text.lower() for word in stress_keywords):
            polarity = -0.5
        if polarity < -0.1:
            stress_level = "High Stress 😟"
            recommendations = ["☕ Take short breaks every hour.", "💬 Talk to a friend or family member.", "🧘 Try 5 minutes of mindfulness meditation."]
        elif -0.1 <= polarity < 0.3:
            stress_level = "Moderate Stress 😐"
            recommendations = ["🚶 Go for a short walk.", "🌿 Step outside and get some fresh air.", "📅 Organize your tasks to reduce stress."]
        else:
            stress_level = "Low Stress 🙂"
            recommendations = ["😊 Keep up your good mood!", "🎨 Engage in a creative hobby.", "🏃 Stay active and exercise regularly."]

        # Update stress trends
        current_time = datetime.now().strftime("%H:%M")
        stress_level_value = 1 if stress_level == "High Stress 😟" else 0.5 if stress_level == "Moderate Stress 😐" else 0
        st.session_state.stress_trends.append((current_time, stress_level_value))

        # Mark analysis as completed
        st.session_state.analysis_completed = True

        return transcribed_text, stress_level, random.sample(recommendations, 3)

    record_audio()
    transcribed_text, stress_level, recommendations = analyze_speech()
    st.write("📝 Transcribed Text:", transcribed_text)
    st.write("📊 Stress Level:", stress_level)
    st.write("💡 Recommendations:")
    for rec in recommendations:
        st.write(f"- {rec}")
    text_to_speech(f"Your stress level is {stress_level}. Here are some recommendations: {', '.join(recommendations)}")

# Show the chart button only if analysis is completed
if st.session_state.analysis_completed:
    if st.button("Show Stress Trends Chart"):
        plot_stress_trends()

# Real-Time Emotion Analysis
st.header("📷 Real-Time Emotion Analysis")
if 'camera_active' not in st.session_state:
    st.session_state.camera_active = False
if 'captured_emotion' not in st.session_state:
    st.session_state.captured_emotion = None
if 'captured_stress' not in st.session_state:
    st.session_state.captured_stress = None
if 'captured_recommendations' not in st.session_state:
    st.session_state.captured_recommendations = []

def detect_emotion(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = DeepFace.analyze(frame_rgb, actions=['emotion'], enforce_detection=False)
    emotion = faces[0]['dominant_emotion'] if faces else "No face detected"
    stress_mapping = {"angry": "High Stress 😟", "sad": "High Stress 😟", "fear": "High Stress 😟", "neutral": "Moderate Stress 😐", "disgust": "Moderate Stress 😐", "happy": "Moderate Stress 😐", "surprise": "Moderate Stress 😐"}
    stress_level = stress_mapping.get(emotion, "Unknown")
    recommendations = {"High Stress 😟": ["🎶 Listen to calming music.", "💤 Take a quick power nap.", "🧘 Try deep breathing exercises."], "Moderate Stress 😐": ["🚶 Go for a short walk.", "🌊 Practice deep breathing exercises.", "📖 Read a book to calm your mind."], "Low Stress 🙂": ["😊 Keep up your good mood!", "🎨 Engage in a creative hobby.", "🏃 Stay active and exercise regularly."]}

    # Update stress trends
    current_time = datetime.now().strftime("%H:%M")
    stress_level_value = 1 if stress_level == "High Stress 😟" else 0.5 if stress_level == "Moderate Stress 😐" else 0
    st.session_state.stress_trends.append((current_time, stress_level_value))

    return emotion, stress_level, recommendations.get(stress_level, [])

if st.button("Start Camera"):
    st.session_state.camera_active = True
    st.session_state.cap = cv2.VideoCapture(0)

if st.button("Stop Camera"):
    st.session_state.camera_active = False
    if 'cap' in st.session_state and st.session_state.cap is not None:
        st.session_state.cap.release()
        st.session_state.cap = None

if st.session_state.camera_active:
    ret, frame = st.session_state.cap.read()
    if ret:
        st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")
    if st.button("Capture Emotion") and ret:
        emotion, stress_level, recommendations = detect_emotion(frame)
        st.session_state.captured_emotion = emotion
        st.session_state.captured_stress = stress_level
        st.session_state.captured_recommendations = recommendations

        # Mark analysis as completed
        st.session_state.analysis_completed = True

if st.session_state.captured_emotion:
    st.write(f"🎭 Detected Emotion: {st.session_state.captured_emotion}")
    st.write(f"📊 Stress Level: {st.session_state.captured_stress}")
    st.write("💡 Recommendations:")
    for rec in random.sample(st.session_state.captured_recommendations, min(3, len(st.session_state.captured_recommendations))):
        st.write(f"- {rec}")

# Sleep Quality Analysis
st.header("💤 Sleep Quality Analysis")
sleep_data = st.text_area("Enter your sleep data (e.g., hours slept, quality):")
if st.button("Analyze Sleep Quality"):
    if sleep_data:
        st.write("📊 Sleep Analysis:")
        st.write("Based on your input, here are some insights:")
        st.write("- Aim for 7-9 hours of sleep per night.")
        st.write("- Avoid caffeine and screens before bedtime.")
        st.write("- Maintain a consistent sleep schedule.")
    else:
        st.write("Please enter your sleep data.")

# Interactive Chatbot
st.header("🤖 Interactive Chatbot")
user_input = st.text_input("Ask me anything about stress or sleep:")
if user_input:
    st.write("🤖 Chatbot Response:")
    st.write("Here are some tips to help you:")
    st.write("- Practice deep breathing exercises.")
    st.write("- Try mindfulness meditation.")
    st.write("- Maintain a healthy sleep routine.")

# Community Support
st.header("👥 Community Support")
st.write("Join our community forum to share your experiences and support others:")
st.write("[Community Forum Link](#)")

# Gamification
st.header("🎮 Gamification")
st.write("Earn points and badges for completing stress management activities:")
st.write("- 🏆 Complete 5 activities to earn the 'Stress Buster' badge.")
st.write("- 🎯 Set a daily goal and track your progress.")

# Educational Content
st.header("📚 Educational Content")
st.write("Learn more about stress management and sleep hygiene:")
st.write("- Article: [10 Tips for Better Sleep](#)")
st.write("- Video: [Mindfulness Meditation for Stress Relief](#)")

# Sleep Reminder Section
st.header("⏰ Sleep Reminder")
alarm_time = st.text_input("Enter Sleep Alarm Time (HH:MM)")

if st.button("Set Alarm"):
    st.write(f"🔔 Alarm set for {alarm_time}")
    current_time = datetime.now().strftime("%H:%M")

    # Wait until the alarm time is reached
    while current_time != alarm_time:
        time.sleep(1)
        current_time = datetime.now().strftime("%H:%M")

    # Play alarm sound
    pygame.mixer.init()
    pygame.mixer.music.load("alarm.wav")  # Ensure you have an alarm.wav file in your directory
    pygame.mixer.music.play()

    # Send pop-up notification
    notification.notify(
        title="Sleep Reminder",
        message="It's time to sleep!",
        timeout=10  # Notification stays for 10 seconds
    )

    # Send SMS using Twilio
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body="It's time to sleep!",
            from_=TWILIO_PHONE_NUMBER,
            to=USER_PHONE_NUMBER
        )
        st.success("SMS sent successfully!")
    except Exception as e:
        st.error(f"Failed to send SMS: {e}")

    st.write("🔔 Alarm triggered! Check your notifications and SMS.")