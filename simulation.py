from bot import Bot
from licytacja import Licytacja
from akcje import *
from random import shuffle
from przygotowanie import earnings
from traceback import print_exception

def game():
    board = Plansza()
    players = [Bot(i) for i in range(2)] #zmiana na więcej graczy
    gods = {'ze':Zeus(board),'at':Athena(board),'ap':Apollo(board),'ar':Ares(board),'po':Poseidon(board)}
    while True:
        players = turn(players,gods)
        print(players)
        
def turn(players, gods):
    print('faza produkcji')
    for p in players: # zmiana na faktyczną produkcję
        p.coins+=5
    print('początek licytacji')
    lic = Licytacja(players)
    licres=lic.perform()
    print('koniec licytacji')
    print(licres)
    order=[]
    p_to_god={}
    for god,p in licres.items():
        if god=='ap':
            for player in p:
                p_to_god[players[player]] = gods['ap']
                order.append(players[player])
        else:
            if p[1]!=-1:
                p_to_god[players[p[1]]] = gods[god]
                order.append(players[p[1]])
                players[p[1]].coins-=p[0]

    print('początek akcji')
    name_to_f = {'r':'rekrutuj','b':'buduj','m':'ruch'}
    for player in order:
        action = player.get_move()
        while action[0]!='p':
            god = p_to_god[player]
            try:
                if god is gods['ap']:
                    god.praise(player,*action[1:])
                else:
                    f=name_to_f[action[0]]
                    getattr(god, f)(player,*action[1:])
            except Exception as e:
                print_exception(e)
            action = player.get_move()
        print(f'gracz {player.name} pasuje')

    reset(*gods.values())
    order.reverse()
    return order

if __name__ == "__main__":
    game()