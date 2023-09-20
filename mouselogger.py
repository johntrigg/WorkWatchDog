from pynput.mouse import Listener
import time

# List to store recorded mouse clicks
clicks = []

# Function to record mouse clicks
def on_click(x, y, button, pressed):
    if pressed:
        clicks.append((x, y, button, time.time()))

# Start recording mouse clicks
print("Recording mouse clicks for 1 minute...")

# Record mouse clicks for 1 minute
start_time = time.time()
runTimeSeconds = 60
runTimeMinutes = runTimeSeconds / 60
end_time = start_time + runTimeSeconds  # 60 seconds = 1 minute

with Listener(on_click=on_click) as listener:
    try:
        while time.time() < end_time:
            pass
    except KeyboardInterrupt:
        pass

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

print("Recording completed.")

# Measure the amount of mouse clicks

# Open the key log file, and count the lines
with open('recorded_clicks.txt','r') as file:
   li = file.readlines()
clicksInLogFile = len(li)
print(f"Number of minutes that have passed since the log file started: {runTimeMinutes}")
print(f"Number of clicks in the log file: {clicksInLogFile}")
clicksPerMinute = clicksInLogFile
print(f"Number of clicks per minute: {clicksPerMinute}")
