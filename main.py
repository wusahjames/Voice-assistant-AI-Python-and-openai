import speech_recognition as sr
import pyttsx3
import os
import openai
from dotenv import load_dotenv

load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')

openai.api_key = "YOUR API KEY"

engine = pyttsx3.init()

recognizer = sr.Recognizer()

def speak_text(command):
    engine.say(command)
    engine.runAndWait()

def record_text():
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for input...")
                recognizer.adjust_for_ambient_noise(source, duration=0.2)
                audio = recognizer.listen(source)
                print("Audio captured.")

            text = recognizer.recognize_google(audio)
            if text:
                print(f"Recognized: {text}")
                return text
            else:
                print("No speech recognized.")

        except sr.RequestError as e:
            print(f"Could not request results: {e}")
        except sr.UnknownValueError:
            print("Unknown error occurred. Please speak clearly.")

def send_to_chatGPT(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].message.content

messages = []

while True:
    text = record_text()
    if text:
        messages.append({"role": "user", "content": text})
        response = send_to_chatGPT(messages)
        speak_text(response)
        print(f"Response: {response}")
