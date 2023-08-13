import pygame
from constantes import *
from auxiliar import Auxiliar
from bullet import Bullet

class Player:
    def __init__(self,x,y,speed_walk,speed_run,gravity,jump_power,frame_rate_ms,move_rate_ms,jump_height,p_scale=1,interval_time_jump=100) -> None:

        self.stay_r = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/robot/Idle ({0}).png",1,10,flip=False,scale=p_scale)
        self.stay_l = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/robot/Idle ({0}).png",1,10,flip=True,scale=p_scale)
        self.jump_r = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/robot/Jump ({0}).png",1,10,flip=False,scale=p_scale)
        self.jump_l = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/robot/Jump ({0}).png",1,10,flip=True,scale=p_scale)
        self.walk_r = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/robot/Run ({0}).png",1,8,flip=False,scale=p_scale)
        self.walk_l = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/robot/Run ({0}).png",1,8,flip=True,scale=p_scale)
        self.shoot_r = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/robot/Shoot ({0}).png",1,3,flip=False,scale=p_scale,repeat_frame=2)
        self.shoot_l = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/robot/Shoot ({0}).png",1,3,flip=True,scale=p_scale,repeat_frame=2)
        self.knife_r = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/robot/Melee ({0}).png",1,7,flip=False,scale=p_scale,repeat_frame=1)
        self.knife_l = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/robot/Melee ({0}).png",1,7,flip=True,scale=p_scale,repeat_frame=1)

        self.frame = 0
        self.lives = 5
        self.score = 0
        self.move_x = 0
        self.move_y = 0
        self.speed_walk =  speed_walk
        self.speed_run =  speed_run
        self.gravity = gravity
        self.jump_power = jump_power
        self.animation = self.stay_r
        self.direction = DIRECTION_R
        self.image = self.animation[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collition_rect = pygame.Rect(x+self.rect.width/3,y,self.rect.width/3,self.rect.height)
        self.ground_collition_rect = pygame.Rect(self.collition_rect)
        self.ground_collition_rect.height = GROUND_COLLIDE_H
        self.ground_collition_rect.y = y + self.rect.height - GROUND_COLLIDE_H

        self.is_jump = False
        self.is_fall = False
        self.is_shoot = False
        self.is_knife = False

        self.tiempo_transcurrido_animation = 0
        self.frame_rate_ms = frame_rate_ms 
        self.tiempo_transcurrido_move = 0
        self.move_rate_ms = move_rate_ms
        self.y_start_jump = 0
        self.jump_height = jump_height

        self.tiempo_transcurrido = 0
        self.tiempo_last_jump = 0 # en base al tiempo transcurrido general
        self.interval_time_jump = interval_time_jump
        self.bullet_list = list()

    def walk(self,direction):
        if(self.is_jump == False and self.is_fall == False):
            if(self.direction != direction or (self.animation != self.walk_r and self.animation != self.walk_l)):
                self.frame = 0
                self.direction = direction
                if(direction == DIRECTION_R):
                    self.move_x = self.speed_walk
                    self.animation = self.walk_r
                else:
                    self.move_x = -self.speed_walk
                    self.animation = self.walk_l
                    
    def shoot_bullet(self):
        bullet_speed = 10  # Velocidad de la bala
        bullet_path = "images\caracters\players\robot\Objects\Bullet_000.png"  # Ruta de la imagen de la bala
        target_x = self.rect.x + self.rect.width  # Coordenada x del objetivo (por ejemplo, frente al jugador)
        target_y = self.rect.y + self.rect.height / 2  # Coordenada y del objetivo (por ejemplo, altura media del jugador)
        frame_rate_ms = 100  # Tasa de cuadro de la animación de la bala
        move_rate_ms = 50  # Tasa de movimiento de la bala
        bullet = Bullet(self, self.rect.x, self.rect.y, target_x, target_y, bullet_speed, bullet_path, frame_rate_ms, move_rate_ms)
        self.bullet_list.append(bullet)

    def shoot(self,on_off = True):
        self.is_shoot = on_off
        if(on_off == True and self.is_jump == False and self.is_fall == False):

            if(self.animation != self.shoot_r and self.animation != self.shoot_l):
                self.frame = 0
                self.is_shoot = True
                if(self.direction == DIRECTION_R):
                    self.animation = self.shoot_r
                else:
                    self.animation = self.shoot_l       

    def receive_shoot(self):
        self.lives -= 1
        self.score += 100

    def knife(self,on_off = True):
        self.is_knife = on_off
        if(on_off == True and self.is_jump == False and self.is_fall == False):
            if(self.animation != self.knife_r and self.animation != self.knife_l):
                self.frame = 0
                if(self.direction == DIRECTION_R):
                    self.animation = self.knife_r
                else:
                    self.animation = self.knife_l      

    def jump(self,on_off = True):
        if(on_off and self.is_jump == False and self.is_fall == False):
            self.y_start_jump = self.rect.y
            if(self.direction == DIRECTION_R):
                self.move_x = int(self.move_x / 2)
                self.move_y = -self.jump_power
                self.animation = self.jump_r
            else:
                self.move_x = int(self.move_x / 2)
                self.move_y = -self.jump_power
                self.animation = self.jump_l
            self.frame = 0
            self.is_jump = True
        if(on_off == False):
            self.is_jump = False
            self.stay()

    def stay(self):
        if self.is_knife or self.is_shoot:
            return

        if self.animation != self.stay_r and self.animation != self.stay_l:
            if(self.direction == DIRECTION_R):
                self.animation = self.stay_r
            else:
                self.animation = self.stay_l
            self.move_x = 0
            self.move_y = 0
            self.frame = 0

    def change_x(self,delta_x):
        self.rect.x += delta_x
        self.collition_rect.x += delta_x
        self.ground_collition_rect.x += delta_x

    def change_y(self,delta_y):
        self.rect.y += delta_y
        self.collition_rect.y += delta_y
        self.ground_collition_rect.y += delta_y

    def do_movement(self,delta_ms,plataform_list):
        self.tiempo_transcurrido_move += delta_ms
        if(self.tiempo_transcurrido_move >= self.move_rate_ms):
            self.tiempo_transcurrido_move = 0

            if(abs(self.y_start_jump - self.rect.y) > self.jump_height and self.is_jump):
                self.move_y = 0
          
            self.change_x(self.move_x)
            self.change_y(self.move_y)

            if(not self.is_on_plataform(plataform_list)):
                if(self.move_y == 0):
                    self.is_fall = True
                    self.change_y(self.gravity)
            else:
                if (self.is_jump): 
                    self.jump(False)
                self.is_fall = False            

    def is_on_plataform(self,plataform_list):
        retorno = False
        
        if(self.ground_collition_rect.bottom >= GROUND_LEVEL):
            retorno = True     
        else:
            for plataforma in  plataform_list:
                if(self.ground_collition_rect.colliderect(plataforma.ground_collition_rect)):
                    retorno = True
                    break       
        return retorno                 

    def do_animation(self,delta_ms):
        self.tiempo_transcurrido_animation += delta_ms
        if(self.tiempo_transcurrido_animation >= self.frame_rate_ms):
            self.tiempo_transcurrido_animation = 0
            if(self.frame < len(self.animation) - 1):
                self.frame += 1 
                #print(self.frame)
            else: 
                self.frame = 0
 
    def update(self,delta_ms,plataform_list):
        for bullet in self.bullet_list:
            bullet.update(delta_ms, plataform_list)
        self.do_movement(delta_ms,plataform_list)
        self.do_animation(delta_ms)
        
    
    def draw(self,screen):
        
        if(DEBUG):
            pygame.draw.rect(screen,color=(255,0 ,0),rect=self.collition_rect)
            pygame.draw.rect(screen,color=(255,255,0),rect=self.ground_collition_rect)
        
        self.image = self.animation[self.frame]
        screen.blit(self.image,self.rect)
        
        # Mostrar puntaje en la pantalla
        font = pygame.font.SysFont(None, 36)
        score_text = font.render("Score: " + str(self.score), True, BLANCO)
        screen.blit(score_text, (10, 10))
        
        # for bullet in self.bullet_list:
        #     bullet.draw(screen)
        
    def events(self, delta_ms, lista_eventos):
        keys = dict()
        
        self.tiempo_transcurrido += delta_ms
        
        if keys.get(pygame.K_s, False) and not keys.get(pygame.K_a, False):
            self.shoot_bullet()

        for event in lista_eventos:
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                keys[event.key] = event.type == pygame.KEYDOWN

            if (keys.get(pygame.K_LEFT, False) and not keys.get(pygame.K_RIGHT, False)):
                self.walk(DIRECTION_L)

            if (not keys.get(pygame.K_LEFT, False) and keys.get(pygame.K_RIGHT, False)):
                self.walk(DIRECTION_R)

            if (not keys.get(pygame.K_LEFT, False) and not keys.get(pygame.K_RIGHT, False) and not keys.get(pygame.K_SPACE, False)):
                self.stay()

            if (keys.get(pygame.K_LEFT, False) and keys.get(pygame.K_RIGHT, False) and not keys.get(pygame.K_SPACE, False)):
                self.stay()

            if (keys.get(pygame.K_SPACE, False)):
                if ((self.tiempo_transcurrido - self.tiempo_last_jump) > self.interval_time_jump):
                    self.jump(True)
                    self.tiempo_last_jump = self.tiempo_transcurrido

            if (not keys.get(pygame.K_a, False)):
                self.shoot(False)

            if (not keys.get(pygame.K_a, False)):
                self.knife(False)

            if (keys.get(pygame.K_s, False) and not keys.get(pygame.K_a, False)):
                self.shoot()

            if (keys.get(pygame.K_a, False) and not keys.get(pygame.K_s, False)):
                self.knife()
