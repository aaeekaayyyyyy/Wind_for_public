import webbrowser
import speech_recognition as sr
import threading
from skills.ai import aiProcess
from skills.calendar import google_calendar_authenticate, add_event_to_calendar, get_next_event
from skills.clock import tell_time, start_timer, set_alarm
from skills.controls import set_volume, set_brightness, toggle_wifi, toggle_bluetooth, shutdown, restart, lock_system
from skills.messaging import launch_whatsapp, send_whatsapp_message
from skills.music import launch_spotify, control_spotify
import re
import os
import subprocess
import requests
import datetime
from googleapiclient.discovery import build

# Define your News API key here
newsapi = "your_news_api_key"

from skills.utilities import speak

def recognize_speech(timeout=5, phrase_time_limit=4):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for noise...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text.lower()
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"Speech Recognition API error: {e}")
    return ""

def open_notepad():
    raise NotImplementedError

def processCommand(c):
    c = c.lower()
    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
    elif "open spotify" in c:
        launch_spotify()
    elif "play music" in c or "resume music" in c or "play" in c:
        control_spotify("play")
    elif "pause music" in c or "pause" in c or "stop" in c:
        control_spotify("pause")
    elif "next song" in c:
        control_spotify("next")
    elif "previous song" in c:
        control_spotify("previous")
    elif "set volume to" in c:
        level = int(c.split("set volume to")[1].strip().replace("%", ""))
        set_volume(level)
    elif "what's the time" in c or "tell me the time" in c:
        tell_time()
    elif "start timer for" in c:
        match = re.search(r'start timer for (\d+)\s?(second|seconds|minute|minutes)?', c)
        if match:
            value = int(match.group(1))
            unit = match.group(2)
            if unit and "minute" in unit:
                seconds = value * 60
            else:
                seconds = value
            start_timer(seconds)
        else:
            speak("Please specify the timer duration like 'start timer for 5 minutes'.")
    elif "set alarm for" in c:
        match = re.search(r'set alarm for (\d{1,2}):(\d{2})', c)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2))
            set_alarm(hour, minute)
        else:
            speak("Please say the time in the format: set alarm for HH:MM.")
    elif "open timer" in c or "open alarm" in c or "open clock" in c:
        speak("Opening the clock application is not implemented yet.")
    elif "set brightness to" in c:
        level = int(c.split("set brightness to")[1].strip().replace("%", ""))
        set_brightness(level)
    elif "turn off wifi" in c:
        toggle_wifi("disable")
    elif "turn on wifi" in c:
        toggle_wifi("enable")
    elif "turn off bluetooth" in c:
        toggle_bluetooth("off")
    elif "turn on bluetooth" in c:
        toggle_bluetooth("on")
    elif "open camera" in c:
        subprocess.Popen("start microsoft.windows.camera:", shell=True)
        speak("Camera opened.")
    elif "shutdown" in c:
        shutdown()
    elif "restart" in c:
        restart()
    elif "lock system" in c:
        lock_system()
    elif "open notepad" in c:
        open_notepad()
    elif "open whatsapp" in c:
        launch_whatsapp()
    elif "send message to" in c and "saying" in c:
        send_whatsapp_message(c)
    elif "news" in c:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            articles = r.json().get('articles', [])
            for article in articles[:5]:
                speak(article['title'])
        else:
            speak("Failed to fetch news.")
    elif "add event to my calendar" in c:
        if calendar_service is None:
            speak("Google Calendar service is not available.")
            return
        speak("What is the title of the event?")
        title = recognize_speech()
        if not title:
            speak("Event title not recognized.")
            return
        speak("When is the event?")
        datetime_str = recognize_speech()
        if not datetime_str:
            speak("Event time not recognized.")
            return
        try:
            event_start = datetime.datetime.strptime(datetime_str, '%B %d at %I %p')
            now = datetime.datetime.now()
            event_start = event_start.replace(year=now.year)
            if event_start < now:
                event_start = event_start.replace(year=now.year + 1)
            event_end = event_start + datetime.timedelta(hours=1)
        except Exception as e:
            speak("Sorry, I couldn't understand the date and time.")
            return
        
        link = add_event_to_calendar(calendar_service, title, event_start, event_end)
        speak(f"Event '{title}' added to your calendar. You can view it here: {link}")
    elif "show my next event" in c or "what is my next event" in c:
        if calendar_service is None:
            speak("Google Calendar service is not available.")
            return
        event = get_next_event(calendar_service)
        if event is None:
            speak("You have no upcoming events.")
        else:
            summary, start = event
            speak(f"Your next event is {summary} at {start}")
    else:
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Wind...")
    wind_active = False

    try:
        creds = google_calendar_authenticate()
        calendar_service = build('calendar', 'v3', credentials=creds)
    except Exception as e:
        calendar_service = None
        print("[Google Calendar Setup Error]:", e)

    while True:
        try:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)

                if not wind_active:
                    print("Listening for wake word...")
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=3)
                    trigger = recognizer.recognize_google(audio)
                    print("Recognized:", trigger)

                    if "hello" in trigger.lower():
                        wind_active = True
                        speak("I'm listening.")
                    continue

                print("Waiting for command...")
                audio = recognizer.listen(source, timeout=20, phrase_time_limit=7)
                command = recognizer.recognize_google(audio)
                print("Recognized Command:", command)

                if "stop listening" in command or "goodbye" in command:
                    speak("Okay, going to sleep.")
                    wind_active = False
                    continue

                processCommand(command)

        except sr.WaitTimeoutError:
            print("Timeout: No input detected.")
            if wind_active:
                speak("Still here if you need me.")
        except sr.UnknownValueError:
            print("Could not understand audio.")
            if wind_active:
                speak("I didn't get that.")
        except Exception as e:
            print("Unexpected error:", e)