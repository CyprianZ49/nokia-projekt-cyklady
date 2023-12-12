import socket
from constants import host, port
from threading import Thread
import shlex
from sys import argv
from subprocess import Popen,PIPE

proc = Popen(shlex.split(f'python {" ".join(argv[2:])}'), stdin=PIPE, stdout=PIPE)

def handle_data(s):
    while True:
        proc.stdin.write(s.recv(1))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    Thread(target=handle_data, args=(s,)).start()
    s.sendall((argv[1]+'\n').encode())
    while True:
        s.send(proc.stdout.read(1))