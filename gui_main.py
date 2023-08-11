import pygame
from pygame.locals import *
import sys
from constantes import *
from GUI_form import Form
from gui_form_menu_A import FormMenuA # pricipal
from gui_form_menu_B import FormMenuB
from gui_form_menu_C import FormMenuC
from gui_form_menu_game_l1 import FormGameLevel1

flags = DOUBLEBUF 
screen = pygame.display.set_mode((ANCHO_PANTALLA,ALTO_PANTALLA), flags, 16)
pygame.init()
clock = pygame.time.Clock()

form_game_L1 = FormGameLevel1(name="form_game_L1",master_surface = screen,x=0,y=0,w=ANCHO_PANTALLA,h=ALTO_PANTALLA,color_background=(0,255,255),color_border=(255,0,255),active=False)


while True:
    lista_eventos = pygame.event.get()
    for event in lista_eventos:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    delta_ms = clock.tick(FPS)

    aux_form_active = Form.get_active()
    if(aux_form_active != None):
        aux_form_active.update(lista_eventos,keys,delta_ms)
        aux_form_active.draw()

    pygame.display.flip()