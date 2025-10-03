from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
import os
import subprocess
from datetime import datetime
import glob
import time

def index(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        text = request.POST.get('text')
        voice = request.POST.get('voice')  # Get the selected voice

        if not image or not text:
            return render(request, 'avatar/index.html', {'error': 'Please provide both an image and text.'})

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        session_dir = os.path.join(settings.MEDIA_ROOT, 'uploads', timestamp)
        os.makedirs(session_dir, exist_ok=True)

        image_path = os.path.join(session_dir, image.name)
        with open(image_path, 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)

        text_path = os.path.join(session_dir, 'speech.txt')
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(text)

        output_dir = os.path.join(settings.MEDIA_ROOT, 'output_videos', timestamp)
        os.makedirs(output_dir, exist_ok=True)

        try:
            cmd = [
                'conda', 'run', '-n', 'ditto_env', 'python',
                os.path.join(settings.BASE_DIR, 'generate_talking_avatar.py'),
                '--source_image', image_path,
                '--text_file', text_path,
                '--output_dir', output_dir,
                '--speaker', voice
            ]
            print(f"Running command: {' '.join(cmd)}")
            subprocess.run(cmd, check=True, timeout=600)  # Removed capture_output=True, added timeout

            # Wait briefly for the file to be written
            time.sleep(1)

            # Find the actual video file
            video_files = glob.glob(os.path.join(output_dir, 'result_*.mp4'))
            print(f"Found video files: {video_files}")
            if not video_files:
                raise FileNotFoundError("No video file found in output directory.")
            actual_video_file = video_files[0]
            video_relative_path = os.path.join('output_videos', timestamp, os.path.basename(actual_video_file)).replace('\\', '/')
            return redirect('avatar:result', video_path=video_relative_path)

        except subprocess.TimeoutExpired:
            print("Subprocess timed out after 600 seconds.")
            error_message = "Video generation took too long. Please try again with a shorter text or smaller image."
            return render(request, 'avatar/index.html', {'error': error_message})
        except subprocess.CalledProcessError as e:
            print(f"Subprocess failed: {e}")
            error_message = f"Failed to generate video. Error: {e}"
            return render(request, 'avatar/index.html', {'error': error_message})
        except Exception as e:
            print(f"Unexpected error: {e}")
            error_message = f"An unexpected error occurred: {e}"
            return render(request, 'avatar/index.html', {'error': error_message})

    return render(request, 'avatar/index.html')

def result(request, video_path):
    context = {
        'video_url': os.path.join(settings.MEDIA_URL, video_path).replace('\\', '/'),
        'video_path': video_path.replace('\\', '/')
    }
    return render(request, 'avatar/result.html', context)

def download_video(request, video_path):
    video_full_path = os.path.join(settings.MEDIA_ROOT, video_path.replace('/', os.sep))
    if os.path.exists(video_full_path):
        with open(video_full_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='video/mp4')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(video_path)}"'
            return response
    else:
        return HttpResponse("Video not found.", status=404)