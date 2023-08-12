import pygame,sys
from pygame.locals import *
from nivel import Level1
from nivel_dos import Level2
from nivel_tres import Level3
from constantes import *
# PANTALLA
TAMAÑO_PANTALLA = (ANCHO_PANTALLA,ALTO_PANTALLA)

# INICIAMOS PYGAME
pygame.init()
pygame.display.set_caption("Platform shooter")

RELOJ = pygame.time.Clock()
PANTALLA = pygame.display.set_mode(TAMAÑO_PANTALLA)
imagen_fondo = pygame.image.load(r"menu_1\fondo_menu.jpg")

imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))

nivel_uno = Level3(ANCHO_PANTALLA,ALTO_PANTALLA)

flag = True
while flag:
    RELOJ.tick(FPS)
    lista_eventos = pygame.event.get()

    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    
    nivel_uno.update(lista_eventos)
    nivel_uno.draw(pantalla=PANTALLA)

    pygame.display.update()