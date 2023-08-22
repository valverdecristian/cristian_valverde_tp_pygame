import pygame
from constantes import *

class HealthBar():
    '''
    Inicializa una instancia de la clase HealthBar.

        Parámetros:
        x (int): La coordenada x de la posición de la barra de salud en la pantalla.
        y (int): La coordenada y de la posición de la barra de salud en la pantalla.
        salud (int): La cantidad actual de salud.
        salud_maxima (int): La cantidad máxima de salud.
        
        Atributos:
        x (int): La coordenada x de la posición de la barra de salud.
        y (int): La coordenada y de la posición de la barra de salud.
        salud (int): La cantidad actual de salud.
        salud_maxima (int): La cantidad máxima de salud.
    '''
    def __init__(self, x, y, salud, salud_maxima):
        self.x = x
        self.y = y
        self.salud = salud
        self.salud_maxima = salud_maxima

    def draw(self, salud, pantalla):
        '''
        Dibuja la barra de salud en la pantalla.

        Parámetros:
        salud (int): La cantidad actual de salud.
        pantalla (Surface): La superficie de la pantalla en la que se dibujará la barra de salud.
        '''
        self.salud = salud
        proporcion_salud = self.salud / self.salud_maxima
        pygame.draw.rect(pantalla, NEGRO, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(pantalla, ROJO, (self.x, self.y, 150, 20))
        pygame.draw.rect(pantalla, VERDE, (self.x, self.y, 150 * proporcion_salud, 20))
