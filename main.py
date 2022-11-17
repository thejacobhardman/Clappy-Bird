# Version 0.2.0

# Gem image credit - https://pngtree.com/freepng/purple-luminous-gemstone-diamond_6070400.html

# Gem sound credit - https://freesound.org/people/bradwesson/sounds/135936/
# Author - Brad Wesson

import pygame as pg
import globals as g
from sprites.background import Background
from scene import scenes
import sys

pg.display.set_caption("Clappy Bird")
pg.display.set_icon(g.icon)

g.backgrounds.add(Background(g.vec(g.WIDTH / 2, g.HEIGHT / 2)),
                  Background(g.vec(g.WIDTH / 2 + 2560, g.HEIGHT / 2)))

scenes[g.current_scene].init()

# Game loop
while True:
    g.events = pg.event.get()

    g.backgrounds.draw(g.screen)

    scenes[g.current_scene].update()

    g.fps_clock.tick(g.FPS)
    g.org_screen.blit(g.screen, next(g.offset))
    pg.display.update()

    for event in g.events:
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
