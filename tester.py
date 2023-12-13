from simulation import game
from bot import Bot
from random import setstate
from pickle import loads
from contextlib import redirect_stdout
from log import Log
from sys import exit

test = '0'
players = [Bot(i, f'filebot.py "testcases/{test}/{i}"') for i in range(2)]
with open(f'testcases/{test}/out', 'r', encoding='utf-8') as f:
    d=f.readline().rstrip()
    setstate(loads(eval(d)))
    output = f.read()
with redirect_stdout(Log('tmp', False)):
    game(players, False)
with open('tmp', 'r', encoding='utf-8') as f:
    for num, lines in enumerate(zip(output.strip().splitlines(), f.read().strip().splitlines())):
        if lines[0]!=lines[1]:
            print(f'Błąd w teście {test} w linii {num}')
            exit(1)
print('wszystko poprawnie')