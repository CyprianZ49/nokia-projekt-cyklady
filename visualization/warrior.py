import pygame
import math
from visualization.globals import *

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