import pygame
from constantes import *

class Chronometer:
    def __init__(self, tiempo_inicial) -> None:
        '''
        Inicializa una instancia de la clase Chronometer.

        Parámetros:
        tiempo_inicial (int): El tiempo inicial en segundos para el cronómetro.

        Atributos:
        tiempo_desendente (int): El tiempo descendente actual del cronómetro.
        minutos (int): Los minutos actuales del cronómetro.
        fuente (Font): La fuente utilizada para renderizar el texto del cronómetro.
        tiempo_actual (int): El tiempo en milisegundos desde que se inició el cronómetro.
        detenido (bool): Indica si el cronómetro está detenido o no.
        color (tuple): El color del texto del cronómetro.
        '''
        self.tiempo_desendente = tiempo_inicial
        self.minutos = 0
        self.fuente = pygame.font.SysFont("Forte", 40)
        self.tiempo_actual = pygame.time.get_ticks()
        self.detenido = False
        self.color = BLANCO

    def actualizar(self):
        '''
        Actualiza el cronómetro si no está detenido.

        Calcula el tiempo transcurrido desde la última actualización y reduce el tiempo descendente en consecuencia.
        '''
        if self.detenido == False:
            tiempo_transcurrido = pygame.time.get_ticks() - self.tiempo_actual
            if tiempo_transcurrido >= 1000:
                self.tiempo_actual = pygame.time.get_ticks()
                self.tiempo_desendente -= 1

    def mostrar_tiempo(self, pantalla):
        '''
        Muestra el tiempo del cronómetro en la pantalla.

        Parámetros:
        pantalla (Surface): La superficie de la pantalla en la que se mostrará el cronómetro.
        '''
        cronometro = self.fuente.render(f"0{self.minutos} : {str(self.tiempo_desendente).zfill(2)}", False, self.color)
        pantalla.blit(cronometro, (870, 6))

    def get_tiempo(self)-> int:
        '''
        Devuelve el tiempo descendente actual del cronómetro.

        Retorna:
        int: El tiempo descendente actual en segundos.
        '''
        return self.tiempo_desendente
