"""
This module contains the Player class for the user controlled character.
"""
import math
import random

import pygame as pg

import prepare, tools

GRAD = math.pi/180
FRAGMENTMAXSPEED = 200

class Player(pg.sprite.Sprite):
    """
    This class represents our user controlled character.
    """
    def __init__(self, pos, image, speed=100, *groups):
        super(Player, self).__init__(*groups)
        self.speed = speed # px/seg
        self.max_speed = 600
        self.acc = 85 # px/s^2
        self.dec = 150
        self.angle = 90
        self.source_image = pg.transform.rotozoom(image, 0, prepare.SCALE_FACTOR)
        self.image = pg.transform.rotate(self.source_image, self.angle)
        self.rect = self.image.get_rect(center=pos)
        self.hit_rect = self.rect.inflate(-20, -20)
        self.hit_rect.center = self.rect.center
        self.pos = list(pos)
        self.dx = 0.0
        self.dy = 0.0

    def update(self, keys, bounding, obstacles, dt):
        """
        Updates the players position based on currently held keys.
        """
        for key in prepare.DIRECT_DICT:
            if keys[key]:
                self.dx = prepare.DIRECT_DICT[key][0]*math.cos(self.angle*GRAD)
                self.dy = prepare.DIRECT_DICT[key][1]*math.sin(self.angle*GRAD)
                Smoke(self.rect.center, -self.dy, -self.dx, self.gfx_group)
        

        if any((keys[pg.K_UP], keys[pg.K_DOWN], keys[pg.K_e], keys[pg.K_q])):
            if self.speed < self.max_speed:
                self.speed += self.acc * dt
        else:
            if self.speed > 100:
                self.speed -= self.dec * dt
            else:
                self.dx = 0.0
                self.dy = 0.0

        self.pos[0] += self.dx*self.speed*dt
        self.pos[1] += self.dy*self.speed*dt
        self.rect.center = self.pos

        rotate_factor = 0
        if keys[pg.K_LEFT]:
            rotate_factor += 1
        if keys[pg.K_RIGHT]:
            rotate_factor -= 1

        if rotate_factor != 0:
            self.angle += rotate_factor
            self.image = pg.transform.rotate(self.source_image, self.angle)
            self.rect = self.image.get_rect()
            self.rect.centerx = round(self.pos[0], 0)
            self.rect.centery = round(self.pos[1], 0)

        self.wrap_in_screen(bounding)
        self.check_collisions(obstacles)

    def check_collisions(self, obstacles):
        collision = pg.sprite.spritecollideany(self, obstacles, 
                                collided=tools.hit_rect_collision)
        if collision:
            for _ in range(50):
                RedFragment(self.pos, self.gfx_group)
            self.kill()

    def wrap_in_screen(self, bounding):
        buffer = 50
        if self.rect.centerx < bounding.left - buffer:
            self.rect.centerx = bounding.right + buffer
        elif self.rect.centerx > bounding.right + buffer:
            self.rect.centerx = bounding.left - buffer
        elif self.rect.centery < bounding.top - buffer:
            self.rect.centery = bounding.bottom + buffer
        elif self.rect.centery > bounding.bottom + buffer:
            self.rect.centery = bounding.top - buffer

        self.hit_rect.center = self.rect.center
        self.pos = list(self.rect.center)

    def draw(self, surface):
        """
        Basic draw function. (not  used if drawing via groups)
        """
        surface.blit(self.image, self.rect)

# Based on http://thepythongamebook.com/en:pygame:step017
class Fragment(pg.sprite.Sprite):
    """generic Fragment class. Use to generate Smoke and Expltions"""
    def __init__(self, pos, layer = 9, *groups):
        super(Fragment, self).__init__(*groups)
        self._layer = layer
        self.pos = [0.0,0.0]
        self.fragmentmaxspeed = FRAGMENTMAXSPEED# try out other factors !

    def init2(self):  # split the init method into 2 parts for better access from subclasses
        self.image = pg.Surface((10,10))
        self.image.set_colorkey((0,0,0)) # black transparent
        pg.draw.circle(self.image, self.color, (5,5), random.randint(2,5))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos #if you forget this line the sprite sit in the topleft corner
        self.time = 0.0
        
    def update(self, seconds):
        self.time += seconds
        if self.time > self.lifetime:
            self.kill() 
        self.pos[0] += self.dx * seconds
        self.pos[1] += self.dy * seconds
        self.rect.centerx = round(self.pos[0],0)
        self.rect.centery = round(self.pos[1],0)


class Smoke(Fragment):
    """black exhaust indicating that the Ship sprite is moved by
       the player. Exhaust direction is inverse of players movement direction"""
    def __init__(self, pos, dx, dy, *groups):
        super(Smoke, self).__init__(pos, 3, *groups)
        self.color = ( random.randint(125,250), random.randint(25,150), random.randint(1,50) )
        self.pos[0] = pos[0]
        self.pos[1] = pos[1]
        self.lifetime = 1 + random.random()*2
        Fragment.init2(self)
        self.smokespeed = 120.0
        self.smokearc = .3 # 0 = thin smoke stream, 1 = 180 Degrees
        arc = self.smokespeed * self.smokearc
        self.dx = dx * self.smokespeed + random.random()*2*arc - arc
        self.dy = dy * self.smokespeed + random.random()*2*arc - arc

class RedFragment(Fragment):
    """explodes outward from (killed) ship"""
    def __init__(self, pos, *groups):
        super(RedFragment, self).__init__(pos, 3, *groups)
        #red-only part -----------------------------
        self.color = (random.randint(25,255),0,0) # red     
        self.pos[0] = pos[0]
        self.pos[1] = pos[1]
        self.dx = random.randint(-self.fragmentmaxspeed,self.fragmentmaxspeed)
        self.dy = random.randint(-self.fragmentmaxspeed,self.fragmentmaxspeed)
        self.lifetime = 1 + random.random()*3 # max 3 seconds
        self.init2() # continue with generic Fragment class