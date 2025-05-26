import subprocess
import pyautogui

def launch_spotify():
    try:
        subprocess.Popen("start spotify", shell=True)
        speak("Spotify launched.")
    except Exception as e:
        speak("Could not open Spotify.")
        print("Spotify launch error:", e)

def control_spotify(action):
    try:
        if action == "play" or action == "pause":
            pyautogui.press("playpause")
        elif action == "next":
            pyautogui.press("nexttrack")
        elif action == "previous":
            pyautogui.press("prevtrack")
        else:
            speak(f"Unknown action: {action}")
    except Exception as e:
        speak(f"Could not perform the {action} action.")
        print(f"[Spotify Control Error] {e}")