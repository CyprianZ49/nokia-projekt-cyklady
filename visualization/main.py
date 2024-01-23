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
from visualization.draw_and_conv import *
from visualization.ship import Ship
from visualization.coin import Coin
from visualization.structures import Structure
import copy


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
                sprites.add(Structure(x,centre,radius,0))
        else:
            ktory_budynek = 1
            for x in budynki:
                sprites.add(Structure(x,centre,radius,ktory_budynek))
                ktory_budynek+=1

                if ktory_budynek>2:#ten if sluzy do testowania!!!
                    break

    def handle_islands(capitalx,capitaly,pola,budynki,centre,radius,iM):
        if iM:
            budynki.append(5)

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
    
    def handle_capital(x,y,pola, budynki,sila,value,centre,radius,imie,czy_solo_stolica,iM):
        if iM:
            budynki.append(5)
        # if sila>0:
        #     sprites.add(Warrior(centre,radius,imie))
        while 0 in budynki:
            budynki.remove(0)

        if value>0:
            if (x,y) not in ktory_wyglad_monety:
                ktory_wyglad_monety[(x,y)]=random.randint(1,2)
            sprites.add(Coin(centre,radius,ktory_wyglad_monety[(x,y)],value))
        
        # print(czy_solo_stolica,value,sila)
        if czy_solo_stolica:
            # entity = budynki+['moneta','zolnierz']
            if len(budynki)==0:
                if value==0:
                    if sila>0:
                        sprites.add(Warrior(centre,radius,imie,0,sila,False,0,0))# solo warrior
                else:
                    if sila>0:
                        sprites.add(Warrior(centre,radius,imie,1,sila,False,0,0))# warrior i moneta
            else:
                if value==0:
                    if sila>0:
                        sprites.add(Warrior(centre,radius,imie,3,sila,False,0,0))#budynek i warrior, TEN CASE NIGDY NIE  ZACHODZI, A ZOSTAWIAM GO DLA WIDOCZNOSCI
                else:
                    if sila>0:
                        sprites.add(Warrior(centre,radius,imie,2,sila,False,0,0))#budynek, moneta i warrior
                        if 1 in budynki:
                            sprites.add(Structure(1,centre,radius,3))
                        if 2 in budynki:
                            # print("xd")
                            sprites.add(Structure(2,centre,radius,3))
                        if 3 in budynki:
                            sprites.add(Structure(3,centre,radius,3))
                        if 4 in budynki:
                            sprites.add(Structure(4,centre,radius,3))

        else:#przypadek w ktorym istnieja inne pola wyspy i na nich sa wszystkie budynki
            if value==0:
                if sila>0:
                    sprites.add(Warrior(centre,radius,imie,0,sila,False,0,0)) # tylko zolnierz
            else:
                if sila>0:
                    sprites.add(Warrior(centre,radius,imie,1,sila,False,0,0))# zolnierz i moneta

    def handle_fight(centre,radius,ap,dp,ac,dc,czy_pole_wodne): #a - atacker, d - defender, c - color, p - power
        x = centre[0]
        y = centre[1]
        wysokosc_prostokata = 1.3*radius
        szerokosc_prosokata = 2.5*radius
        pygame.draw.polygon(screen,(184,14,48),[
            (x-szerokosc_prosokata/2,y-radius-wysokosc_prostokata),
            (x-szerokosc_prosokata/2,y-radius),
            (x+szerokosc_prosokata/2,y-radius),
            (x+szerokosc_prosokata/2,y-radius-wysokosc_prostokata),
        ])
        pygame.draw.polygon(screen,"black",[
            (x-szerokosc_prosokata/2,y-radius-wysokosc_prostokata),
            (x-szerokosc_prosokata/2,y-radius),
            (x+szerokosc_prosokata/2,y-radius),
            (x+szerokosc_prosokata/2,y-radius-wysokosc_prostokata),
        ],3)

        sr = ((x-szerokosc_prosokata/2+x+szerokosc_prosokata/2)/2,(y-radius-wysokosc_prostokata+y-radius)/2)
        jaka_czesc = 0.5 #jaka czesc odleglosci z srodka prostokata do boku, 1 - na maksa w prawo, 0 - srodek
        sr1 = (sr[0]+jaka_czesc*(szerokosc_prosokata/2),sr[1])
        sr2 = (sr[0]-jaka_czesc*(szerokosc_prosokata/2),sr[1])

        if czy_pole_wodne:
            sprites.add(Ship(sr1,radius,ac.name,0,ap,True,szerokosc_prosokata,wysokosc_prostokata))
            sprites.add(Ship(sr2,radius,dc.name,0,dp,True,szerokosc_prosokata,wysokosc_prostokata))
        else:
            sprites.add(Warrior(sr1,radius,ac.name,0,ap,True,szerokosc_prosokata,wysokosc_prostokata))
            sprites.add(Warrior(sr2,radius,dc.name,0,dp,True,szerokosc_prosokata,wysokosc_prostokata))


        
    
    def update1(x,y,centre,radius,board):
        if isinstance(board.pola[x][y],plansza.Water): 
            draw_hexagon(centre,radius,"blue",screen)
            if board.pola[x][y].strength>0:
                sprites.add(Ship(centre,radius,board.pola[x][y].owner.name,board.pola[x][y].value>0,board.pola[x][y].strength,False,0,0))
            if board.pola[x][y].value>0:
                if (x,y) not in ktory_wyglad_monety:
                    ktory_wyglad_monety[(x,y)]=random.randint(1,2)
                sprites.add(Coin(centre,radius,ktory_wyglad_monety[(x,y)],board.pola[x][y].value))

        if isinstance(board.pola[x][y],plansza.Capital):
            draw_hexagon(centre,radius,"gold",screen)
            if len(board.pola[x][y].territory)>1:
                handle_islands(x,y,board.pola[x][y].territory.copy(),board.pola[x][y].buildings.copy(),centre,radius,board.pola[x][y].isMetropolis)
                handle_capital(x,y,board.pola[x][y].territory.copy(),board.pola[x][y].buildings.copy(),board.pola[x][y].strength,board.pola[x][y].value,centre,radius,board.pola[x][y].owner.name,False,board.pola[x][y].isMetropolis)
            else:
                handle_capital(x,y,board.pola[x][y].territory.copy(),board.pola[x][y].buildings.copy(),board.pola[x][y].strength,board.pola[x][y].value,centre,radius,board.pola[x][y].owner.name,True,board.pola[x][y].isMetropolis)
    
    def update2(x,y,centre,radius,board):
        if (isinstance(board.pola[x][y],plansza.Water) or isinstance(board.pola[x][y],plansza.Capital)) and board.pola[x][y].fighting:
            draw_red_line(centre,radius,screen)
    
    def update3(x,y,centre,radius,board):
        if board.isFight and board.whereFight == (x,y):
            handle_fight(centre,radius,board.attackerPower,board.defenderPower,board.attackerColor,board.defenderColor,True if isinstance(board.pola[x][y],plansza.Water) else False)
    
    def crawl(x,y,centre,radius,board,func):
        if (x,y) not in odwiedzone:
            odwiedzone[(x,y)]=True
            
            func(x,y,centre,radius,board)

            if x+1<len(board.pola) and y+1<len(board.pola[x+1]):
                crawl(x+1,y+1,konw(centre,radius,1),radius,board,func)

            if x+1<len(board.pola) and y<len(board.pola[x+1]):
                crawl(x+1,y,konw(centre,radius,2),radius,board,func)

            if x>=0 and y-1>=0:
                crawl(x,y-1,konw(centre,radius,3),radius,board,func)
            
            if x-1>=0 and y-1>=0:
                crawl(x-1,y-1,konw(centre,radius,4),radius,board,func)
            if x-1>=0 and y>=0:
                crawl(x-1,y,konw(centre,radius,5),radius,board,func)
    
    def crawles():
        crawl(1,1,poczatkowy_srodek,promien,board,update1)
        odwiedzone.clear()
        crawl(1,1,poczatkowy_srodek,promien,board,update2)
        odwiedzone.clear()
        crawl(1,1,poczatkowy_srodek,promien,board,update3)


    # crawl1(1,1,poczatkowy_srodek,promien,board)
    # odwiedzone.clear()
    # crawl2(1,1,poczatkowy_srodek,promien,board)
    crawles()
    
    sprites.draw(screen)

def generate_to_wh(screen):
    width,height = screen.get_width(),screen.get_height()
    procent_ekranu_na_plansze = 0.9
    drawing_width,drawing_height = width*procent_ekranu_na_plansze,height*procent_ekranu_na_plansze
    delta_width,delta_height = width-drawing_width,height-drawing_height
    dozy_promien = 1/math.sin(math.radians(60))
    ile_w_gore = 21
    ile_w_dol = 1
    ile_w_lewo = 8*dozy_promien
    ile_w_prawo = 8*dozy_promien
    pr = min(drawing_height/22,drawing_width*math.sin(math.radians(60))/(17))

    y = height/2+10*pr
    x = width/2
    return ((x,y),pr)

def generete_w_players(screen):
    width,height = screen.get_width(),screen.get_height()
    procent_ekranu_na_plansze = 0.9
    drawing_width,drawing_height = width*procent_ekranu_na_plansze,height*procent_ekranu_na_plansze
    delta_width,delta_height = width-drawing_width,height-drawing_height
    dozy_promien = 1/math.sin(math.radians(60))
    ile_w_gore = 21
    ile_w_dol = 1
    ile_w_lewo = 8*dozy_promien
    ile_w_prawo = 8*dozy_promien
    pr = min(drawing_height/22,drawing_width*math.sin(math.radians(60))/(17))

    res=pr*dozy_promien*17


    return (width-res)/2

def render_gracz(ld,pg,screen,bot_name):#ld - lewy dolny punkt pola, pg - prawy górny rog pola (x,y)
    pygame.draw.polygon(screen,"black",[
        ld,
        (pg[0],ld[1]),
        pg,
        (ld[0],pg[1])
    ],3)

def render_players(szerekosc_prostokata,wysokosc_prostokata,screen,players:list[Bot]):
    odl_miedzy_polami_graczy = (0.15*wysokosc_prostokata)/4
    odl_miedzy_bokami = 0.075*szerekosc_prostokata
    wysokosc_pola_gracza = (wysokosc_prostokata-4*odl_miedzy_polami_graczy)/3
    szerokosc_pola_gracza = szerekosc_prostokata-2*odl_miedzy_bokami

    liczba_graczy = len(players)
    ld = [odl_miedzy_bokami,odl_miedzy_polami_graczy+wysokosc_pola_gracza]
    pg = [szerekosc_prostokata-odl_miedzy_bokami,odl_miedzy_polami_graczy]
    for i in range(3):
        render_gracz(ld.copy(),pg.copy(),screen,"xd")
        ld[1]+=odl_miedzy_polami_graczy+wysokosc_pola_gracza
        pg[1]+=odl_miedzy_polami_graczy+wysokosc_pola_gracza

    ld = [screen.get_width()-odl_miedzy_bokami,odl_miedzy_polami_graczy+wysokosc_pola_gracza]
    pg = [screen.get_width()-(szerekosc_prostokata-odl_miedzy_bokami),odl_miedzy_polami_graczy]

    for i in range(3):
        render_gracz(ld.copy(),pg.copy(),screen,"xd")
        ld[1]+=odl_miedzy_polami_graczy+wysokosc_pola_gracza
        pg[1]+=odl_miedzy_polami_graczy+wysokosc_pola_gracza




def game(board,screen,players):
    running = 1
    ile = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    ile+=1
                if event.key == pygame.K_LCTRL:
                    ile+=1
        if ile == 2:
            running = False

        # set_up(board)

        screen.fill("light blue")
        render_board(generate_to_wh(screen),board,screen)
        render_players(generete_w_players(screen),screen.get_height(),screen,players)
            
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


# def set_up(board):
#     for x in range(len(board.pola)):
#         for y in range(len(board.pola[x])):
#             if isinstance(board.pola[x][y],plansza.Capital):
#                 if board.pola[x][y].isMetropolis:
#                     board.pola[x][y].buildings.append(5)

def start_visualization(board,players):
    global clock
    pygame.init()
    # pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS,3)
    screen = pygame.display.set_mode((tk.Tk().winfo_screenwidth(),tk.Tk().winfo_screenheight()-65),pygame.RESIZABLE)
    pygame.display.set_caption("Cyklades")
    clock = pygame.time.Clock()
    icon = pygame.image.load('graphics/ikona.ico') 
    pygame.display.set_icon(icon)
    game(board,screen,players)
