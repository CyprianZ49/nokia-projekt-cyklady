from typing import Any
import pygame
import math
import random

pygame.init()
screen = pygame.display.set_mode((1820, 980))
running = True
pygame.display.set_caption("Game")
clock = pygame.time.Clock()




def draw_map(wspolrzedne_pierwszego_punktu,mapa,promien,odw): #mapa sklada się z listy par (para(id,lista 6 sąsiadów(ich id)),rodzaj terenu(woda lub ziemia))
    pass



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    screen.fill("light blue")

   
    pygame.display.update()
    clock.tick(60)
    

   

pygame.quit()