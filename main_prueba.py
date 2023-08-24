import pygame,sys
from pygame.locals import *
from nivel import Level1
from nivel_dos import Level2
from nivel_tres import Level3
from constantes import *

TAMAÑO_PANTALLA = (ANCHO_PANTALLA,ALTO_PANTALLA)

pygame.init()
pygame.display.set_caption("Robot Blaster Adventure")

RELOJ = pygame.time.Clock()
PANTALLA = pygame.display.set_mode(TAMAÑO_PANTALLA)
imagen_fondo = pygame.image.load(r"images/locations/FONDO.png")
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))

nivel_prueba = Level3(ANCHO_PANTALLA,ALTO_PANTALLA)

flag = True
while flag:
    RELOJ.tick(FPS)
    lista_eventos = pygame.event.get()

    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    
    nivel_prueba.update(lista_eventos)
    nivel_prueba.draw(pantalla=PANTALLA)

    pygame.display.update()