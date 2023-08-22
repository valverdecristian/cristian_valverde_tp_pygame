import pygame
from constantes import *
from auxiliar import Auxiliar

class Background:
    '''
    Clase para representar un fondo en un juego utilizando Pygame.

    Attributes:
        x (int): La coordenada x de la esquina superior izquierda del fondo.
        y (int): La coordenada y de la esquina superior izquierda del fondo.
        width (int): Ancho del fondo.
        height (int): Alto del fondo.
        path (str): Ruta del archivo de imagen para el fondo.
    '''
    def __init__(self, x, y,width, height,  path):
        '''
        Constructor de la clase. Inicializa las propiedades del fondo.
        '''
        self.image = pygame.image.load(path).convert()
        self.image = pygame.transform.scale(self.image,(width,height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self,screen):
        '''
        Dibuja el fondo en la pantalla especificada.
        '''
        screen.blit(self.image,self.rect)
        if(DEBUG):
            pygame.draw.rect(screen,color=ROJO,rect=self.collition_rect)