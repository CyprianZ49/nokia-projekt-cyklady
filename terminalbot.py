from sys import argv
from threading import Thread

print(f'gracz {argv[1]}')

try:
    with open(f'{argv[1]}.in', 'x') as f:
        pass
except FileExistsError:
    pass

def print_data():
    while True:
        f=open(f'{argv[1]}.in', 'r')
        d=f.readline().strip().split()
        rest=f.read()
        if d!=[]:
            print(d)
            f.close()
            with open(f'{argv[1]}.in', 'w') as f:
                f.write(rest)
        f.close()

Thread(target=print_data).start()

while True:
    move=input()
    with open(f"{argv[1]}.out", "a") as f:
        print(move, file=f)