from sys import argv

print(f'gracz {argv[1]}')
while True:
    move=input()
    with open(f"{argv[1]}.txt", "a") as f:
        print(move, file=f)