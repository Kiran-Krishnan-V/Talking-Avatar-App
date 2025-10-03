import subprocess
import os
import argparse
import datetime
import time
import tempfile

def run_tts(text, output_audio_path="tmp/audio.wav", speaker=None):
    start_time = time.time()
    os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)
    tts_script = os.path.join(os.getcwd(), "generate_audio_google.py")

    cleaned_text = text.replace('\n\n', ' [PAUSE] ').replace('\n', ' ')
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as temp_file:
        temp_file.write(cleaned_text)
        temp_text_path = temp_file.name

    # Run directly in the current environment (ditto_env)
    cmd = ["python", tts_script, temp_text_path, output_audio_path]
    if speaker:
        cmd.append(speaker)
    print(f"Running TTS command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    os.unlink(temp_text_path)

    if result.returncode != 0:
        print(f"TTS stderr: {result.stderr}")
        print(f"TTS stdout: {result.stdout}")
        raise RuntimeError(f"TTS generation failed: {result.stderr}")
    end_time = time.time()
    print(f"Generated audio: {output_audio_path} (Took {end_time - start_time:.2f} seconds)")

def run_ditto_pipeline(audio_path, source_image_path, output_video_path):
    start_time = time.time()
    os.makedirs(os.path.dirname(output_video_path), exist_ok=True)
    working_dir = os.path.join(os.getcwd(), "ditto-talkinghead-windows")
    cmd = [
        "python", "inference.py",
        "--data_root", ".\\checkpoints\\ditto_trt_custom",
        "--cfg_pkl", ".\\checkpoints\\ditto_cfg\\v0.4_hubert_cfg_trt.pkl",
        "--audio_path", os.path.join("..", audio_path),
        "--source_path", os.path.join("..", source_image_path),
        "--output_path", os.path.join("..", output_video_path)
    ]
    result = subprocess.run(cmd, cwd=working_dir, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Ditto pipeline failed: {result.stderr}")
    end_time = time.time()
    print(f"Generated video: {output_video_path} (Took {end_time - start_time:.2f} seconds)")

def main():
    parser = argparse.ArgumentParser(description="Generate a talking avatar video from text.")
    parser.add_argument("--text", help="Text to convert to speech")
    parser.add_argument("--text_file", help="Path to a text file containing the speech")
    parser.add_argument("--source_image", default=".\\example\\avatar4.jpg", help="Path to source image")
    parser.add_argument("--output_dir", default="output_videos", help="Output directory for the video")
    parser.add_argument("--speaker", default="en-US-Neural2-D", help="Google TTS voice name (e.g., en-US-Neural2-F for female, en-US-Neural2-D for male)")
    args = parser.parse_args()

    # Default to speech.txt in the project folder if neither --text nor --text_file is provided
    default_text_file = os.path.join(os.getcwd(), "speech.txt")

    if args.text_file:
        with open(args.text_file, "r", encoding="utf-8") as f:
            text = f.read()
        print(f"Text from file: {text}")
    elif args.text:
        text = args.text
        print(f"Text from argument: {text}")
    else:
        # Use the default speech.txt if no text or file is provided
        if not os.path.exists(default_text_file):
            raise FileNotFoundError(f"Default text file not found: {default_text_file}")
        with open(default_text_file, "r", encoding="utf-8") as f:
            text = f.read()
        print(f"Text from default file (speech.txt): {text}")

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_video_path = os.path.join(args.output_dir, f"result_{timestamp}.mp4")
    temp_audio_path = "tmp/audio.wav"

    try:
        run_tts(text, temp_audio_path, args.speaker)
        run_ditto_pipeline(temp_audio_path, args.source_image, output_video_path)
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
            print("Cleaned up temporary audio file:", temp_audio_path)
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    main()