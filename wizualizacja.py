from typing import Any
import pygame
import math
import random
import plansza

pygame.init()
screen = pygame.display.set_mode((1820, 980))
running = True
pygame.display.set_caption("Cyklades")
clock = pygame.time.Clock()




def draw_map(wspolrzedne_pierwszego_punktu,mapa,promien,odw): #mapa sklada się z listy par (para(id,lista 6 sąsiadów(ich id)),rodzaj terenu(woda lub ziemia))
    pass

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


odwiedzone = {}
def crawl(x,y,centre,radius):
    #print(board.pola[x][y]==plansza.Water)
    if (x,y) not in odwiedzone:
        print(x,y)
        odwiedzone[(x,y)]=True
        if isinstance(board.pola[x][y],plansza.Water):
            draw_hexagon(centre,radius,"blue")
        if isinstance(board.pola[x][y],plansza.Island):
            draw_hexagon(centre,radius,"brown")
        if isinstance(board.pola[x][y],plansza.Capital):
            draw_hexagon(centre,radius,"gold")
        
        if x+1<len(board.pola) and y+1<len(board.pola[x+1]):
            crawl(x+1,y+1,konw(centre,radius,1),radius)

        if x+1<len(board.pola) and y<len(board.pola[x+1]):
            crawl(x+1,y,konw(centre,radius,2),radius)

        if x>=0 and y-1>=0:
            crawl(x,y-1,konw(centre,radius,3),radius)
        
        if x-1>=0 and y-1>=0:
            crawl(x-1,y-1,konw(centre,radius,4),radius)
        if x-1>=0 and y>=0:
            crawl(x-1,y,konw(centre,radius,5),radius)
        
        # if x-1>=0 and y-1>=0:
        #     crawl(x-1,y-1,konw(centre,radius,4),radius)
    

def render_board(poczatkowy_srodek,promien):
    odwiedzone.clear()
    crawl(0,0,poczatkowy_srodek,promien)

def game():
    running = 1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        
        screen.fill("light blue")
        render_board((900,850),30)
        # srodek = (900,450)
        # promien = 50
        # draw_hexagon(srodek,promien,"grey")
        # for i in range(1,7):
        #     draw_hexagon(konw(srodek,promien,i),promien,((i+5)**1.5,(i+5)**1.9,(i+5)**2.2))


    
        pygame.display.update()
        clock.tick(60)
    

board = plansza.Plansza()
board.generateBoard()
#print(board.pola)
game()

pygame.quit()