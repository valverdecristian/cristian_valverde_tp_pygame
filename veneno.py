import pygame
from constantes import *
from auxiliar import Auxiliar

class Veneno:
    def __init__(self, x, y, width, height, image_path):
        self.image_list = Auxiliar.getSurfaceFromSeparateFiles(image_path, 1, 18, flip=False, w=width, h=height)
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)
