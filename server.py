import socket
from threading import Thread
from collections import defaultdict

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.data = defaultdict(list)
        self.clients = {}
        Thread(target=self.run, daemon=True).start()

    def getline(self, client):
        line=''
        data=client.recv(1).decode()
        while data!='\n':
            line+=data
            data=client.recv(1).decode()
        return line

    def senddata(self, name, data):
        while not name in self.clients:
            pass
        self.clients[name].sendall((data+'\n').encode())

    def handle_client(self, client):
        name = int(self.getline(client))
        self.clients[name] = client
        while True:
            self.data[name].append(self.getline(client))

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            while True:
                client, address = s.accept()
                Thread(target=self.handle_client, args=(client,), daemon=True).start()