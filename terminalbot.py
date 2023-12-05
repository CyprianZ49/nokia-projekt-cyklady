import socket
from constants import host, port
from threading import Thread
from sys import argv

print(f'gracz {argv[1]}')

def handle_data(s):
    while True:
        data=s.recv(1).decode()
        print(data, end='')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    with open(f'testcases/{argv[1]}', 'w') as f:
        s.connect((host, port))
        Thread(target=handle_data, args=(s,)).start()
        s.sendall((argv[1]+'\n').encode())
        while True:
            inp=input()
            f.write(inp+'\n')
            f.flush()
            s.sendall((inp+'\n').encode())