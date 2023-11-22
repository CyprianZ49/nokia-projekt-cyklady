#graczy w sensie gry nazywami botami
from subprocess import Popen,PIPE,CREATE_NEW_CONSOLE
import shlex
from os import remove

class Bot:
    def __init__(self, name, prompt=None):
        self.prompt=prompt
        if prompt is None:
            try:
                with open(f'{name}.txt', 'x') as f:
                    pass
            except FileExistsError:
                pass
            self.proc=Popen(shlex.split(f"python terminalbot.py {name}"), creationflags=CREATE_NEW_CONSOLE)
        else:
            self.proc=Popen(shlex.split(prompt), stdin=PIPE, stdout=PIPE)
        self.name=name
        self.coins=0
        self.tempsoldiers=0
        self.tempfleets=0
        self.philosophers=0
        self.ownedTiles=[]
    def __hash__(self):
        return hash(self.name)
    def __eq__(self, other):
        return self.name==other.name
    def __ne__(self, other):
        return self.name!=other.name
    def get_move(self):
        if self.prompt is not None:
            return self.proc.stdout.readline().decode().split()
        #for testing only
        else:
            print(f'ruch gracza {self.name}')
            while True:
                f=open(f'{self.name}.txt', 'r')
                d=f.readline().strip().split()
                rest=f.read()
                if d!=[]:
                    print(d)
                    f.close()
                    with open(f'{self.name}.txt', 'w') as f:
                        f.write(rest)
                    return d
                f.close()
    def send_move(self,player,move):
        if self.prompt is not None:
            return self.proc.stdin.write(f"{player} {move}")

    def __del__(self):
        self.proc.kill()
        if self.prompt is None:
            remove(f'{self.name}.txt')


if __name__=='__main__':
    b = Bot("x")
    m=b.get_move()
    print(m)
