from typing import Any
import pygame
import math
import random
import plansza
from bot import Bot
import sys
import tkinter as tk





class Warrior(pygame.sprite.Sprite):
    def __init__(self,srodek,promien,owner_name):
        global ktory_nr_wolny
        global owners_colors
        super().__init__()

        if owner_name not in owners_colors:
            owners_colors[owner_name] = ktory_nr_wolny
            ktory_nr_wolny+=1
        
        if owners_colors[owner_name] == 1:
            self.image = pygame.image.load("grafikav2/solider_blue.png").convert_alpha()
        if owners_colors[owner_name] == 2:
            self.image = pygame.image.load("grafikav2/solider_green.png").convert_alpha()
        if owners_colors[owner_name] == 3:
            self.image = pygame.image.load("grafikav2/solider_red.png").convert_alpha()
        if owners_colors[owner_name] == 4:
            self.image = pygame.image.load("grafikav2/solider_white.png").convert_alpha()
        if owners_colors[owner_name] == 5:
            self.image = pygame.image.load("grafikav2/solider_yellow.png").convert_alpha()

        dozy_promien = promien/math.cos(math.radians(60))
        maxwidth = 1.8*dozy_promien
        maxheight = 1.8*promien
        skala = min(maxheight/self.image.get_height(),maxwidth/self.image.get_width())

        self.image = pygame.transform.scale(self.image,(self.image.get_width()*skala,self.image.get_height()*skala))

        self.rect = self.image.get_rect(center = srodek)
class Ship(pygame.sprite.Sprite):
    def __init__(self,srodek,promien,owner_name):
        global ktory_nr_wolny
        global owners_colors
        super().__init__()

        if owner_name not in owners_colors:
            owners_colors[owner_name] = ktory_nr_wolny
            ktory_nr_wolny+=1
        
        if owners_colors[owner_name] == 1:
            self.image = pygame.image.load("grafikav2/fleet_blue.png").convert_alpha()
        if owners_colors[owner_name] == 2:
            self.image = pygame.image.load("grafikav2/fleet_green.png").convert_alpha()
        if owners_colors[owner_name] == 3:
            self.image = pygame.image.load("grafikav2/fleet_red.png").convert_alpha()
        if owners_colors[owner_name] == 4:
            self.image = pygame.image.load("grafikav2/fleet_white.png").convert_alpha()
        if owners_colors[owner_name] == 5:
            self.image = pygame.image.load("grafikav2/fleet_yellow.png").convert_alpha()

        dozy_promien = promien/math.cos(math.radians(60))
        maxwidth = 1.4*dozy_promien
        maxheight = 1.4*promien
        skala = min(maxheight/self.image.get_height(),maxwidth/self.image.get_width())

        self.image = pygame.transform.scale(self.image,(self.image.get_width()*skala,self.image.get_height()*skala))

        self.rect = self.image.get_rect(center = srodek)

class Coin(pygame.sprite.Sprite):
    def __init__(self,srodek,promien,kt):
        super().__init__()
        moneta = "coin_omega" if kt==1 else "coin_theta"
        self.image = pygame.image.load(f"grafikav2/{moneta}.png").convert_alpha()
        
        dozy_promien = promien/math.cos(math.radians(60))
        maxwidth = 1.4*dozy_promien
        maxheight = 1.4*promien
        skala = min(maxheight/self.image.get_height(),maxwidth/self.image.get_width())

        self.image = pygame.transform.scale(self.image,(self.image.get_width()*skala,self.image.get_height()*skala))

        self.rect = self.image.get_rect(center = srodek)




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


def punkty(centre,promien):
    dozy_promien = promien/math.cos(math.radians(60))

def render_board(package,board):
    odwiedzone = {}
    poczatkowy_srodek,promien = package
    for warrior in sprites:
        warrior.kill()
    def crawl(x,y,centre,radius,board):
        #print(board.pola[x][y]==plansza.Water)
        if (x,y) not in odwiedzone:
            #print(x,y)
            odwiedzone[(x,y)]=True
            if isinstance(board.pola[x][y],plansza.Water): 
                draw_hexagon(centre,radius,"blue")
                if board.pola[x][y].strength>0:
                    sprites.add(Ship(centre,radius,board.pola[x][y].owner.name))

            if isinstance(board.pola[x][y],plansza.Island):
                draw_hexagon(centre,radius,"brown")
            if isinstance(board.pola[x][y],plansza.Capital):
                draw_hexagon(centre,radius,"gold")
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
    
        pygame.display.update()
        clock.tick(60)
    

# board = plansza.Plansza("xd")
# board.generateBoard()

def start_visualization(board):
    pygame.init()
    global screen
    global clock
    screen = pygame.display.set_mode((tk.Tk().winfo_screenwidth(),tk.Tk().winfo_screenheight()-80),pygame.RESIZABLE)
    pygame.display.set_caption("Cyklades")
    clock = pygame.time.Clock()
    icon = pygame.image.load('graphics/ikona.ico') 
    pygame.display.set_icon(icon)
    set_up(board)
    # print("xddddd")
    game(board)




