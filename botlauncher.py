import socket
from constants import host, port
from threading import Thread
import shlex
from sys import argv
import subprocess
import pathlib
import signal
import os
import platform

def terminate(*args):
    if platform.system() == 'Windows':
        os.kill(proc.pid, signal.CTRL_BREAK_EVENT)
    else:
        os.kill(proc.pid, signal.SIGKILL)
    os.kill(os.getpid(), signal.SIGTERM)

signal.signal(signal.SIGINT, terminate)
signal.signal(signal.SIGBREAK, terminate)

file = " ".join(argv[3:])
file_extension = pathlib.Path(file).suffix

if file_extension == '.py':
    prompt = f'python {file}'
else:
    prompt = file


if platform.system() == 'Windows':
    proc = subprocess.Popen(shlex.split(prompt), stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, bufsize=0)
else:
    proc = subprocess.Popen(shlex.split(prompt), stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, bufsize=0, start_new_session=True)

def handle_data(s):
    while True:
        try:
            proc.stdin.write(s.recv(1))
        except (ConnectionResetError, ConnectionAbortedError):
            break

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        Thread(target=handle_data, args=(s,)).start()
        s.sendall((argv[1]+'\n').encode())
        if argv[2]=='True':
            with open(f"testcases/{max(map(int,os.listdir('testcases')))}/{argv[1]}", 'wb') as f:
                while True:
                    data = proc.stdout.read(1)
                    s.send(data)
                    f.write(data)
                    f.flush()
        else:
            while True:
                data = proc.stdout.read(1)
                s.send(data)
except BaseException:
    pass
finally:
    terminate()