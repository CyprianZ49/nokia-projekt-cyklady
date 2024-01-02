from typing import Any
import pygame
import math
import random
import plansza
from bot import Bot
import sys
import tkinter as tk
# from OpenGL.GL import *
from pygame.locals import *
# from OpenGL.GLU import *
from visualization.warrior import Warrior
from visualization.globals import *
from visualization.university import University
from visualization.draw_and_conv import *
from visualization.ship import Ship
from visualization.coin import Coin
from visualization.temple import Temple
from visualization.fort import Fort
from visualization.port import Port


def render_board(package,board,screen):
    odwiedzone = {}
    poczatkowy_srodek,promien = package
    for warrior in sprites:
        warrior.kill()
    def draw_island(x,y,budynki,centre,radius):
        # print(len(budynki))
        draw_hexagon(centre,radius,"brown",screen)
        if len(budynki)==1:
            for x in budynki:
                if x == 1:
                    sprites.add(University(centre,radius,0))
                if x == 2:
                    sprites.add(Temple(centre,radius,0))
                if x == 3:
                    sprites.add(Fort(centre,radius,0))
                if x == 4:
                    sprites.add(Port(centre,radius,0))
        else:
            ktory_budynek = 1
            for x in budynki:
                if x == 1:
                    sprites.add(University(centre,radius,ktory_budynek))
                    ktory_budynek+=1
                if x == 2:
                    sprites.add(Temple(centre,radius,ktory_budynek))
                    ktory_budynek+=1
                if x == 3:
                    sprites.add(Fort(centre,radius,ktory_budynek))
                    ktory_budynek+=1
                if x == 4:
                    sprites.add(Port(centre,radius,ktory_budynek))
                    ktory_budynek+=1
                if ktory_budynek>2:#ten if sluzy do testowania!!!
                    break

    def handle_islands(capitalx,capitaly,pola,budynki,centre,radius):
        if [capitalx,capitaly] in pola:
            pola.remove([capitalx,capitaly])
        
        while 0 in budynki:
            budynki.remove(0)
        


        for i in range(len(pola)):
            ile = math.ceil(len(budynki)/(len(pola)-i))
            island_centre = centre
            # print(island_centre)
            polex,poley=pola[i][0],pola[i][1]
            if poley > capitaly:
                for _ in range(poley-capitaly):
                    island_centre=konw(island_centre,radius,1)
                polex-=poley-capitaly
            if polex > capitalx:
                for _ in range(polex-capitalx):
                    island_centre=konw(island_centre,radius,2)
            if polex < capitalx:
                for _ in range(capitalx-polex):
                    island_centre=konw(island_centre,radius,5)
            if poley < capitaly:
                for _ in range(capitaly-poley):
                    island_centre=konw(island_centre,radius,3)
            
            # print(len(budynki[0:ile]),len(budynki),len(pola))
            draw_island(polex,poley,budynki[0:ile] if ile!=0 else [],island_centre,radius)
            for _ in range(ile):
                budynki.pop(0)

            
        # print(capitalx,capitaly,pola)
    
    def handle_capital(x,y,pola, budynki,sila,value,centre,radius,imie,czy_solo_stolica):
        # if sila>0:
        #     sprites.add(Warrior(centre,radius,imie))
        while 0 in budynki:
            budynki.remove(0)

        if value>0:
            if (x,y) not in ktory_wyglad_monety:
                ktory_wyglad_monety[(x,y)]=random.randint(1,2)
            sprites.add(Coin(centre,radius,ktory_wyglad_monety[(x,y)]))
        
        # print(czy_solo_stolica,value,sila)
        if czy_solo_stolica:
            # entity = budynki+['moneta','zolnierz']
            if len(budynki)==0:
                if value==0:
                    if sila>0:
                        sprites.add(Warrior(centre,radius,imie,0))# solo warrior
                else:
                    if sila>0:
                        sprites.add(Warrior(centre,radius,imie,1))# warrior i moneta
            else:
                if value==0:
                    if sila>0:
                        sprites.add(Warrior(centre,radius,imie,3))#budynek i warrior, TEN CASE NIGDY NIE  ZACHODZI, A ZOSTAWIAM GO DLA WIDOCZNOSCI
                else:
                    if sila>0:
                        sprites.add(Warrior(centre,radius,imie,2))#budynek, moneta i warrior
                
        else:#przypadek w ktorym istnieja inne pola wyspy i na nich sa wszystkie budynki
            if value==0:
                if sila>0:
                    sprites.add(Warrior(centre,radius,imie,0)) # tylko zolnierz
            else:
                if sila>0:
                    sprites.add(Warrior(centre,radius,imie,1))# zolnierz i moneta

        

    def crawl(x,y,centre,radius,board):
        #print(board.pola[x][y]==plansza.Water)
        if (x,y) not in odwiedzone:
            #print(x,y)
            odwiedzone[(x,y)]=True
            if isinstance(board.pola[x][y],plansza.Water): 
                draw_hexagon(centre,radius,"blue",screen)
                if board.pola[x][y].strength>0:
                    sprites.add(Ship(centre,radius,board.pola[x][y].owner.name,board.pola[x][y].value>0))
                if board.pola[x][y].value>0:
                    if (x,y) not in ktory_wyglad_monety:
                        ktory_wyglad_monety[(x,y)]=random.randint(1,2)
                    sprites.add(Coin(centre,radius,ktory_wyglad_monety[(x,y)]))

            # if isinstance(board.pola[x][y],plansza.Island):
            #     draw_hexagon(centre,radius,"brown")
            if isinstance(board.pola[x][y],plansza.Capital):
                draw_hexagon(centre,radius,"gold",screen)
                if len(board.pola[x][y].territory)>1:
                    handle_islands(x,y,board.pola[x][y].territory.copy(),board.pola[x][y].buildings.copy(),centre,radius)
                    handle_capital(x,y,board.pola[x][y].territory.copy(),board.pola[x][y].buildings.copy(),board.pola[x][y].strength,board.pola[x][y].value,centre,radius,board.pola[x][y].owner.name,False)
                else:
                    handle_capital(x,y,board.pola[x][y].territory.copy(),board.pola[x][y].buildings.copy(),board.pola[x][y].strength,board.pola[x][y].value,centre,radius,board.pola[x][y].owner.name,True)
                # print(x,y)
                # if board.pola[x][y].strength>0:
                #     sprites.add(Warrior(centre,radius,board.pola[x][y].owner.name))
                # if board.pola[x][y].value>0:
                #     if (x,y) not in ktory_wyglad_monety:
                #         ktory_wyglad_monety[(x,y)]=random.randint(1,2)
                #     sprites.add(Coin(centre,radius,ktory_wyglad_monety[(x,y)]))
            
            if x+1<len(board.pola) and y+1<len(board.pola[x+1]):
                crawl(x+1,y+1,konw(centre,radius,1),radius,board)

            if x+1<len(board.pola) and y<len(board.pola[x+1]):
                crawl(x+1,y,konw(centre,radius,2),radius,board)

            if x>=0 and y-1>=0:
                crawl(x,y-1,konw(centre,radius,3),radius,board)
            
            if x-1>=0 and y-1>=0:
                crawl(x-1,y-1,konw(centre,radius,4),radius,board)
            if x-1>=0 and y>=0:
                crawl(x-1,y,konw(centre,radius,5),radius,board)

    crawl(1,1,poczatkowy_srodek,promien,board)
    sprites.draw(screen)

def generate_to_wh(screen):
    width,height = screen.get_width(),screen.get_height()
    drawing_width,drawing_height = width*0.9,height*0.9
    delta_width,delta_height = width-drawing_width,height-drawing_height
    dozy_promien = 1/math.cos(math.radians(60))
    ile_w_gore = 21
    ile_w_dol = 1
    ile_w_lewo = 8*dozy_promien
    ile_w_prawo = 8*dozy_promien
    pr = min(drawing_height/22,drawing_width/(16*dozy_promien))

    y = height/2+10*pr
    x = width/2
    return ((x,y),pr)



def game(board,screen):
    running = 1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # print("clicked")
                running = False
                # pygame.quit()

        screen.fill("light blue")
        render_board(generate_to_wh(screen),board,screen)
        
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    

def start_visualization(board):
    global clock
    pygame.init()
    # pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS,3)
    screen = pygame.display.set_mode((tk.Tk().winfo_screenwidth(),tk.Tk().winfo_screenheight()-80),pygame.RESIZABLE)
    pygame.display.set_caption("Cyklades")
    clock = pygame.time.Clock()
    icon = pygame.image.load('graphics/ikona.ico') 
    pygame.display.set_icon(icon)
    # set_up(board)
    game(board,screen)
