from typing import Any
import pygame
import math
import random

pygame.init()
screen = pygame.display.set_mode((1820, 980))
running = True
pygame.display.set_caption("Cyklades")
clock = pygame.time.Clock()




def draw_map(wspolrzedne_pierwszego_punktu,mapa,promien,odw): #mapa sklada się z listy par (para(id,lista 6 sąsiadów(ich id)),rodzaj terenu(woda lub ziemia))
    pass

def draw_hexagon(centre,radius,color):
    pygame.draw.polygon(screen,color,[
        (centre[0]-radius*0.5,centre[1]-radius),
        (centre[0]-(radius*0.5+radius/math.tan(math.radians(60))),centre[1]),
        (centre[0]-radius*0.5,centre[1]+radius),
        (centre[0]+radius*0.5,centre[1]+radius),
        (centre[0]+(radius*0.5+radius/math.tan(math.radians(60))),centre[1]),
        (centre[0]+radius*0.5,centre[1]-radius)])
    pygame.draw.polygon(screen,"black",[
        (centre[0]-radius*0.5,centre[1]-radius),
        (centre[0]-(radius*0.5+radius/math.tan(math.radians(60))),centre[1]),
        (centre[0]-radius*0.5,centre[1]+radius),
        (centre[0]+radius*0.5,centre[1]+radius),
        (centre[0]+(radius*0.5+radius/math.tan(math.radians(60))),centre[1]),
        (centre[0]+radius*0.5,centre[1]-radius)],3)
    
def konw1(centre,radius):#1 na gorze i pozniej wedlug wskazowek zegara
    return (centre[0],centre[1]-2*radius)
def konw2(centre,radius):
    return (centre[0]+(0.5*radius+(radius*0.5+radius/math.tan(math.radians(60)))),centre[1]-radius)
def konw3(centre,radius):
    return (centre[0]+(0.5*radius+(radius*0.5+radius/math.tan(math.radians(60)))),centre[1]+radius)
def konw4(centre,radius):#1 na gorze i pozniej wedlug wskazowek zegara
    return (centre[0],centre[1]+2*radius)
def konw5(centre,radius):
    return (centre[0]-(0.5*radius+(radius*0.5+radius/math.tan(math.radians(60)))),centre[1]+radius)
def konw6(centre,radius):
    return (centre[0]-(0.5*radius+(radius*0.5+radius/math.tan(math.radians(60)))),centre[1]-radius)

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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    screen.fill("light blue")
    srodek = (900,450)
    promien = 50
    draw_hexagon(srodek,promien,"red")
    for i in range(1,7):
        draw_hexagon(konw(srodek,promien,i),promien,((i+5)**1.5,(i+5)**1.9,(i+5)**2.2))
    # draw_hexagon((900,450),50,"gray")

   
    pygame.display.update()
    clock.tick(60)
    

   

pygame.quit()