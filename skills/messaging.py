import subprocess
import time
import pygetwindow as gw
import pyautogui

def launch_whatsapp():
    try:
        subprocess.Popen(
            ["powershell", "start shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App"],
            shell=True
        )
        print("WhatsApp launched.")
    except Exception as e:
        print("Error launching WhatsApp:", e)


last_contact = None  # Track last contact globally

def send_whatsapp_message(command):
    global last_contact
    try:
        if "send message to" in command and "saying" in command:
            parts = command.split("send message to")[1].strip().split("saying")
            contact_name = parts[0].strip()
            message = parts[1].strip()
        else:
            print("Please say 'send message to [name] saying [message]'.")
            return

        print(f"Sending message to {contact_name}")
        launch_whatsapp()
        time.sleep(7)

        # Focus WhatsApp window
        windows = gw.getWindowsWithTitle("WhatsApp")
        if windows:
            windows[0].activate()
            time.sleep(1)
        else:
            print("Could not find WhatsApp window.")
            return

        # If same contact as before, skip search
        if last_contact and contact_name.lower() == last_contact.lower():
            pyautogui.write(message, interval=0.05)
            pyautogui.press('enter')
            print("Message sent.")
            return

        # Trigger search with Ctrl+F
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(1)
        pyautogui.write(contact_name, interval=0.1)
        time.sleep(2)

        pyautogui.press('down')
        pyautogui.press('enter')
        time.sleep(1.5)

        pyautogui.write(message, interval=0.05)
        pyautogui.press('enter')
        print("Message sent.")
        last_contact = contact_name  # Update for next time

    except Exception as e:
        print("WhatsApp Error:", e)
        print("Something went wrong.")