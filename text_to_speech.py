import azure.cognitiveservices.speech as speechsdk

# Set your Azure Speech API key and region
SPEECH_KEY = "your_subscription_key_here"
SPEECH_REGION = "your_region_here"

def text_to_speech(text):
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("✅ Speech synthesis successful!")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = result.cancellation_details
        print(f"⚠️ Speech synthesis failed! Reason: {cancellation.reason}")
        if cancellation.reason == speechsdk.CancellationReason.Error:
            print(f"🔴 Error details: {cancellation.error_details}")
            print("🔎 Make sure your API key and region are correct!")
    else:
        print(f"Unexpected result: {result.reason}")

# Test the function
if __name__ == "__main__":
    text_to_speech("Hello! This is a test of Azure Text to Speech.")
