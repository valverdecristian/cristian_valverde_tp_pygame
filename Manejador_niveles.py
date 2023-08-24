from pygame.locals import*
from nivel import Level1
from nivel_dos import Level2
from nivel_tres import Level3
from constantes import *

class Manejador_niveles:
    def __init__(self, pantalla) -> None:
        self._slave = pantalla
        self.nivel = None
       
    def get_nivel_1(self):
        self.nivel = Level1(ANCHO_PANTALLA,ALTO_PANTALLA)
        return self.nivel

    def get_nivel_2(self):
        self.nivel = Level2(ANCHO_PANTALLA,ALTO_PANTALLA)
        return self.nivel

    def get_nivel_3(self):
        self.nivel = Level3(ANCHO_PANTALLA,ALTO_PANTALLA)
        return self.nivel