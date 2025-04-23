import whisper

# Load the Whisper model
model = whisper.load_model("base")

# Transcribe the recorded audio file
result = model.transcribe("output.wav")

# Save the text to a file
with open("transcribed_text.txt", "w") as file:
    file.write(result["text"])

print("Transcribed text saved. Now running stress analysis...")

# Run stress analysis automatically
import os
os.system("python analyze_stress.py")
