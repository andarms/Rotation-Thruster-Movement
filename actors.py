"""
This module contains the Player class for the user controlled character.
"""

import pygame as pg

import prepare


class Player(pg.sprite.Sprite):
    """
    This class represents our user controlled character.
    """
    def __init__(self, pos, image, speed=300, *groups):
        super(Player, self).__init__(*groups)
        self.speed = speed # px/seg
        self.angle = 90
        self.source_image = pg.transform.rotozoom(image, 0.0, prepare.SCALE_FACTOR)
        self.image = pg.transform.rotate(self.source_image, self.angle)
        self.rect = self.image.get_rect(center=pos)
        self.pos = list(pos)

    def update(self, keys, bounding, dt):
        """
        Updates the players position based on currently held keys.
        """

        for key in prepare.DIRECT_DICT:
            if keys[key]:
                self.pos[0] += prepare.DIRECT_DICT[key][0]*self.speed*dt
                self.pos[1] += prepare.DIRECT_DICT[key][1]*self.speed*dt

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

        
        self.rect.center = self.pos
        self.rect.clamp_ip(bounding)

    def draw(self, surface):
        """
        Basic draw function. (not  used if drawing via groups)
        """
        surface.blit(self.image, self.rect)
