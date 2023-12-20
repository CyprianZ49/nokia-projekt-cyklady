from typing import Any
import pygame
import math
import random
import plansza
from bot import Bot
import sys
import tkinter as tk
from OpenGL.GL import *
from pygame.locals import *
from OpenGL.GLU import *



def punkty(centre,promien):
    dozy_promien = promien/math.cos(math.radians(60))
    return [(centre[0]-promien*math.tan(math.radians(30)),centre[1]-promien),
        (centre[0]-(promien/math.cos(math.radians(30))),centre[1]),
        (centre[0]-promien*math.tan(math.radians(30)),centre[1]+promien),
        (centre[0]+promien*math.tan(math.radians(30)),centre[1]+promien),
        (centre[0]+(promien/math.cos(math.radians(30))),centre[1]),
        (centre[0]+promien*math.tan(math.radians(30)),centre[1]-promien)]

class Warrior(pygame.sprite.Sprite):
    def __init__(self,srodek,promien,owner_name):
        global ktory_nr_wolny
        global owners_colors
        super().__init__()

        if owner_name not in owners_colors:
            owners_colors[owner_name] = ktory_nr_wolny
            ktory_nr_wolny+=1
        
        if owners_colors[owner_name] == 1:
            self.image = pygame.image.load("icons/warrior blue.png").convert_alpha()
        if owners_colors[owner_name] == 2:
            self.image = pygame.image.load("icons/warrior green.png").convert_alpha()
        if owners_colors[owner_name] == 3:
            self.image = pygame.image.load("icons/warrior red.png").convert_alpha()
        if owners_colors[owner_name] == 4:
            self.image = pygame.image.load("icons/warrior white.png").convert_alpha()
        if owners_colors[owner_name] == 5:
            self.image = pygame.image.load("icons/warrior yellow.png").convert_alpha()

        dozy_promien = promien/math.cos(math.radians(60))
        maxwidth = 1.8*dozy_promien
        maxheight = 1.8*promien
        skala = min(maxheight/self.image.get_height(),maxwidth/self.image.get_width())

        self.image = pygame.transform.smoothscale(self.image,(self.image.get_width()*skala,self.image.get_height()*skala))

        self.rect = self.image.get_rect(center = srodek)
class Ship(pygame.sprite.Sprite):
    def __init__(self,srodek,promien,owner_name,withcoin:bool):
        global ktory_nr_wolny
        global owners_colors
        super().__init__()

        if owner_name not in owners_colors:
            owners_colors[owner_name] = ktory_nr_wolny
            ktory_nr_wolny+=1
        
        if owners_colors[owner_name] == 1:
            self.image = pygame.image.load("icons/fleet blue.png").convert_alpha()
        if owners_colors[owner_name] == 2:
            self.image = pygame.image.load("icons/fleet green.png").convert_alpha()
        if owners_colors[owner_name] == 3:
            self.image = pygame.image.load("icons/fleet red.png").convert_alpha()
        if owners_colors[owner_name] == 4:
            self.image = pygame.image.load("icons/fleet white.png").convert_alpha()
        if owners_colors[owner_name] == 5:
            self.image = pygame.image.load("icons/fleet yellow.png").convert_alpha()
        
        new_srodek = srodek
        if withcoin:
            jc = 0.32#jaka czesc 1 - na skraju max, 0 - na srodku
            dl = promien*jc
            x = dl/math.tan(math.radians(60))
            new_srodek = (srodek[0]-x,srodek[1]+dl)

        dozy_promien = promien/math.cos(math.radians(60))
        maxwidth = 1.4*dozy_promien
        maxheight = 1.4*promien
        skala = min(maxheight/self.image.get_height(),maxwidth/self.image.get_width())

        self.image = pygame.transform.smoothscale(self.image,(self.image.get_width()*skala,self.image.get_height()*skala))

        self.rect = self.image.get_rect(center = new_srodek)

class Coin(pygame.sprite.Sprite):
    def __init__(self,srodek,promien,kt):
        super().__init__()
        moneta = "coin_omega" if kt==1 else "coin_theta"
        self.image = pygame.image.load(f"grafikav2/{moneta}.png").convert_alpha()
        
        new_srodek = srodek
        jc = 0.6#jaka czesc 1 - na skraju max, 0 - na srodku
        dl = promien*jc
        x = dl/math.tan(math.radians(60))
        new_srodek = (srodek[0]+x,srodek[1]-dl)

        # skala = min(maxheight/self.image.get_height(),maxwidth/self.image.get_width())

        dozy_promien = promien/math.cos(math.radians(60))
        maxwidth = 0.8*dozy_promien
        maxheight = 0.8*promien
        skala = min(maxheight/self.image.get_height(),maxwidth/self.image.get_width())

        self.image = pygame.transform.smoothscale(self.image,(self.image.get_width()*skala,self.image.get_height()*skala))

        self.rect = self.image.get_rect(center = new_srodek)




def draw_hexagon(centre,radius,color):
    pygame.draw.polygon(screen,color,[
        (centre[0]-radius*math.tan(math.radians(30)),centre[1]-radius),
        (centre[0]-(radius/math.cos(math.radians(30))),centre[1]),
        (centre[0]-radius*math.tan(math.radians(30)),centre[1]+radius),
        (centre[0]+radius*math.tan(math.radians(30)),centre[1]+radius),
        (centre[0]+(radius/math.cos(math.radians(30))),centre[1]),
        (centre[0]+radius*math.tan(math.radians(30)),centre[1]-radius)])
    pygame.draw.polygon(screen,"black",[
        (centre[0]-radius*math.tan(math.radians(30)),centre[1]-radius),
        (centre[0]-(radius/math.cos(math.radians(30))),centre[1]),
        (centre[0]-radius*math.tan(math.radians(30)),centre[1]+radius),
        (centre[0]+radius*math.tan(math.radians(30)),centre[1]+radius),
        (centre[0]+(radius/math.cos(math.radians(30))),centre[1]),
        (centre[0]+radius*math.tan(math.radians(30)),centre[1]-radius)],3)
    
def konw1(centre,radius):#1 na gorze i pozniej wedlug wskazowek zegara
    return (centre[0],centre[1]-2*radius)
def konw2(centre,radius):
    return (centre[0]+2*(math.cos(math.radians(30))*radius),centre[1]-2*(math.sin(math.radians(30))*radius))
def konw3(centre,radius):
    return (centre[0]+2*(math.cos(math.radians(30))*radius),centre[1]+2*(math.sin(math.radians(30))*radius))
def konw4(centre,radius):#1 na gorze i pozniej wedlug wskazowek zegara
    return (centre[0],centre[1]+2*radius)
def konw5(centre,radius):
    return (centre[0]-2*(math.cos(math.radians(30))*radius),centre[1]+2*(math.sin(math.radians(30))*radius))
def konw6(centre,radius):
    return (centre[0]-2*(math.cos(math.radians(30))*radius),centre[1]-2*(math.sin(math.radians(30))*radius))

def konw(centre,radius,typ):
    if typ == 1:
        return konw1(centre,radius)
    if typ == 2:
        return konw2(centre,radius)
    if typ == 3:
        return konw3(centre,radius)
    if typ == 4:
        return konw4(centre,radius)
    if typ == 5:
        return konw5(centre,radius)
    if typ == 6:
        return konw6(centre,radius)



def render_board(package,board):
    odwiedzone = {}
    poczatkowy_srodek,promien = package
    for warrior in sprites:
        warrior.kill()
    def draw_island(x,y,budynki,centre,radius):
        draw_hexagon(centre,radius,"brown")

    def handle_islands(capitalx,capitaly,pola,budynki,centre,radius):
        if [capitalx,capitaly] in pola:
            pola.remove([capitalx,capitaly])
        
        while 0 in budynki:
            budynki.remove(0)
        


        for i in range(len(pola)):
            ile = math.ceil(len(budynki)/len(pola))
            island_centre = centre

            if pola[i][1] > capitaly:
                for _ in range(pola[i][1]-capitaly):
                    island_centre=konw(island_centre,radius,1)
                pola[i][0]+=pola[i][1]-capitaly
            if pola[i][0] > capitalx:
                for _ in range(pola[i][0]-capitalx):
                    island_centre=konw(island_centre,radius,2)
            if pola[i][0] < capitalx:
                for _ in range(capitalx-pola[i][0]):
                    island_centre=konw(island_centre,radius,5)
            if pola[i][1] < capitaly:
                for _ in range(capitaly-pola[i][1]):
                    island_centre=konw(island_centre,radius,3)

            draw_island(pola[i][0],pola[i][1],budynki[0:ile] if ile!=0 else [],island_centre,radius)
            for _ in range(ile):
                budynki.pop(0)

            




        
        # print(capitalx,capitaly,pola)

    def crawl(x,y,centre,radius,board):
        #print(board.pola[x][y]==plansza.Water)
        if (x,y) not in odwiedzone:
            #print(x,y)
            odwiedzone[(x,y)]=True
            if isinstance(board.pola[x][y],plansza.Water): 
                draw_hexagon(centre,radius,"blue")
                if board.pola[x][y].strength>0:
                    sprites.add(Ship(centre,radius,board.pola[x][y].owner.name,board.pola[x][y].value>0))
                if board.pola[x][y].value>0:
                    if (x,y) not in ktory_wyglad_monety:
                        ktory_wyglad_monety[(x,y)]=random.randint(1,2)
                    sprites.add(Coin(centre,radius,ktory_wyglad_monety[(x,y)]))

            # if isinstance(board.pola[x][y],plansza.Island):
            #     draw_hexagon(centre,radius,"brown")
            if isinstance(board.pola[x][y],plansza.Capital):
                draw_hexagon(centre,radius,"gold")
                handle_islands(x,y,board.pola[x][y].territory.copy(),board.pola[x][y].buildings.copy(),centre,radius)
                # print(x,y)
                if board.pola[x][y].strength>0:
                    sprites.add(Warrior(centre,radius,board.pola[x][y].owner.name))
                if board.pola[x][y].value>0:
                    if (x,y) not in ktory_wyglad_monety:
                        ktory_wyglad_monety[(x,y)]=random.randint(1,2)
                    sprites.add(Coin(centre,radius,ktory_wyglad_monety[(x,y)]))
            
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

def generate_to_wh():
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






    
def set_up(board):
    global sprites
    sprites = pygame.sprite.Group()
    global owners_colors
    owners_colors={}
    global ktory_nr_wolny
    ktory_nr_wolny = 1
    global ktory_wyglad_monety
    ktory_wyglad_monety={}

def game(board):
    running = 1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # print("clicked")
                running = False
                # pygame.quit()

        screen.fill("light blue")
        render_board(generate_to_wh(),board)
        
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    

# board = plansza.Plansza("xd")
# board.generateBoard()

def start_visualization(board):
    pygame.init()
    global screen
    global clock
    # pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS,3)
    screen = pygame.display.set_mode((tk.Tk().winfo_screenwidth(),tk.Tk().winfo_screenheight()-80),pygame.RESIZABLE)
    pygame.display.set_caption("Cyklades")
    clock = pygame.time.Clock()
    icon = pygame.image.load('graphics/ikona.ico') 
    pygame.display.set_icon(icon)
    set_up(board)
    # print("xddddd")
    game(board)




