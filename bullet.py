from constantes import *
from enemigo import Enemy

class Bullet2:
    def __init__(self, x, y, direction, image_bullet):
        self.x = x
        self.y = y
        self.velocidad = 10
        self.image = image_bullet
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self, nivel_actual, player, enemy_list, bullet_list):
        self.x += (self.direction * self.velocidad)
        self.rect.x = self.x

        if self.x < 0 or self.x > ANCHO_PANTALLA:
            bullet_list.remove(self)


        for obstacle in nivel_actual.plataform_list:
            if self.rect.colliderect(obstacle.rect) and self in bullet_list:
                bullet_list.remove(self)

        for bullet in bullet_list:
            if bullet != self and self.rect.colliderect(bullet.rect):
                #bullet_list.remove(self)
                bullet_list.remove(bullet)

        if player.rect.colliderect(self.rect):
            if player.lives > 0:
                player.lives -= 1
                bullet_list.remove(self)

        for enemy in enemy_list:
            if enemy.rect.colliderect(self.rect):
                if enemy.lives > 0:
                    enemy.lives -= 1
                if enemy.lives == 0:
                    player.score += 200
                    enemy_list.remove(enemy)
                    # new_enemy = Enemy.generate_random_enemy()
                    # enemy_list.append(new_enemy)
                if self in bullet_list:
                    bullet_list.remove(self)

    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)

