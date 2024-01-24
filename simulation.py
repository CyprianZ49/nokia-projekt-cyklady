from licytacja import Licytacja
from akcje import *
from custom_rand import random
from traceback import print_exception
import tkinter as tk
from przygotowanie import przypiszWarunkiStartowe
from threading import Thread,Condition
from traceback import print_exc
import os
from contextlib import redirect_stdout
from log import Log
from random import getstate, setstate
from ast import literal_eval
import copy
import argparse
from sys import argv, stdout
from plansza import Plansza
from bot import Bot
import signal
from legalMoves import *
import platform

def game(players, visual = True):
    pusty = Bot(-1, prompt='') #coś tu jest jakieś takie niefajne
    board = Plansza(pusty)
    board.generateBoard()
    for x in range(13):
        for y in range(13):
            if board.pola[x][y].typ=='capital' or board.pola[x][y].typ=='water':
                pusty.ownedTiles.append((x, y))
    random.shuffle(players)
    print(players)
    order = [player.name for player in players]

    for player in players:
        player.send_move(-1, player.name) #który gracz
        player.send_move(-1,order) #kolejność
    przypiszWarunkiStartowe(board, players, len(players))
    gods = {'ze':Zeus(board),'at':Athena(board),'ap':Apollo(board),'ar':Ares(board),'po':Poseidon(board)}


    if visual: #banish pygame
        import visualization.main
        from visualization.main import start_visualization
        th = Thread(target=start_visualization,args=(board,players))
        th.start()


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
            print("The game has ended!\nThe winner(s) is/are:")
            for player in wygraniForReal:
                print(f"{player.name}")
            break
        print(players)

        
def turn(players, gods, board):
    print('production')
    for kto in players:
        for wys in kto.ownedTiles:
            kto.coins+=board.pola[wys[0]][wys[1]].value
    for kto in players:
        kto.actionDiscount=0
        for wys in kto.ownedTiles:
            if board.pola[wys[0]][wys[1]].typ=='capital':
                if board.pola[wys[0]][wys[1]].isMetropolis:
                    kto.actionDiscount+=1
                for bud in board.pola[wys[0]][wys[1]].buildings:
                    if bud == 2:
                        kto.actionDiscount+=1
    print('bidding phase begins')
    lic = Licytacja(players)
    licres=lic.perform()
    print('bidding phase ends')
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

    print('action phase begins')
    name_to_f = {'r':'rekrutuj','b':'buduj','m':'ruch'}
    for player in order:
        board.turn = player
        legal = getLegalMoves(board, player, gods)
        if player.skipping:
            action = ["p"]
        else:
            action = player.get_move()
        move =  " ".join(action)
        print(move)
        print(legal)
        while move not in legal:
            player.increment_errors()
            player.send_move(-3, "InvalidMoveError")
            if player.skipping:
                action = ["p"]
            else:
                action = player.get_move()
            move =  " ".join(action)
            
        while action[0]!='p':
            god = p_to_god[player]
            try:
                if god is gods['ap'] and action[0]!='l':
                    god.praise(player,*map(int, action[1:]))
                else:
                    f=name_to_f[action[0]]
                    getattr(god, f)(player,*map(int, action[1:]))
            except Exception as e:
                player.increment_errors()
                player.send_move(-3, type(e).__name__)
                print(god, move, player.god)
                # print_exception(e)
                raise
            else:
                player.send_move(-5, "ok")
            Metropolizacja(board, player)
            legal = getLegalMoves(board, player, gods)
            if player.skipping:
                action = ["p"]
            else:
                action = player.get_move()
            move =  " ".join(action)
            print(move)
            print(legal)
            if move not in legal:
                raise InvalidMoveError
        print(f'gracz {player.name} pasuje')
    print('turn ends')
    reset(*gods.values())
    order.reverse()
    return order

def init_bots(files, log):
    return [Bot(i, p, log) for i,p in enumerate(files)] if files else [Bot(i, None, log) for i in range(2)]

def terminate(*args):
    for player in players:
        try:
            if platform.system() == 'Windows':
                if player.terminal:
                    os.kill(player.proc.pid, signal.SIGTERM)
                else:
                    os.kill(player.proc.pid, signal.CTRL_BREAK_EVENT)
            else:
                os.kill(player.proc.pid, signal.SIGKILL)
        except PermissionError:
            pass
    os.kill(os.getpid(), signal.SIGTERM)
    
signal.signal(signal.SIGINT, terminate)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Launch arena with bots.')
    parser.add_argument('--bots', nargs='*', dest="files", action="store",
                        help='file paths to be used for bots', required=False)
    parser.add_argument('--rng', dest="rng", action="store",
                help='file to read rng state from', required=False)
    parser.add_argument('--rng2', dest="rng2", action="store",
            help='file to read rng state from', required=False)
    parser.add_argument('--log', dest="log", action="store_true",
            help='specifies that output should be stored as a log', required=False)
    parser.add_argument('-v', dest="visual", action="store_false",
                    help='if specified lauches without visuals', required=False)
    
    nspc = parser.parse_args(argv[1:])
    # exit(0)
    
    random.load(nspc.rng2)

    if nspc.rng:
        with open(nspc.rng, 'r') as f:
            setstate(literal_eval(f.read()))

    if nspc.log:
        if not os.path.exists('testcases'):
            n=0
        else:
            n=max(map(int,os.listdir('testcases')))+1
        os.makedirs(f'testcases/{n}')

        with open(f'testcases/{n}/rng', 'w') as f:
            f.write(str(getstate()))
        log = Log(f'testcases/{n}/out')
    try:
        with redirect_stdout(log if nspc.log else stdout):
            players = init_bots(nspc.files, nspc.log)
            print(len(players))
            game(players, nspc.visual)
            # while True:
            #     pass
    except BaseException as e:
        print_exception(e)
    finally:
        terminate()