"""
This module initializes useful constants, initializes the display,
and loads necessary resources.
"""

import os
import pygame as pg
import tools


CAPTION = "Space"
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE = (700, 525)
BACKGROUND_COLOR = (10, 20, 30)
SCALE_FACTOR = 0.3 # For scaleing down ship images.


DIRECT_DICT = {pg.K_UP   : ( 1, -1),
               pg.K_DOWN : ( -1, 1),
               pg.K_q: ( 1, 1),
               pg.K_e : (-1, -1)}


# Set up environment.
os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.init()
pg.display.set_caption(CAPTION)
pg.display.set_mode(SCREEN_SIZE)

# Load all graphics.
GFX = tools.load_all_gfx("resources")
GFX["ships"] = tools.load_all_gfx(os.path.join("resources", "ships"))
