#graczy w sensie gry nazywami botami
from subprocess import Popen,CREATE_NEW_CONSOLE
import shlex
from server import Server
from constants import host, port

server = Server(host, port)

class Bot:
    def __init__(self, name, prompt=None):
        self.prompt=prompt
        if prompt is None:
            self.proc=Popen(shlex.split(f"python terminalbot.py {name}"), creationflags=CREATE_NEW_CONSOLE)
        elif prompt != '':
            self.proc=Popen(shlex.split(f"python botlauncher.py {name} {prompt}"))

        self.name=name
        self.coins=0
        self.soliderLimit=8
        self.fleetLimit=8
        self.philosophers=0
        self.priests=0
        self.ownedTiles=[]

    def __hash__(self):
        return hash(self.name)
    def __eq__(self, other):
        return self.name==other.name
    def __ne__(self, other):
        return self.name!=other.name
    def get_move(self):
        print(f'ruch {self.name}')
        while not server.data[self.name]:
            pass
        ret=server.data[self.name].pop(0).split()
        print(f"ruch to {ret}")
        return ret
    
    def send_move(self, player,move):
        server.senddata(self.name, f'{player} {move}')

    def __del__(self):
        if hasattr(self, 'proc'):
            self.proc.kill()