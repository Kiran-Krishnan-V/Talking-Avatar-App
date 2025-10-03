import sys
import time
from google.cloud import texttospeech

def main():
    client = texttospeech.TextToSpeechClient()

    text_path = sys.argv[1]
    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read()
    print(f"Input text: {text}")
    print(f"Character count: {len(text)}")

    output_path = sys.argv[2]
    speaker = sys.argv[3] if len(sys.argv) > 3 else "en-US-Neural2-D"

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=speaker,  # Use the speaker argument directly as the Google TTS voice name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        speaking_rate=1.0,
        pitch=0.0,
    )

    start_time = time.time()
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )
    print(f"Audio generation took: {time.time() - start_time:.2f} seconds")

    with open(output_path, "wb") as f:
        f.write(response.audio_content)
    print(f"Generated audio: {output_path}")

if __name__ == "__main__":
    main()