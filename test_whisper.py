import whisper

# Load Whisper model (use 'base' for faster processing, or 'large' for best accuracy)
model = whisper.load_model("base")

# Transcribe an audio file (replace 'audio.wav' with your actual file)
result = model.transcribe("audio.wav")

# Print the transcribed text
print("Transcribed Text:", result["text"])
