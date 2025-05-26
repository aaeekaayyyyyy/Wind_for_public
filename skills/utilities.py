import uuid
from gtts import gTTS
import pygame
import time
import threading
import os
import speech_recognition as sr
from difflib import get_close_matches

def speak(text):
    # Function to convert text to speech
    def _speak():
        try:
            unique_filename = f"temp_{uuid.uuid4().hex}.mp3"
            tts = gTTS(text)
            tts.save(unique_filename)
            
            pygame.mixer.music.load(unique_filename)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

            # Delay cleanup to allow OS to release the file
            def cleanup():
                time.sleep(1.5)  # 1.5 seconds delay
                try:
                    if os.path.exists(unique_filename):
                        os.remove(unique_filename)
                except Exception as e:
                    print(f"[Cleanup Error] {e}")

            threading.Thread(target=cleanup).start()

        except Exception as e:
            print(f"[Speak Error] {e}")

    threading.Thread(target=_speak).start()
    

def recognize_speech(timeout=5, phrase_time_limit=4):
    # Function to recognize speech and return the recognized text
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


def is_wake_word(text, wake_word="hello"):
    matches = get_close_matches(wake_word, text.split(), cutoff=0.8)
    return wake_word in matches or wake_word in text

recognizer = sr.Recognizer()