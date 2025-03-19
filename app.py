import cv2
import pyttsx3
import os
import tensorflow as tf
import speech_recognition as sr
import requests
import json
from deepface import DeepFace


os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"


DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")  
DEEPSEEK_API_URL = "https://openrouter.ai/api/v1/chat/completions"


engine = pyttsx3.init()


LOW_MOOD = ["sad", "fear", "angry"]


conversation_history = []

def speak(text):
    """Convert text to speech."""
    print("AI Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen_query(prompt="Please say something..."):
  
    speak(prompt)
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio)
        print("You said:", query)
        return query
    except sr.UnknownValueError:
        print("Sorry, I could not understand.")
        return ""
    except sr.RequestError as e:
        print("Speech recognition error:", e)
        return ""

def analyze_emotion(frame):
 
    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion'] if isinstance(result, list) else result['dominant_emotion']
        return emotion
    except Exception as e:
        print("Error analyzing emotion:", e)
        return "neutral"

def deepseek_chatbot(emotion, query):

    global conversation_history

    if not DEEPSEEK_API_KEY:
        print("Error: DeepSeek API key not found.")
        return "API key is missing."


    if not conversation_history:
        conversation_history.append({
            "role": "system",
            "content": f"You are a helpful AI assistant. The user is currently feeling {emotion}."
        })


    conversation_history.append({"role": "user", "content": query})

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek/deepseek-r1-distill-llama-8b",
        "messages": conversation_history,
        "temperature": 1.0
    }
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            reply = result["choices"][0]["message"]["content"]
            conversation_history.append({"role": "assistant", "content": reply})
            return reply
        else:
            print("API Error:", response.text)
            return "Sorry, I couldn't process your request."
    except Exception as e:
        print("Error during API call:", e)
        return "An error occurred while communicating with the AI."

def ask_query_flow(current_emotion):
    """Guide user through query flow based on detected emotion."""
    user_query = listen_query("I noticed you're feeling low. What would you like to talk about?")
    if not user_query:
        return

    response = deepseek_chatbot(current_emotion, user_query)
    print("DeepSeek Response:", response)
    speak(response)

    follow_query = listen_query("Would you like to ask anything else?")
    if follow_query:
        follow_response = deepseek_chatbot(current_emotion, follow_query)
        print("Follow-up Response:", follow_response)
        speak(follow_response)

def live_emotion_and_chat():
  
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        speak("Error: Unable to access camera.")
        return

    prev_emotion = None
    speak("Live emotion detection started. Press 'q' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            speak("Camera error detected.")
            break
        
        resized_frame = cv2.resize(frame, (640, 480))
        current_emotion = analyze_emotion(resized_frame)
        print("Detected Emotion:", current_emotion or "neutral")

        if current_emotion in LOW_MOOD and current_emotion != prev_emotion:
            ask_query_flow(current_emotion)
        
        prev_emotion = current_emotion

        cv2.imshow('Live Emotion Detection', resized_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    live_emotion_and_chat()

if __name__ == "__main__":
    main()
