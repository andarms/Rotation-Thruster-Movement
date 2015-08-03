import itertools
import pygame as pg
import prepare

class Loop(object):
    def __init__(self, sheet, size, fps, rows, columns, missing=0):
        self.delay = 1.0/fps
        self.accumulator = 0.0
        self.frames = self.make_cycle(sheet, size, rows, columns, missing)
        self.frame = None
        self.get_next()

    def make_cycle(self, sheet, size, rows, columns, missing=0):
        subsurfaces = []
        total = rows*columns-missing
        for frame in range(total):
            y, x = divmod(frame, columns)
            rect = pg.Rect((x*size[0], y*size[1]), size)
            subsurfaces.append(sheet.subsurface(rect))
        return itertools.cycle(subsurfaces)

    def get_next(self, dt=0):
        self.accumulator += dt
        if not self.frame:
            self.frame = self.frames.next()
        while self.accumulator >= self.delay:
            self.frame = self.frames.next()
            self.accumulator -= self.delay
        return self.frame

    
class Asteroid(pg.sprite.Sprite):
    def __init__(self, pos, *groups):
        super(Asteroid, self).__init__(*groups)
        self.frames = Loop(prepare.GFX['asteroid_simple'], (96, 80), 60, 7, 21, missing=4)
        self.image = self.frames.frame
        self.rect = self.image.get_rect(center=pos)
        self.hit_rect = self.rect.inflate(-15, -15)

    def update(self, dt):
        self.image = self.frames.get_next(dt)

    def draw(self, surface):
        surface.blit(self.image, self.rect)