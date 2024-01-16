import socket
from constants import host, port
from threading import Thread
import shlex
from sys import argv
from subprocess import Popen,PIPE
import pathlib
import signal
import os

def terminate(*args):
    print('killing')
    proc.terminate()
    os.kill(os.getpid(), signal.SIGTERM)

signal.signal(signal.SIGINT, terminate)

file = " ".join(argv[3:])
file_extension = pathlib.Path(file).suffix

if file_extension == '.py':
    prompt = f'python {file}'
else:
    prompt = file

proc = Popen(shlex.split(prompt), stdin=PIPE, stdout=PIPE, bufsize=0)

def handle_data(s):
    while True:
        proc.stdin.write(s.recv(1))

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        Thread(target=handle_data, args=(s,)).start()
        s.sendall((argv[1]+'\n').encode())
        with open(f"testcases/{max(map(int,os.listdir('testcases')))}/{argv[1]}", 'wb') as f:
            while True:
                data = proc.stdout.read(1)
                s.send(data)
                f.write(data)
                f.flush()
finally:
    terminate()