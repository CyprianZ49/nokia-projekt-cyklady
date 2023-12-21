import math
import pygame
from visualization.globals import *

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