



# Virtual Assistant: Emotion-Driven Interactive Chatbot with Live Emotion Detection

A smart virtual assistant that uses your webcam to capture real-time video, analyzes your emotional state using DeepFace, and engages in a natural conversation via the DeepSeek API. The assistant also uses text-to-speech (TTS) and speech recognition to provide a seamless interactive experience and can trigger IoT-like actions based on detected emotions.

## Demo Video
> **Note:** Please unmute the video manually by clicking the sound icon 🔊

https://github.com/user-attachments/assets/03d525b0-e0b6-4253-a30d-2960a39d10c5





## Features

- **Live Emotion Detection:** Continuously analyzes facial expressions (using DeepFace) to determine the user’s dominant emotion.
- **Voice Interaction:** Utilizes speech recognition to capture queries and pyttsx3 to convert text responses to speech.
- **Conversational AI:** Leverages the DeepSeek API (with a specified model) to generate context-aware responses based on conversation history and detected emotion.
- **Smart Interactions:** Automatically triggers follow-up questions or IoT-like actions (e.g., adjusting smart lighting) when low moods are detected.

## Dependencies

The project requires Python 3.8 or later and the following packages:

- OpenCV-Python
- pyttsx3
- TensorFlow
- SpeechRecognition
- Requests
- DeepFace

Install them using pip:

```bash
pip install opencv-python pyttsx3 tensorflow speechrecognition requests deepface
```

## Environment Setup

### Clone the Repository

```bash
git clone https://github.com/YourGitHubUsername/virtual-assistant.git
cd virtual-assistant
```

### Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

### Activate the Virtual Environment

#### Windows (CMD):

```cmd
venv\Scripts\activate
```

#### Windows (PowerShell):

```powershell
.\venv\Scripts\Activate.ps1
```

#### macOS/Linux:

```bash
source venv/bin/activate
```

### Install Dependencies

Either run:

```bash
pip install -r requirements.txt
```

(if you have a `requirements.txt` file with the dependencies listed) or install each package individually as shown above.

## Set Up the API Key

The assistant uses the DeepSeek API. Set your API key in an environment variable named `DEEPSEEK_API_KEY`:

#### Windows (CMD):

```cmd
set DEEPSEEK_API_KEY=your_api_key_here
```

#### Windows (PowerShell):

```powershell
$env:DEEPSEEK_API_KEY="your_api_key_here"
```

#### macOS/Linux:

```bash
export DEEPSEEK_API_KEY=your_api_key_here
```

## How to Run

Ensure your webcam is connected and accessible.

### Run the application:

```bash
python app.py
```

The assistant will start capturing video from your webcam, analyze your emotions in real-time, and if a low mood (e.g., sad, fear, angry) is detected, it will prompt you for a query and respond via voice.

Press 'q' in the video window to exit the application.
