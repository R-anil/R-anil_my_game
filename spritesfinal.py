# This file was created by: Ryan Anil
import pygame as pg
from pygame.sprite import Sprite
from settingsfinal import *
from random import randint
from random import randrange

vec = pg.math.Vector2

# player class
class Player(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        # these are the properties
        self.game = game
        self.image_orig = pg.transform.scale(game.player_img, (128, 128))
        self.image_orig.set_colorkey(WHITE)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.pos = vec(0, 0)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.cofric = 0.1
        self.canjump = False
        self.rot = 0
        self.rot_speed = 0
        self.last_update = pg.time.get_ticks()
        self.left_key = pg.K_a
    def input(self):
        keystate = pg.key.get_pressed()
        # if keystate[pg.K_w]:
        #     self.acc.y = -PLAYER_ACC
        if keystate[self.left_key]:
            self.acc.x = -PLAYER_ACC
            self.rot_speed = 8
        # if keystate[pg.K_s]:
        #     self.acc.y = PLAYER_ACC
        if keystate[pg.K_d]:
            self.acc.x = PLAYER_ACC
            self.rot_speed = -8
        # if keystate[pg.K_p]:
        #     if PAUSED == False:
        #         PAUSED = True
        #         print(PAUSED)
        #     else:
        #         PAUSED = False
        #         print(PAUSED)
    # the player can rotate
    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 30:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pg.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
    # Allows the player to jump when bellarman is upright 
    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits and self.canjump:
            self.vel.y = -PLAYER_JUMP
    # boundaries
    def inbounds(self):
        if self.rect.x > WIDTH - 50:
            self.pos.x = WIDTH - 25
            self.vel.x = 0
            print("i am off the right side of the screen...")
        if self.rect.x < 0:
            self.pos.x = 25
            self.vel.x = 0
            print("i am off the left side of the screen...")
        if self.rect.y > HEIGHT:
            print("i am off the bottom of the screen")
        if self.rect.y < 0:
            print("i am off the top of the screen...")
    def mob_collide(self):
            hits = pg.sprite.spritecollide(self, self.game.enemies, True)
            if hits:
                print("you collided with an enemy...")
                self.game.score += 1
                print(SCORE)
    def update(self):
        self.rot_speed = 0
        if self.rot > 312 or self.rot < 56:
            self.canjump = True
        else:
            self.canjump = False
        self.acc = vec(0, PLAYER_GRAV)
        self.acc.x = self.vel.x * PLAYER_FRICTION
        self.input()
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rotate()
        self.rect.midbottom = self.pos
#  Enemy class
class Mob(Sprite):
    def __init__(self, game, width,height, color):
        Sprite.__init__(self)
        # properties
        self.game = game
        self.width = width
        self.height = height
        self.image = pg.Surface((self.width,self.height))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(randint(1,5),randint(1,5))
        self.acc = vec(1,1)
        # self.pos = vec(100, 100)
        # self.vel = vec(0,0)
        # self.acc = vec(1,1)
        self.cofric = 0.01
        print(self.vel.x)
        print(self.vel.y)
    # # makes the mob jump
    # def jump(self):
    #     hits = pg.sprite.spritecollide(self, self.game.platforms, False)
    #     if hits:
    #         if self.vel.y > 1:
    #             self.vel = vec(30,-10)
    #             print(self.vel.y)
    #         else:
    #             self.pos.y = hits[0].rect.top
    #             self.vel.y = 0
    #     else:
    #         self.vel.x = 0
    def inbounds(self):
        if self.rect.x > WIDTH:
            self.vel.x *= -1
            # self.acc = self.vel * -self.cofric
        if self.rect.x < 0:
            self.vel.x *= -1
            # self.acc = self.vel * -self.cofric
        if self.rect.y < 0:
            self.vel.y *= -1
            # self.acc = self.vel * -self.cofric
        if self.rect.y > HEIGHT:
            self.vel.y *= -1
            # self.acc = self.vel * -self.cofric
    def update(self):
        self.inbounds()
        # self.pos.x += self.vel.x
        # self.pos.y += self.vel.y
        self.pos += self.vel
        self.rect.center = self.pos
        # self.acc = vec(0, PLAYER_GRAV)
        # # self.jump()
        # self.acc.x = self.vel.x * PLAYER_FRICTION
        # self.vel += self.acc
        # self.pos += self.vel + 0.5 * self.acc
        # self.rect.midbottom = self.pos

# create a new platform class...
class Platform(Sprite):
    def __init__(self, x, y, width, height, color, variant):
        Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = pg.Surface((self.width,self.height))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.variant = variant
    
# # This is a platform that can move
# class MovingPlatform(Sprite):
#     def __init__(self, x, y, width, height, color,):
#         Sprite.__init__(self)
#         self.width = width
#         self.height = height
#         self.image = pg.Surface ((self.width,self.height))
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#     def update(self):
#         # Move left or right
#         self.rect.x += self.change_x
#         # if player is hit
#         hit = pg.sprite.collide_rect(self, self.player)
#         if hit:
#             # if moving to the right, have the right side set to the left side of the object we hit
#             if self.change_x < 0:
#                 self.player.rect.right = self.rect.left
#             else:
#                 # otherwise, do the opposite
#                 self.player.rect.left = self.rect.right

#         # Move up/down
#         self.rect.y += self.change_y
#         hit = pg.sprite.collide_rect(self, self.player)
#         if hit:
#             if self.change_y < 0:
#                 self.player.rect.right = self.rect.left
#             else:
#                 self.player.rect.left = self.rect.right
#         if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
#             self.change_y *= -1
#         cur_pos = self.rect.x - self.level.world_shift
#         if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
#             self.change_x *= -1

    
