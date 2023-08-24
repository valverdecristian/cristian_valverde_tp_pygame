import pygame,sys
from pygame.locals import *
from GUI_formulario_prueba import FormPrincipal
from constantes import *

pygame.init()
pygame.display.set_caption("Robot Blaster Adventure")

RELOJ = pygame.time.Clock()
PANTALLA = pygame.display.set_mode((ANCHO_PANTALLA,ALTO_PANTALLA))
imagen_fondo = pygame.image.load(r"images/locations/FONDO.png")
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))

form_principal = FormPrincipal(PANTALLA, 0, 0, ANCHO_PANTALLA, ALTO_PANTALLA, imagen_fondo, (171, 1, 1))

pausa = pygame.image.load(r"images\menu\pause.png")
pausa = pygame.transform.scale(pausa,(ANCHO_PANTALLA,ALTO_PANTALLA))

esta_en_pausa = False
musica_en_pausa = False
flag = True
while flag:
    RELOJ.tick(FPS)
    lista_eventos = pygame.event.get()

    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                esta_en_pausa = not esta_en_pausa
                if esta_en_pausa:
                    pygame.mixer.music.pause()
                    musica_en_pausa = True
                else:
                    musica_en_pausa = False
                    pygame.mixer.music.unpause()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_TAB:
                cambiar_modo()
            
    PANTALLA.fill(ROJO)
    
    if not esta_en_pausa:
        form_principal.update(lista_eventos)
    else:
        PANTALLA.blit(pausa, (0,0))

    pygame.display.update()