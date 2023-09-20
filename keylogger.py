from pynput.keyboard import Key, Listener

import time
import os

keys_information = "key_log.txt"

keys_information_e = "e_key_log.txt"

file_path = "" # Enter the file path you want your files to be saved to
extend = ""
file_merge = file_path + extend

# We have each time iteration be 60 seconds. At the end of this time iteration, the file will be written to, as well as other features
time_iteration = 60

number_of_iterations = 0

# The number of iterations we will end after.
number_of_iterations_end = 1

totalExpectedTimeSeconds = time_iteration*number_of_iterations_end
totalExpectedTimeMinutes = totalExpectedTimeSeconds / 60


# Grab current time the keylogger is launched
currentTime = time.time()

# Grab the stopping time, ie when we want the iteration to end.
stoppingTime = time.time() + time_iteration

# Timer control loop. The timer will end after x iterations, where each iteration is y seconds. For measurement purposes, each iteration is a minute, and we will stop after 1 interation for now.
while number_of_iterations < number_of_iterations_end:

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
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
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
        listener.join()

    if currentTime > stoppingTime:

        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration

# This is a bunch of sample test texst for testing the keylogger its actually really difficult to type like this since im not very good at making things up

# At this point, the loop has stopped, and we need to count the number of characters in the file, and try to get our WPM from that.

with open('key_log.txt','r') as file:
   li = file.readlines()
total_line = len(li)
print(f"Number of words in the log file: {total_line}")
print(f"Number of minutes that have passed since the log file started: {totalExpectedTimeMinutes}")
measuredWPM = total_line // totalExpectedTimeMinutes    
print(f"Measured words per minute: {totalExpectedTimeMinutes}")
