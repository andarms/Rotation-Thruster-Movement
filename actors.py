"""
This module contains the Player class for the user controlled character.
"""
import math

import pygame as pg

import prepare

GRAD = math.pi/180
class Player(pg.sprite.Sprite):
    """
    This class represents our user controlled character.
    """
    def __init__(self, pos, image, speed=100, *groups):
        super(Player, self).__init__(*groups)
        self.speed = speed # px/seg
        self.max_speed = 700
        self.acc = 85 # px/s^2
        self.dec = 150
        self.angle = 90
        self.source_image = pg.transform.rotozoom(image, 0, prepare.SCALE_FACTOR)
        self.image = pg.transform.rotate(self.source_image, self.angle)
        self.rect = self.image.get_rect(center=pos)
        self.pos = list(pos)
        self.dx = 0
        self.dy = 0

    def update(self, keys, bounding, dt):
        """
        Updates the players position based on currently held keys.
        """

        for key in prepare.DIRECT_DICT:
            if keys[key]:
                self.dx = prepare.DIRECT_DICT[key][0]*math.cos(self.angle*GRAD)
                self.dy = prepare.DIRECT_DICT[key][1]*math.sin(self.angle*GRAD)
        

        if any((keys[pg.K_UP], keys[pg.K_DOWN], keys[pg.K_e], keys[pg.K_q])):
            if self.speed < self.max_speed:
                self.speed += self.acc * dt
        else:
            if self.speed > 100:
                self.speed -= self.dec * dt
            else:
                self.dx = 0.0
                self.dy = 0.0



        # print dx*self.speed*dt


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

        # clampin the ship in the screen
        self.rect.clamp_ip(bounding)

    def draw(self, surface):
        """
        Basic draw function. (not  used if drawing via groups)
        """
        surface.blit(self.image, self.rect)
