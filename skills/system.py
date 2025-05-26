import subprocess
import pyautogui

def set_volume(level):  # 0-100
    devices = ctypes.windll.user32
    # Requires pycaw for more advanced control
    speak(f"Setting volume to {level} percent")
    # Here you could use `pycaw` for more precise control
    for _ in range(50): pyautogui.press("volumedown")
    for _ in range(level // 2): pyautogui.press("volumeup")

def set_brightness(level):  # 0-100
    try:
        sbc.set_brightness(level)
        speak(f"Setting brightness to {level} percent")
    except Exception as e:
        speak("Could not set brightness.")
        print(f"[Brightness Control Error] {e}")

def toggle_wifi(state):  # state = "on" or "off"
    try:
        command = f'netsh interface set interface name="Wi-Fi" admin={state}'
        subprocess.run(command, shell=True)
        speak(f"Wi-Fi turned {state}")
    except Exception as e:
        speak("Failed to toggle Wi-Fi.")
        print("Wi-Fi toggle error:", e)

def toggle_bluetooth(state):  # state = "on" or "off"
    try:
        subprocess.run(f"powershell -Command \"(Get-Service bthserv).Status\"", shell=True)
        command = f"powershell -Command \"Start-Process 'ms-settings:bluetooth'\""
        subprocess.Popen(command, shell=True)
        speak(f"Bluetooth window opened. Please turn it {state} manually.")
    except Exception as e:
        speak("Bluetooth control failed.")
        print("Bluetooth error:", e)

def shutdown():
    speak("Shutting down the system.")
    os.system("shutdown /s /t 1")

def restart():
    speak("Restarting the system.")
    os.system("shutdown /r /t 1")

def lock_system():
    speak("Locking the system.")
    os.system("rundll32.exe user32.dll,LockWorkStation")