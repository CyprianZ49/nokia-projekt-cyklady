#graczy w sensie gry nazywami botami
from subprocess import Popen,PIPE,CREATE_NEW_CONSOLE
import shlex
class Bot:
    def __init__(self, name, prompt=None):
        self.prompt=prompt
        if prompt is None:
            self.proc=Popen(shlex.split("python terminalbot.py"), stdout=PIPE, creationflags=CREATE_NEW_CONSOLE)
        else:
            self.proc=Popen(shlex.split(prompt), stdin=PIPE, stdout=PIPE)
        self.name=name
        self.coins=0
        self.tempsoldiers=0
        self.tempfleet=0
        self.philosophers=0
        self.ownedTiles=set()
    def __hash__(self):
        return hash(self.name)
    def get_move(self):
        return self.proc.stdout.readline().decode().split()
    def send_move(self,player,move):
        if self.prompt is not None:
            return self.proc.stdin.write(f"{player} {move}")

if __name__=='__main__':
    b = Bot("x")
    m=b.get_move()
    print(m)
