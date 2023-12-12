import socket
from constants import host, port, debug
from threading import Thread
from sys import argv, stdout
import os
from traceback import print_exception

print(f'gracz {argv[1]}')

def handle_data(s):
    while True:
        data=s.recv(1).decode()
        print(data, end='')

def main(f):
    s.connect((host, port))
    Thread(target=handle_data, args=(s,)).start()
    s.sendall((argv[1]+'\n').encode())
    while True:
        inp=input()
        print(inp, file=f, flush=True)
        s.sendall((inp+'\n').encode())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        if debug:
            with open(f"testcases/{max(map(int,os.listdir('testcases')))}/{argv[1]}", 'w') as f:
                main(f)
        else:
            main(stdout)
    except Exception as e:
        print_exception(e)
        while True:
            pass