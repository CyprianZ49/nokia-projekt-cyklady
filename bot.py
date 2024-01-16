#graczy w sensie gry nazywami botami
import shlex
from typing import Any
from server import Server
from constants import host, port, move_delay
from typing import Iterable
import time
import platform
from subprocess import Popen
if platform.system() == 'Windows':
    from subprocess import CREATE_NEW_CONSOLE, CREATE_NEW_PROCESS_GROUP

server = Server(host, port)

class Bot:
    def __init__(self, name, prompt=None, log=False):

        self.name=name
        self.coins= 0
        self.soliderLimit=8
        self.fleetLimit=8
        self.philosophers=0
        self.priests=0
        self.ownedTiles=[]
        self.prompt=prompt
        self.actionDiscount=0
        self.isBuildingMetropolis = False
        self.isFighting = False
        self.god = None
        self.terminal = False
        if prompt is None or prompt in ('t', 'terminal'):
            self.terminal = True
            if platform.system() == 'Windows':
                self.proc=Popen(shlex.split(f"python terminalbot.py {name} {log}"), creationflags=CREATE_NEW_CONSOLE|CREATE_NEW_PROCESS_GROUP)
            else:
                self.proc=Popen(shlex.split(f"python terminalbot.py {name} {log}"), shell=True)
        elif prompt != '':
            self.proc=Popen(shlex.split(f"python botlauncher.py {name} {log} {prompt}"))

    def __hash__(self):
        return hash(self.name)
    def __eq__(self, other):
        return self.name==other.name
    def __ne__(self, other):
        return self.name!=other.name
    def get_move(self):
        time.sleep(move_delay)
        print(f'ruch {self.name}')
        while not server.data[self.name]:
            pass
        ret=server.data[self.name].pop(0).split()
        print(f"ruch to {ret}")
        return ret
    
    def __repr__(self):
        return f'Bot({self.name})'

    def send_move(self, player, move):
        if not isinstance(move, str) and isinstance(move, Iterable):
            move = " ".join(map(str,move))
        print(f'sending to {self.name}:', player, move)
        server.senddata(self.name, f'{player} {move}')

    def __del__(self):
        if hasattr(self, 'proc'):
            self.proc.kill()