from simulation import game
from bot import Bot
from os import listdir
from random import setstate
from pickle import loads
from contextlib import redirect_stdout
from log import Log
from sys import exit

for test in listdir('testcases'):
    players = [Bot(i, f'filebot.py "testcases/{test}/{i}"') for i in range(5)]
    with open(f'testcases/{test}/out', 'br') as f:
        d=f.readline().rstrip()
        setstate(loads(eval(d)))
        output = f.read()
    with redirect_stdout(Log('tmp')):
        game(players)
    with open('tmp', 'r', encoding='utf-8') as f:
        if output.strip() != f.read().strip():
            print(f'Błąd w teście {test}')
            exit(1)

print('wszystko poprawnie')