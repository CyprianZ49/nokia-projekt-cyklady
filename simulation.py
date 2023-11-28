from bot import Bot
from licytacja import Licytacja
from akcje import *
from random import shuffle
from traceback import print_exception

def game():
    players = [Bot(i) for i in range(2)] #zmiana na więcej graczy
    pusty = Bot(-1, prompt='where') #coś tu jest jakieś takie niefajne
    board = Plansza(pusty)
    board.generateBoard()
    for x in range(13):
        for y in range(13):
            if board.pola[x][y].typ=='capital' or board.pola[x][y].typ=='water':
                pusty.ownedTiles.append((x, y))
    board.changeOwnership(3, 3, players[0])
    board.changeOwnership(2, 4, players[0])
    shuffle(players)
    gods = {'ze':Zeus(board),'at':Athena(board),'ap':Apollo(board),'ar':Ares(board),'po':Poseidon(board)}
    while True:
        players = turn(players,gods, board)
        wygrani = []
        for player in players:
            k = 0
            for tile in player.ownedTiles:
                if board.pola[tile[0]][tile[1]].typ=='capital' and board.pola[tile[0]][tile[1]].isMetropolis:
                    k+=1
            if k>=2:
                wygrani.append(player)
        maks = 0
        for player in wygrani:
            maks = max(maks, player.coins)
        wygraniForReal = []
        for player in wygrani:
            if player.coins==maks:
                wygraniForReal.append(player)
        if len(wygraniForReal)>0:
            print("rozgrywka zakonczyla się!\nUltymatywny Grek:")
            for player in wygraniForReal:
                print(f"{player.name}")
            break
        print(players)

        
def turn(players, gods, board):
    print('produkcja')
    for kto in players:
        kto.coins+=9 # test only
        for wys in kto.ownedTiles:
            kto.coins+=board.pola[wys[0]][wys[1]].value
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
                players[p[1]].coins-=max(p[0]-players[p[1]].priests, 1)

    print('początek akcji')
    name_to_f = {'r':'rekrutuj','b':'buduj','m':'ruch'}
    for player in order:
        action = player.get_move()
        while action[0]!='p':
            god = p_to_god[player]
            try:
                if god is gods['ap']:
                    god.praise(player,*map(int, action[1:]))
                else:
                    f=name_to_f[action[0]]
                    getattr(god, f)(player,*map(int, action[1:]))
            except Exception as e:
                print_exception(e)
            Metropolizacja(board, player)
            action = player.get_move()
        print(f'gracz {player.name} pasuje')
    print('koniec tury')
    reset(*gods.values())
    order.reverse()
    return order

if __name__ == "__main__":
    game()