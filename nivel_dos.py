import pygame
from pygame.locals import *
from constantes import *
from player import Player
from enemigo import Enemy
from plataforma import Plataform
from background import Background
from bullet import Bullet
from botin import Objeto
from auxiliar import Auxiliar
from class_healthBar import HealthBar
from class_chronometer import Chronometer

class Level2():
    def __init__(self,w,h):

        # --- GAME ELEMNTS --- 
       
        self.last_update_time = pygame.time.get_ticks()
        self.cronometro = Chronometer(tiempo_inicial=60)
        self.static_background = Background(x=0,y=0,width=w,height=h,path="images/locations/set_bg_01/forest/all2.png")

        self.player_1 = Player(x=100,y=400,speed_walk=6,speed_run=12,gravity=14,jump_power=30,frame_rate_ms=100,move_rate_ms=50,jump_height=140,p_scale=0.2,interval_time_jump=300)
        self.barra_salud = HealthBar(200, 10, self.player_1.lives, 5)
        self.datos_obtenidos = Auxiliar.leer_json(ruta="niveles.json")

        self.enemy_list = list()
        self.enemy_list.append (Enemy(x=700,y=400,speed_walk=6,speed_run=5,gravity=14,jump_power=30,frame_rate_ms=150,move_rate_ms=50,jump_height=140,p_scale=0.08,interval_time_jump=300))
        self.enemy_list.append (Enemy(x=1100,y=400,speed_walk=6,speed_run=5,gravity=14,jump_power=30,frame_rate_ms=150,move_rate_ms=50,jump_height=140,p_scale=0.08,interval_time_jump=300))
        self.enemy_list.append (Enemy(x=900,y=200,speed_walk=6,speed_run=5,gravity=14,jump_power=30,frame_rate_ms=150,move_rate_ms=50,jump_height=140,p_scale=0.08,interval_time_jump=300))
        self.plataform_list = list()
        self.gema_list = list()
        self.veneno_list = list()
        
        for coordenada in self.datos_obtenidos["segundo_nivel"]["plataformas"]:
            x,y,width,height,type=coordenada
            self.plataform_list.append(Plataform(x,y,width,height,type))

            gema = Objeto(x=x, y=y-50, width=30, height=30, image_path="images/gema2.png")
            self.gema_list.append(gema)

        # lista de balas
        self.bullet_list = list()


    def update(self,lista_eventos):
        delta_ms = pygame.time.get_ticks() - self.last_update_time
        self.last_update_time = pygame.time.get_ticks()


        for bullet_element in self.bullet_list:
            print("dispara")
            bullet_element.update(delta_ms,self.plataform_list,self.enemy_list,self.player_1)

        for enemy_element in self.enemy_list:
            if self.player_1.rect.colliderect(enemy_element.rect):
                print("colisiono con el enemigo")
                self.enemy_list.remove(enemy_element)
            enemy_element.update(delta_ms,self.plataform_list)
            
        for gema_element in self.gema_list:
            if self.player_1.rect.colliderect(gema_element.rect):
                self.player_1.score += 100  # Aumentar el puntaje del jugador
                self.gema_list.remove(gema_element)  # Eliminar la gema

        self.player_1.events(delta_ms,lista_eventos)
        self.player_1.update(delta_ms,self.plataform_list)

        self.cronometro.actualizar()


    def draw(self, pantalla): 
        if self.player_1.lives <= 0 or self.cronometro.tiempo_desendente <= 0 :
            imagen = pygame.image.load(r'menu_1\gameover.png')
            imagen_escalada = pygame.transform.scale(imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
            pantalla.blit(imagen_escalada, (0, 0))
        else:    
            self.static_background.draw(pantalla)

            for plataforma in self.plataform_list:
                plataforma.draw(pantalla)

            for enemy_element in self.enemy_list:
                enemy_element.draw(pantalla)
            
            self.player_1.draw(pantalla)
            
            self.barra_salud.draw(self.player_1.lives,pantalla)

            for bullet_element in self.bullet_list:
                bullet_element.draw(pantalla)
                
            for gema_element in self.gema_list:
                gema_element.draw(pantalla)
            self.cronometro.mostrar_tiempo(pantalla)
