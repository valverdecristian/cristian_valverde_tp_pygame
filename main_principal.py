import pygame,sys
from pygame.locals import *
from GUI_formulario_prueba import FormPrincipal
from constantes import *

TAMAÑO_PANTALLA = list()

pygame.init()
pygame.display.set_caption("TP Juego Plataformas")

RELOJ = pygame.time.Clock()
PANTALLA = pygame.display.set_mode((ANCHO_PANTALLA,ALTO_PANTALLA))
imagen_fondo = pygame.image.load(r"menu_1\fondo_menu.jpg")
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))

form_principal = FormPrincipal(PANTALLA, 0, 0, ANCHO_PANTALLA, ALTO_PANTALLA, imagen_fondo, (171, 1, 1))

pausa = pygame.image.load(r"menu_1\pause.png")
pausa = pygame.transform.scale(pausa,(500,500))

is_paused = False
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
                is_paused = not is_paused
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_TAB:
                cambiar_modo()
            
    PANTALLA.fill("Black")
    
    if not is_paused:
        form_principal.update(lista_eventos)
    else:
        PANTALLA.blit(pausa, (200,100))   

    pygame.display.update()


