import pygame,sys
from pygame.locals import *
from GUI_formulario_prueba import FormPrincipal
from constantes import *
import os

pygame.init()
pygame.display.set_caption("Robot Blaster Adventure")

RELOJ = pygame.time.Clock()
PANTALLA = pygame.display.set_mode((ANCHO_PANTALLA,ALTO_PANTALLA))
imagen_fondo = pygame.image.load(r"images/locations/FONDO.png")
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))

form_principal = FormPrincipal(PANTALLA, 0, 0, ANCHO_PANTALLA, ALTO_PANTALLA, imagen_fondo, (171, 1, 1))

pausa = pygame.image.load(r"menu_1\pause.png")
pausa = pygame.transform.scale(pausa,(ANCHO_PANTALLA,ALTO_PANTALLA))

ruta_sonido = os.path.join(r"sounds\ambiente", r"ambiente.wav")
sonido_ambiente = pygame.mixer.Sound(ruta_sonido)

canal_ambiente = pygame.mixer.Channel(0)
canal_ambiente.set_volume(0.1)
canal_ambiente.play(sonido_ambiente, loops=-1)

esta_en_pausa = False
flag = True
while flag:
    RELOJ.tick(FPS)
    lista_eventos = pygame.event.get()

    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            sonido_ambiente.stop()
            pygame.quit()
            sys.exit(0)
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                esta_en_pausa = not esta_en_pausa
                if esta_en_pausa:
                    canal_ambiente.pause()
                else:
                    canal_ambiente.unpause()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_TAB:
                cambiar_modo()
            
    PANTALLA.fill(ROJO)
    
    if not esta_en_pausa:
        form_principal.update(lista_eventos)
    else:
        PANTALLA.blit(pausa, (0,0))

    pygame.display.update()