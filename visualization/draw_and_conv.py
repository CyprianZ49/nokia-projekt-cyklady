import math
import pygame
from visualization.globals import *

def punkty(centre,promien):
    dozy_promien = promien/math.cos(math.radians(60))
    return [(centre[0]-promien*math.tan(math.radians(30)),centre[1]-promien),
        (centre[0]-(promien/math.cos(math.radians(30))),centre[1]),
        (centre[0]-promien*math.tan(math.radians(30)),centre[1]+promien),
        (centre[0]+promien*math.tan(math.radians(30)),centre[1]+promien),
        (centre[0]+(promien/math.cos(math.radians(30))),centre[1]),
        (centre[0]+promien*math.tan(math.radians(30)),centre[1]-promien)]

def draw_hexagon(centre,radius,color,screen):
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
    
def draw_red_line(centre,radius,screen):
    pygame.draw.polygon(screen,"orangered2",[
        (centre[0]-radius*math.tan(math.radians(30)),centre[1]-radius),
        (centre[0]-(radius/math.cos(math.radians(30))),centre[1]),
        (centre[0]-radius*math.tan(math.radians(30)),centre[1]+radius),
        (centre[0]+radius*math.tan(math.radians(30)),centre[1]+radius),
        (centre[0]+(radius/math.cos(math.radians(30))),centre[1]),
        (centre[0]+radius*math.tan(math.radians(30)),centre[1]-radius)],4)
    
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