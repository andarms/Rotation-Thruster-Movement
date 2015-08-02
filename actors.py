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
    def __init__(self, pos, image, speed=300, *groups):
        super(Player, self).__init__(*groups)
        self.speed = speed # px/seg
        self.angle = 90
        self.source_image = pg.transform.rotozoom(image, 0, prepare.SCALE_FACTOR)
        self.image = pg.transform.rotate(self.source_image, self.angle)
        self.rect = self.image.get_rect(center=pos)
        self.pos = list(pos)

    def update(self, keys, bounding, dt):
        """
        Updates the players position based on currently held keys.
        """
        dx = dy = 0.0
        for key in prepare.DIRECT_DICT:
            if keys[key]:
                dx = prepare.DIRECT_DICT[key][0]*math.cos(self.angle*GRAD)
                dy = prepare.DIRECT_DICT[key][1]*math.sin(self.angle*GRAD)

        self.pos[0] += dx*self.speed*dt
        self.pos[1] += dy*self.speed*dt
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
