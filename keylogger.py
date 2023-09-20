from pynput.keyboard import Key, Listener
import datetime
import logging
import time
import os

keys_information = "key_log.txt"

# We have each time iteration be 60 seconds. At the end of this time iteration, the file will be written to, as well as other features
iterationTimeSeconds = 60

# Initialize the number of iterations for loop control
numberOfIterations = 0

# The number of iterations we will end after.
number_of_iterations_end = 1

# Expected runtime in seconds
totalExpectedTimeSeconds = iterationTimeSeconds*number_of_iterations_end
totalExpectedTimeMinutes = totalExpectedTimeSeconds / 60

# Grab current time the keylogger is launched
currentTime = time.time()

# Grab the stopping time, ie when we want the iteration to end.
stoppingTime = time.time() + iterationTimeSeconds

# Timer control loop. The timer will end after x iterations, where each iteration is y seconds. For measurement purposes, each iteration is a minute, and we will stop after 1 interation for now.
while numberOfIterations < number_of_iterations_end:

    count = 0
    keys =[]

    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys =[]

    def write_file(keys):
        with open(keys_information, "a") as f:
            for key in keys:
                # Get rid of single quotes for beautification
                k = str(key).replace("'", "") 
                # Replace spaces with newlines, so every word is on its own line
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()

    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        # print("Recording keyboard input")
        listener.join()

    if currentTime > stoppingTime:
        numberOfIterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + iterationTimeSeconds

# At this point, the loop has stopped, and we need to count the number of lines in the log file, and get our words typed from that, and our estimated runtime in minutes from earlier variables

# Open the key log file, and count the lines
with open('key_log.txt','r') as file:
   li = file.readlines()
wordsInLogFile = len(li)
print(f"Number of minutes that have passed since the log file started: {totalExpectedTimeMinutes}")
print(f"Number of words in the log file: {wordsInLogFile}")
wordsPerMinute = wordsInLogFile
print(f"Number of words per minute: {wordsPerMinute}")
