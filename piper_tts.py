import subprocess

def text_to_speech(text, output_file="output.wav"):
    command = [
        "piper",
        "--model", "en_US/jenny-medium.onnx",
        "--text", text,
        "--output-file", output_file
    ]
    subprocess.run(command)

# Example usage
text_to_speech("Hello, welcome to your AI assistant!")
