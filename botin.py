import pygame
from constantes import *
from auxiliar import Auxiliar


class Objeto:
    '''
    Representa una gema en el juego que puede ser recolectada por el jugador.

    Args:
        x (int): Coordenada x inicial de la gema.
        y (int): Coordenada y inicial de la gema.
        width (int): Ancho de la gema.
        height (int): Alto de la gema.
        image_path (str): Ruta de la imagen de la gema.

    Atributos:
        image_list (list): Lista de imágenes de la gema en diferentes estados.
        image (pygame.Surface): Imagen actual de la gema.
        rect (pygame.Rect): Rectángulo de colisión de la gema.
    '''
    def __init__(self, x, y, width, height, image_path, nombre=""):
        '''
        Inicializa una instancia de la clase Gema.

        Carga la lista de imágenes de la gema y establece su rectángulo de colisión.

        Args:
            x (int): Coordenada x inicial de la gema.
            y (int): Coordenada y inicial de la gema.
            width (int): Ancho de la gema.
            height (int): Alto de la gema.
            image_path (str): Ruta de la imagen de la gema.
        '''
        self.image_list = Auxiliar.getSurfaceFromSeparateFiles(image_path, 1, 18, flip=False, w=width, h=height)
        self.image = self.image_list[0]  # Obtener la imagen de la lista
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.nombre = nombre

    def draw(self, screen):
        '''
        Dibuja la imagen de la gema en la pantalla.

        Args:
            screen: Superficie de la pantalla donde se dibujará la gema.
        '''
        screen.blit(self.image, self.rect)