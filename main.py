import speech_recognition as sr
import pyttsx3
from datetime import datetime
import webbrowser
import openai
import numpy as np
from config import apikey
import os
import wikipedia

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 0.8
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio,language="en-IN")
        print(f"User: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        speak("sorry, i don't get it ")
        return ""
    except sr.RequestError as e:
        print(f"An error occurred during speech recognition: {e}")
        return ""

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

def get_gpt3_response(user_input):
    openai.api_key = apikey
    response = openai.Completion.create(
        engine="text-davinci-002",  
        prompt=user_input,
        max_tokens=150,
        temperature=0.7
    )
    return response['choices'][0]['text'].strip()


def get_greeting():
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        return "Good morning! How can I assist you?"
    elif 12 <= current_hour < 18:
        return "Good afternoon! How can I assist you?"
    else:
        return "Good evening! How can I assist you?"

if __name__ == "__main__":
    greeting = get_greeting()
    speak(greeting)

    while True:
        user_input = listen()
        if "cut it" in user_input:
            speak("Goodbye!, take care")
            break
        if "bye" in user_input:
            speak("Goodbye catch you later")
            break
        if "EXIT" in user_input:
            speak("Goodbye catch you later")
            break
        elif "reset chat" in user_input:
            chatStr = ""
        
        elif user_input:
            current_time = datetime.now().strftime("%H:%M:%S")
            if "time" in user_input:
                speak(f" The current time is {current_time}.")
        sites = [["instagram", "https://www.instagram.com"],["youtube", "https://www.youtube.com"],["wikipedia", "https://www.wikipedia.com"],["google", "https://www.google.com"]]        
        for site in sites:
         if f"open {site[0]}" in user_input:
            webbrowser.open(site[1])
            speak(f"Here you go buddy... opening{site[0]}")

        ai_response = get_gpt3_response(user_input)
        print("Fury:", ai_response)
        speak(ai_response)

            

                
            