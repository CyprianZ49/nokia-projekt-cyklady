import math
import pygame
from visualization.globals import *

class Ship(pygame.sprite.Sprite):

    def good_path(self,kolor,liczba):
        return f"f{kolor}{liczba}"

    def __init__(self,srodek,promien,owner_name,withcoin:bool,sila,isFight,rec_width,rec_height):
        lock.acquire()
        global ktory_nr_wolny
        global owners_colors
        super().__init__()

        if owner_name not in owners_colors:
            owners_colors[owner_name] = ktory_nr_wolny[0]
            # print(ktory_nr_wolny)
            # with open('xd.txt','a') as f:
            #     f.write(f"{owner_name, owners_colors}\n")
            ktory_nr_wolny[0]+=1
        lock.release()
        
        if owners_colors[owner_name] == 1:
            self.image = pygame.image.load(f"icons/{self.good_path('blue',sila)}.png").convert_alpha()
        if owners_colors[owner_name] == 2:
            self.image = pygame.image.load(f"icons/{self.good_path('green',sila)}.png").convert_alpha()
        if owners_colors[owner_name] == 3:
            self.image = pygame.image.load(f"icons/{self.good_path('red',sila)}.png").convert_alpha()
        if owners_colors[owner_name] == 4:
            self.image = pygame.image.load(f"icons/{self.good_path('white',sila)}.png").convert_alpha()
        if owners_colors[owner_name] == 5:
            self.image = pygame.image.load(f"icons/{self.good_path('yellow',sila)}.png").convert_alpha()
        
        if isFight:
            maxwidth = rec_width/2
            maxheight = 0.9*rec_height
            skala = min(maxheight/self.image.get_height(),maxwidth/self.image.get_width())

            self.image = pygame.transform.smoothscale(self.image,(self.image.get_width()*skala,self.image.get_height()*skala))
            self.rect = self.image.get_rect(center = srodek)
        else:
            new_srodek = srodek
            if withcoin:
                jc = 0.32#jaka czesc 1 - na skraju max, 0 - na srodku
                dl = promien*jc
                x = dl/math.tan(math.radians(60))
                new_srodek = (srodek[0]-x,srodek[1]+dl)

                dozy_promien = promien/math.cos(math.radians(60))
                maxwidth = 1.35*dozy_promien
                maxheight = 1.35*promien
                skala = min(maxheight/self.image.get_height(),maxwidth/self.image.get_width())
            else:
                jc = 0#jaka czesc 1 - na skraju max, 0 - na srodku
                dl = promien*jc
                x = dl/math.tan(math.radians(60))
                new_srodek = (srodek[0]-x,srodek[1]+dl)

                dozy_promien = promien/math.cos(math.radians(60))
                maxwidth = 1.75*dozy_promien
                maxheight = 1.75*promien
                skala = min(maxheight/self.image.get_height(),maxwidth/self.image.get_width())

            self.image = pygame.transform.smoothscale(self.image,(self.image.get_width()*skala,self.image.get_height()*skala))
            self.rect = self.image.get_rect(center = new_srodek)