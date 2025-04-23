from textblob import TextBlob
import whisper

# Load Whisper model
model = whisper.load_model("base")

# Transcribe audio file
audio_file = "audio.wav"  # Change this if needed
result = model.transcribe(audio_file)
transcribed_text = result["text"]

# Analyze sentiment
blob = TextBlob(transcribed_text)
polarity = blob.sentiment.polarity  # Ranges from -1 (negative) to 1 (positive)

# Determine stress level
if polarity < -0.3:
    stress_level = "High Stress 😟"
elif -0.3 <= polarity < 0.3:
    stress_level = "Moderate Stress 😐"
else:
    stress_level = "Low Stress 🙂"

# Output results
print("\nTranscribed Text:", transcribed_text)
print("Sentiment Score:", polarity)
print("Stress Level:", stress_level)
