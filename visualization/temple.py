import pygame
import math

class Temple(pygame.sprite.Sprite):
    def __init__(self,srodek,promien,czy_sam):#0 - rysuj na srodku, 1 - rysuj w lewnym dolnym, 2 - rysuj w prawym gornym
        super().__init__()
        self.image = pygame.image.load(f"icons/temple.png").convert_alpha()
        
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



        self.image = pygame.transform.smoothscale(self.image,(self.image.get_width()*skala,self.image.get_height()*skala))

        self.rect = self.image.get_rect(center = new_srodek)