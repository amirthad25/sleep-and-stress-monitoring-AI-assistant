🧘‍♀️ SereneMind – AI-Powered Stress and Sleep Wellness Assistant

SereneMind is an intelligent wellness assistant that uses real-time voice and facial emotion analysis to detect stress levels and guide users toward a healthier mental state.It acts like an AI companion (similar to Siri), providing voice feedback, reminders, breathing exercises, and stress tracking — all in one place.

-🔍 Features

🎙️ Real-Time Voice Analysis
- Records voice input using a live microphone.
- Analyzes vocal tone, pitch, and frequency using ML models.
- Predicts whether the user is under **high or low stress**.
- Provides personalized **voice instructions** to reduce stress.
- Reads feedback out loud using Text-to-Speech (TTS) like Siri.

🎥 Real-Time Facial Emotion Detection
- Captures live video through the webcam.
- Detects facial expressions to assess emotional states.
- Predicts stress levels based on visual cues.
- Gives soothing spoken responses if high stress is detected.

🌬️ Breathing Exercise Assistant
- Guides users through AI-based breathing exercises.
- Uses calming audio and visual cues to help users relax.

⏰ Smart Sleep Alarm with Reminders
- Allows users to set a **daily sleep alarm** (e.g., 10:00 PM).
- Sends SMS reminders using **Twilio**: "Time to sleep – rest well!".
- Plays a gentle beep/alarm when it's time to sleep.

📊 Stress Level Dashboard
- Plots real-time and historical **stress level graphs**.
- Helps users track emotional patterns and improvements over time.

🛠️ Tech Stack
- Python
- OpenCV – Face detection
- Librosa / PyAudio – Voice recording & feature extraction
- TensorFlow / Keras– ML models for emotion/stress detection
- Twilio API– SMS reminders
- Matplotlib / Seaborn – Data visualization
- Text-to-Speech (pyttsx3/gTTS)– Voice response
- Streamlit / Flask – Frontend (optional)

