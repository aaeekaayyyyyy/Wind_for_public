from datetime import datetime, timedelta
import time
import threading

from skills.utilities import speak

def tell_time():
    now = datetime.now()
    current_time = now.strftime("%I:%M %p")
    speak(f"The current time is {current_time}")

def start_timer(seconds):
    speak(f"Starting a timer for {seconds} seconds.")
    time.sleep(seconds)
    speak("Time's up!")

def set_alarm(hour, minute):
    now = datetime.now()
    alarm_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if alarm_time <= now:
        alarm_time += timedelta(days=1)  # Set for next day
    delay = (alarm_time - now).total_seconds()

    def alarm_thread():
        time.sleep(delay)
        speak("Alarm ringing!")

    threading.Thread(target=alarm_thread).start()
    speak(f"Alarm set for {hour}:{minute:02d}")