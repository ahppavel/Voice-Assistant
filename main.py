import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import subprocess
import requests
from data import apps, pages, songs
from key import WEATHER_API_KEY, NEWS_API_KEY

# Configuration

wake_words = ["hi", "hello"]
stop_words = ["stop", "exit"]

# Text-to-Speech 

def speak(text):
    print(f"Assistant: {text}")
    engine = pyttsx3.init()
    engine.setProperty("rate", 180)
    engine.say(text)
    engine.runAndWait()

# Listen to user

def listen():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("Assistant: Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5,phrase_time_limit=5)
    try:
        command = recognizer.recognize_google(audio).lower().strip()
        print(f"You: {command}")
        return command
    except:
        print("Assistant: Sorry, Again Please.")
        return ""
    
    
# weather
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    try:
        data = requests.get(url).json()
        if data.get("cod") != 200:
            speak("City not found")
            return
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        speak(f"The temperature in {city} is {temp}°C with {desc}")
    except:
        speak("Sorry,I cannot get the weather.")

# news

def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    try:
        data = requests.get(url).json()
        articles = data.get("articles", [])[:5]
        if not articles:
            speak("No news found")
            return
        speak("Here are today's top news")
        for a in articles:
            speak(a["title"])
    except:
        speak("Sorry,I cannot fetch the news.")

#  Open App 

def open_app():
    speak("Which app?")
    app_name = listen()
    if not app_name:
        speak("I did not hear the app name.")
        return

    # shortcut 1st
    if app_name in apps:
        try:
            os.startfile(apps[app_name])
            speak(f"Opening {app_name}")
            return
        except Exception as e:
            print(e)
            speak(f"Failed to open {app_name}")

    # Windows start command
    try:
        subprocess.Popen(f'start {app_name}', shell=True)
        speak(f"Opening {app_name}")
    except Exception as e:
        print(e)
        speak("Sorry,again please.")

# limited apps

# def open_app(): 
#     speak("Which app?") 
#     app_name = listen()
#     if app_name in apps: 
#         os.startfile(apps[app_name]) 
#         speak(f"Opening {app_name}") 
#     else: 
#         try: 
#             os.startfile(app_name)
#             speak(f"Opening {app_name}")
#         except: 
#             speak(f"Cannot find {app_name}")


#  Open Site
 
def open_page():
    speak("Which site?")
    page_name = listen()
    if page_name in pages:
        webbrowser.open(pages[page_name])
        speak(f"Opening {page_name}")
    else:
        webbrowser.open(f"https://www.google.com/search?q={page_name}")
        speak(f"Searching {page_name} online")

# Play Song

def play_song():
    speak("Which song?")
    song_name = listen()
    if song_name in songs:
        webbrowser.open(songs[song_name])
        speak(f"Playing {song_name}")
    else:
        webbrowser.open(f"https://www.youtube.com/results?search_query={song_name}")
        speak(f"Searching...{song_name} on youtube")

#  Main Assistant

def assistant():
    speak("Say hi or hello to wake me up.")

    while True:
        command = listen()
        if any(word in command for word in wake_words):
            speak("Hi! How can I help you?")
            break

    while True:
        command = listen()
        if any(word in command for word in stop_words):
            speak("Goodbye!")
            break
        elif "weather" in command:
            speak("Which city?")
            city = listen()
            get_weather(city)

        elif "news" in command or "top news" in command:
            get_news()

        elif "open apps" in command:
            open_app()
        elif "open page" in command:
            open_page()
        elif "play song" in command or "play music" in command:
            play_song()
        else:
            speak("Sorry,Please try again.")
            
#runnnnnnnnnnnnnnnnnn.............

if __name__ == "__main__":
    assistant()
