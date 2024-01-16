import pygame
from threading import Lock

sprites = pygame.sprite.Group()
owners_colors={}
ktory_nr_wolny = [1]
ktory_wyglad_monety={}
lock = Lock()