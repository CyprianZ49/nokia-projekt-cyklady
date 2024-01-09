import pygame
import math

class Structure(pygame.sprite.Sprite):
    def __init__(self,structure_type,srodek,promien,czy_sam):#0 - rysuj na srodku, 1 - rysuj w lewnym dolnym, 2 - rysuj w prawym gornym, 3 - wersja stolicowa
        super().__init__()
        if structure_type == 1:
            self.image = pygame.image.load(f"icons/university.png").convert_alpha()
        if structure_type == 2:
            self.image = pygame.image.load(f"icons/temple.png").convert_alpha()
        if structure_type == 3:
            self.image = pygame.image.load(f"icons/fortress.png").convert_alpha()
        if structure_type == 4:
            self.image = pygame.image.load(f"icons/port.png").convert_alpha()
        if structure_type == 5:
            self.image = pygame.image.load(f"icons/metropolis.png").convert_alpha()
            
        
        new_srodek = srodek
        if czy_sam==1:
            jc = 0.45#jaka czesc 1 - na skraju max, 0 - na srodku
            dl = promien*jc
            x = dl/math.tan(math.radians(60))
            new_srodek = (srodek[0]+x,srodek[1]-dl)

            dozy_promien = promien/math.cos(math.radians(60))
            maxwidth = dozy_promien*1.07
            maxheight = promien*1.07
            skala = min(maxheight/self.image.get_height(),maxwidth/self.image.get_width())
            # print(maxheight,self.image.get_height())
        
        if czy_sam==2:
            jc = 0.45#jaka czesc 1 - na skraju max, 0 - na srodku
            dl = promien*jc
            x = dl/math.tan(math.radians(60))
            new_srodek = (srodek[0]-x,srodek[1]+dl)

            dozy_promien = promien/math.cos(math.radians(60))
            maxwidth = dozy_promien*1.07
            maxheight = promien*1.07
            skala = min(maxheight/self.image.get_height(),maxwidth/self.image.get_width())

        if czy_sam==0:
            dozy_promien = promien/math.cos(math.radians(60))
            maxwidth = dozy_promien*1.75
            maxheight = promien*1.75
            skala = min(maxheight/self.image.get_height(),maxwidth/self.image.get_width())
        
        if czy_sam==3:
            # print("xd")
            jc = 0.6#jaka czesc 1 - na skraju max, 0 - na srodku
            dozy_promien = promien/math.sin(math.radians(60))
            x = dozy_promien*jc
            new_srodek = (srodek[0]-x,srodek[1])

            maxwidth = dozy_promien*0.8
            maxheight = promien*0.8
            skala = min(maxheight/self.image.get_height(),maxwidth/self.image.get_width())



        self.image = pygame.transform.smoothscale(self.image,(self.image.get_width()*skala,self.image.get_height()*skala))

        self.rect = self.image.get_rect(center = new_srodek)