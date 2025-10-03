# Talking Avatar Web App

This is a Django-based web application that generates a talking avatar video from an image and text input. It uses the Ditto talking-head pipeline for video generation and Google Cloud Text-to-Speech for audio synthesis.

## Overview

This project is set up to work on Windows using the `ditto-talkinghead-windows` pipeline, a Windows-specific version of the Ditto Talking-Head pipeline. For other operating systems, you can use the original Ditto repository.

## Features

- Upload an image and input text to generate a talking avatar video.
- Choose from different voices using Google Cloud Text-to-Speech.
- View and download the generated video.

## Prerequisites

Before setting up the project, ensure you have the following:

- **Python 3.9+**: Download and install from python.org.
- **Conda**: Install Miniconda or Anaconda from docs.conda.io.
- **Google Cloud Account**: Sign up at cloud.google.com and enable the Text-to-Speech API.

## Setup Instructions

Follow these steps to set up the project on your local machine (Windows instructions provided, but steps are similar for other operating systems).

### 1. Check Out the Repository

Since this project is hosted on an SVN repository, you’ll use TortoiseSVN to check out the project files.  

The checked-out folder will contain the project files, including the `ditto-talkinghead-windows` directory with the pipeline code for Windows.

### 2. Set Up the Conda Environment

1. **Install Conda**:
       - Download and install Miniconda or Anaconda from [docs.conda.io](https://docs.conda.io/en/latest/miniconda.html).

2. **Create the Environment**:
       - We’ve used Python 3.11.13 for this project. Create the Conda environment with this version:
        conda create -n ditto_env python=3.11.13
        conda activate ditto_env


### 3. Set Up the Ditto Talking-Head Pipeline

The `ditto-talkinghead-windows` pipeline code is already included in the repository, as it’s the Windows-specific version of the Ditto Talking-Head pipeline.

- **Original Ditto Repository** (for non-Windows users):
    - Repository: [https://github.com/antgroup/ditto-talkinghead.git](https://github.com/antgroup/ditto-talkinghead.git)
    - Checkpoints: Download from [https://huggingface.co/digital-avatar/ditto-talkinghead](https://huggingface.co/digital-avatar/ditto-talkinghead)

 - **Windows-Specific Ditto Repository** (included in this project):
    - Repository: [https://github.com/justinjohn0306/ditto-talkinghead-windows.git](https://github.com/justinjohn0306/ditto-talkinghead-windows.git)
    - Checkpoints: Download from [https://huggingface.co/justinjohn-03/ditto-talkinghead-windows](https://huggingface.co/justinjohn-03/ditto-talkinghead-windows)

#### Steps for Ditto Setup

1. **Follow Installation Instructions**:
    - Refer to the installation instructions in the respective Ditto repositories:
    - For Windows: [ditto-talkinghead-windows](https://github.com/justinjohn0306/ditto-talkinghead-windows.git)
    - For other OS: [ditto-talkinghead](https://github.com/antgroup/ditto-talkinghead.git)

2. **Download Checkpoints**:
    - For Windows, download the checkpoints from [https://huggingface.co/justinjohn-03/ditto-talkinghead-windows](https://huggingface.co/justinjohn-03/ditto-talkinghead-windows).
    - Place the downloaded checkpoint files in the `ditto-talkinghead-windows/checkpoints/` directory:
    
      `````
      mkdir ditto-talkinghead-windows\checkpoints
      `````
    - Note: The `checkpoints/` directory is excluded from the SVN repository via `svn:ignore` due to its size.
    
3. **Install Ditto Dependencies**:
    - A separate `requirements-ditto.txt` file is provided for the Ditto pipeline. Install the dependencies:
      `````
      pip install -r requirements-ditto.txt
      `````

    - The `requirements-ditto.txt` contains:
    `````
        tensorrt==8.6.1
        librosa
        tqdm
        filetype
        imageio
        opencv_python_headless
        scikit-image
        cython
        cuda-python
        imageio-ffmpeg
        colored
        polygraphy
        numpy==1.26.4
        torch==2.3.1+cu121
        onnxruntime-gpu==1.22.0
        scipy==1.15.3
        scikit-learn==1.7.0
        soundfile==0.13.1
    `````
    Note: Use the compatable torch and cuda versions to the appropriate device.
     
    
    -Note:
     We have provided the tensorRT model with hardware-compatibility-level=Ampere_Plus (checkpoints/ditto_trt_Ampere_Plus/). If your GPU does not support it, please execute the cvt_onnx_to_trt.py script to convert from the general onnx model (checkpoints/ditto_onnx/) to the tensorRT model.
    ````
     python scripts/cvt_onnx_to_trt.py --onnx_dir "./checkpointsditto_onnx" --trt_dir "./checkpoints/ditto_trt_custom"
    ````

### 4. Install General Project Dependencies

The main project dependencies are listed in `requirements.txt`. Install them:

    
    pip install -r requirements.txt
    

The `requirements.txt` contains the essential dependencies for the Talking Avatar Web App, including:

    django==5.2.3
    google-cloud-texttospeech
    gunicorn
    pillow
    requests==2.32.4
    sqlparse==0.5.3
    tzdata==2025.2


### 5. Set Up Google Cloud Text-to-Speech

The app uses Google Cloud Text-to-Speech for audio generation. Set up your credentials:

1. **Create a Google Cloud Project**:
    - Go to [cloud.google.com](https://cloud.google.com).
    - Create a new project (e.g., `talking-avatar-project`).
    - Enable the Text-to-Speech API for your project.

2. **Generate Credentials**:
    - In the Google Cloud Console, go to `APIs & Services > Credentials`.
    - Create a Service Account and download the JSON key file (e.g., `google-credentials.json`).

3. **Set Up the Credentials**:
    - Copy the `google-credentials.json` file to the project root (`C:\svn_working_copy\talking_avatar_app\`):
        
    - Set the environment variable:
        set GOOGLE_APPLICATION_CREDENTIALS=google-credentials.json
    - Note: `google-credentials.json` is excluded from the SVN repository via `svn:ignore`.

### 6. Set Up Media Directories

Create the necessary directories for uploads and outputs:

    mkdir media\uploads media\output_videos


These directories are excluded from the SVN repository via `svn:ignore`.

### 7. Run the App

1. **Apply Django Migrations**:

        python manage.py makemigrations
        python manage.py migrate

2. **Start the Development Server**:

        python manage.py runserver

3. **Access the App**:
    - Open your browser and go to `http://127.0.0.1:8000`.
    - Upload an image, enter text, select a voice, and generate the talking avatar video.

## Additional Notes

- **GPU Recommendation**: A system with a GPU is recommended for faster video generation using the Ditto pipeline. A CPU will work but may be slower.
- **Troubleshooting**:
- If video generation fails, ensure the Ditto checkpoints are correctly placed in `ditto-talkinghead-windows/checkpoints/`.
- If Google Text-to-Speech fails, verify that `GOOGLE_APPLICATION_CREDENTIALS` is set and the API is enabled in your Google Cloud project.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).































