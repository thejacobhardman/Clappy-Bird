# Version 0.4.0

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

    # Collect pygame events
    g.events = pg.event.get()

    # Draw backgrounds
    g.backgrounds.draw(g.screen)

    # Call update() on the currently active scene
    scenes[g.current_scene].update()

    g.fps_clock.tick(g.FPS)
    g.org_screen.blit(g.screen, next(g.offset))
    pg.display.update()

    for event in g.events:
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
