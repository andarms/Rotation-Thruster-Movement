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
        self.image = pg.transform.rotozoom(image, 90, prepare.SCALE_FACTOR)
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
        
        self.rect.center = self.pos
        # self.rect.move_ip(*move)
        self.rect.clamp_ip(bounding)

    def draw(self, surface):
        """
        Basic draw function. (not  used if drawing via groups)
        """
        surface.blit(self.image, self.rect)
