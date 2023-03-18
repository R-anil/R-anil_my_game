# File created by Ryan Anil

# import libs
import pygame as pg
import random
import os
from random import randint
# test comment for git hub
# import settings 
from settings import *
from sprites import *
# from pg.sprite import Sprite

# set up assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

def get_mouse_now():
    x,y = pg.mouse.get_pos()
    return (x,y)


# init pg and create window
pg.init()
# init sound mixer
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My first game...")
clock = pg.time.Clock() 

all_sprites = pg.sprite.Group()
enemies = pg.sprite.Group()
pewpews = pg.sprite.Group()

# player is instantiated here
player = Player()
player.rect.x = 5
invader = MOB()
invader.image.fill((0,0,255))
invader.vel = vec(randint(1,8),randint(1,8))

for i in range (0,10):
    m = MOB()
    m.vel = invader.vel = vec(randint(10,50),randint(10,50))
    all_sprites.add(m)
    enemies.add(m)
# testSprite = Sprite()
# testSprite.image = pg.Surface((50,50))
# testSprite.image.fill(GREEN)
# testSprite.rect = testSprite.image.get_rect()
# testSprite.rect.center = (WIDTH / 2, HEIGHT / 2)
all_sprites.add(player)
all_sprites.add(invader)
# all_sprites.add(testSprite)

# game loop

while RUNNING:
    #  keep loop running at the right speed
    clock.tick(FPS)
    ### process input events section of game loop
    for event in pg.event.get():
        # check for window closing
        if event.type == pg.QUIT:
            RUNNING = False
            # break
    # print(get_mouse_now())
    ### update section of game loop (if updates take longer the 1/30th of a second, you will get laaaaag...)
    all_sprites.update()

    blocks_hit_list = pg.sprite.spritecollide(player, enemies, True)

    for block in blocks_hit_list:
        print(enemies)
        pass
    ### draw and render section of game loop
    screen.fill(BLUE)
    all_sprites.draw(screen)
    # double buffering draws frames for entire screen
    pg.display.flip()
    # pg.display.update() -> only updates a portion of the screen
# ends program when loops evaluates to false
pg.quit()