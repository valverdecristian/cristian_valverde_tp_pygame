import pygame
from pygame.locals import *
from constantes import *
from player import Player
from enemigo import Enemy
from plataforma import Plataform
from background import Background
from botin import Objeto
from auxiliar import Auxiliar
from class_healthBar import HealthBar
from class_chronometer import Chronometer
from manejador_banderas import *

class Level1():
    def __init__(self,w,h):

        # --- GAME ELEMNTS --- 
        self.cronometro = Chronometer(tiempo_inicial=60)
        self.last_update_time = pygame.time.get_ticks()
        self.static_background = Background(x=0,y=0,width=w,height=h,path="images/locations/all.png")

        self.player = Player(x=100,y=200,speed_walk=10,speed_run=12,gravity=14,jump_power=30,frame_rate_ms=100,move_rate_ms=50,jump_height=140,p_scale=0.2,interval_time_jump=300)
        self.barra_salud = HealthBar(200, 10, self.player.lives, self.player.lives)
        self.datos_obtenidos = Auxiliar.leer_json(ruta="niveles.json")

        self.enemy_list = list()
        self.enemy_list.append (Enemy(x=650,y=200,speed_walk=4,speed_run=5,gravity=14,jump_power=30,frame_rate_ms=150,move_rate_ms=50,jump_height=140,p_scale=0.24,interval_time_jump=300))
        self.enemy_list.append (Enemy(x=900,y=200,speed_walk=4,speed_run=5,gravity=14,jump_power=30,frame_rate_ms=150,move_rate_ms=50,jump_height=140,p_scale=0.24,interval_time_jump=300))
        self.plataform_list = list()
        self.objeto_list = list()
        self.bullet_list_player = list()
        self.flagenemy = False
        self.bullet_list_enemy = list()
        self.enemy_random = 0
        
        for coordenada in self.datos_obtenidos["primer_nivel"]["plataformas"]:
            x,y,width,height,type=coordenada
            self.plataform_list.append(Plataform(x,y,width,height,type, path_img="images/tileset/plataforma1.png"))

            gema = Objeto(x=x, y=y-80, width=30, height=30, image_path="images/objetos/gema1.png", nombre="gema")
            self.objeto_list.append(gema)
            
        for coordenada in self.datos_obtenidos["primer_nivel"]["salud"]:
            x,y,width,height = coordenada
            self.objeto_list.append(Objeto(x,y,width,height, image_path="images/objetos/salud.png", nombre="salud"))

    def update(self,lista_eventos):
        delta_ms = pygame.time.get_ticks() - self.last_update_time
        self.last_update_time = pygame.time.get_ticks()
        if self.bullet_list_player:
            for bullet in self.bullet_list_player:
                bullet.update(self, self.player, self.enemy_list, self.bullet_list_player)
        if self.bullet_list_enemy:
            for bullet in self.bullet_list_enemy:
                bullet.update(self, self.player,self.enemy_list,self.bullet_list_enemy)

        for enemy_element in self.enemy_list:
            enemy_element.update(delta_ms,self.plataform_list,self.bullet_list_enemy)
            
        if not self.enemy_list and self.enemy_random < 6:
            new_enemy = Enemy.generate_random_enemy()
            self.enemy_list.append(new_enemy)
            self.enemy_random +=1
            if self.enemy_random == 6:
                llave = Objeto(x=1000, y=550, width=70, height=100, image_path="images/objetos/keyBlue.png", nombre="llave")
                self.objeto_list.append(llave)
            
        for objeto in self.objeto_list:
            if self.player.rect.colliderect(objeto.rect):
                if objeto.nombre == "gema":
                    self.player.score += 100  # Aumentar el puntaje del jugador
                elif objeto.nombre == "salud":
                    if self.player.lives <= 8:
                        self.player.lives +=2
                    else:
                        self.player.lives +=1
                elif objeto.nombre == "llave":
                    self.guardar_partida()
                    modificar_banderas("nivel_1", "terminado", True)
                    modificar_banderas("nivel_1", "reset", True)
                self.objeto_list.remove(objeto)

        self.player.events(delta_ms,lista_eventos,self.bullet_list_player)
        self.player.update(delta_ms,self.plataform_list)
        self.cronometro.actualizar()
        
        for enemy in self.enemy_list:
            enemy.update(delta_ms,self.plataform_list,self.bullet_list_enemy)

    def draw(self, pantalla): 
        if leer_bandera("nivel_1", "reset"):
            print("Gano")
            imagen = pygame.image.load(r'images\menu\win.png')
            imagen_escalada = pygame.transform.scale(imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
            pantalla.blit(imagen_escalada, (0, 0))
        elif self.player.lives <= 0 or self.cronometro.tiempo_desendente <= 0 :
            print("perdio")
            imagen = pygame.image.load(r'images\menu\gameover.png')
            imagen_escalada = pygame.transform.scale(imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
            pantalla.blit(imagen_escalada, (0, 0))
        else:    
            self.static_background.draw(pantalla)

            for plataforma in self.plataform_list:
                plataforma.draw(pantalla)

            for enemy_element in self.enemy_list:
                enemy_element.draw(pantalla)
            
            self.player.draw(pantalla)
            self.barra_salud.draw(self.player.lives,pantalla)

            for bullet in self.bullet_list_player:
                bullet.draw(pantalla)
                
            for bullet in self.bullet_list_enemy:
                bullet.draw(pantalla)
                
            for objeto in self.objeto_list:
                objeto.draw(pantalla)
                
            self.cronometro.mostrar_tiempo(pantalla)
            
    def guardar_partida(self):
        with open("score.txt","w") as archivo:
            archivo.write(str(self.player.score))
            
# fin del nivel 1