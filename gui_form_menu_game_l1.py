import pygame
from pygame.locals import *
from constantes import *

from player import Player
from enemigo import Enemy
from plataforma import Plataform
from background import Background
from bullet import Bullet
from botin import Gema
from auxiliar import Auxiliar

class Level1():
    def __init__(self,name,master_surface,x,y,w,h,color_background,color_border,active):
        super().__init__(name,master_surface,x,y,w,h,color_background,color_border,active)

        # lista de elementos en pantalla
        self.widget_list = [self.boton1,self.boton2,self.pb_lives]

        # --- GAME ELEMNTS --- 
        self.static_background = Background(x=0,y=0,width=w,height=h,path="images/locations/set_bg_01/forest/all.png")

        self.player_1 = Player(x=100,y=400,speed_walk=6,speed_run=12,gravity=14,jump_power=30,frame_rate_ms=100,move_rate_ms=50,jump_height=140,p_scale=0.2,interval_time_jump=300)

        self.datos_obtenidos = Auxiliar.leer_json(ruta="niveles.json")

        self.enemy_list = []
        self.enemy_list.append (Enemy(x=600,y=400,speed_walk=6,speed_run=5,gravity=14,jump_power=30,frame_rate_ms=150,move_rate_ms=50,jump_height=140,p_scale=0.08,interval_time_jump=300))
        self.enemy_list.append (Enemy(x=1200,y=400,speed_walk=6,speed_run=5,gravity=14,jump_power=30,frame_rate_ms=150,move_rate_ms=50,jump_height=140,p_scale=0.08,interval_time_jump=300))
        self.enemy_list.append (Enemy(x=900,y=200,speed_walk=6,speed_run=5,gravity=14,jump_power=30,frame_rate_ms=150,move_rate_ms=50,jump_height=140,p_scale=0.08,interval_time_jump=300))

        self.plataform_list = []
        self.gema_list = []
        
        for coordenada in self.datos_obtenidos["primer_nivel"]["plataformas"]:
            x,y,width,height,type=coordenada
            self.plataform_list.append(Plataform(x,y,width,height,type))

            gema = Gema(x=x, y=y-50, width=30, height=30, image_path="images/gema.png")
            self.gema_list.append(gema)

        self.bullet_list = []


    def update(self, lista_eventos,keys,delta_ms):
        for aux_widget in self.widget_list:
            aux_widget.update(lista_eventos)

        for bullet_element in self.bullet_list:
            bullet_element.update(delta_ms,self.plataform_list,self.enemy_list,self.player_1)

        for enemy_element in self.enemy_list:
            enemy_element.update(delta_ms,self.plataform_list)
            
        for gema_element in self.gema_list:
            if self.player_1.rect.colliderect(gema_element.rect):
                self.player_1.score += 100  # Aumentar el puntaje del jugador
                self.gema_list.remove(gema_element)  # Eliminar la gema

        self.player_1.events(delta_ms,keys)
        self.player_1.update(delta_ms,self.plataform_list)

        self.pb_lives.value = self.player_1.lives 


    def draw(self): 
        super().draw()
        self.static_background.draw(self.surface)

        for aux_widget in self.widget_list:    
            aux_widget.draw()

        for plataforma in self.plataform_list:
            plataforma.draw(self.surface)

        for enemy_element in self.enemy_list:
            enemy_element.draw(self.surface)
        
        self.player_1.draw(self.surface)

        for bullet_element in self.bullet_list:
            bullet_element.draw(self.surface)
            
        for gema_element in self.gema_list:
            gema_element.draw(self.surface)