import globals as g
from scenes.menu import Menu
import pygame as pg
import sprites.ui.text
import sprites.ui.scene_button
from interactions import clapDetect

class MicCheck(Menu):

    def __init__(self):
        super().__init__([])
        self.clap_detected_text = sprites.ui.text.Text(
                                    "CLAP DETECTED",
                                    (g.WIDTH/2, g.HEIGHT/2),
                                    60,
                                    pg.Color(0, 0, 0))
        self.first_load = True
        self.clap_detected = False
        self.sprites.add(
            sprites.ui.text.Text(
            "Check Microphone Input",
            (g.WIDTH/2, g.HEIGHT/2-250),
            60,
            pg.Color(0, 0, 0)
        ))
        self.sprites.add(
            sprites.ui.text.Text(
            "Try Clapping!",
            (g.WIDTH/2, g.HEIGHT/2-200),
            40,
            pg.Color(0, 0, 0)
        ))
        self.sprites.add(
            sprites.ui.scene_button.SceneButton(
            "Assets/Art/UI/Options-Button.png",
            (g.WIDTH/2, g.HEIGHT/2+200),
            load_scene="options",
            size=g.font_size
        ))

    def __handle_click(self):
        mouseX, mouseY = pg.mouse.get_pos()
        for event in g.events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # self.sprites.sprites() just gets a list of sprites from the self.sprites sprite group
                    for sprite in self.sprites.sprites():
                        # Check if any buttons were clicked
                        if isinstance(sprite, sprites.ui.button.Button) and sprite.click((mouseX, mouseY)):
                            self.first_load = False
                            sprite.on_click()
    
    def update_clap_detected_text(self):
        if clapDetect.update_clap_detected_text() == True and len(self.sprites.sprites()) == 3:
            self.sprites.add(self.clap_detected_text)
            self.clap_detected = True

    def redraw_screen(self):
        with open('interactions\interactions.txt', 'w') as writer:
            writer.write("") 
        self.clap_detected_text.kill()
        self.first_load = True
        super().__init__([])
        self.sprites.add(
            sprites.ui.text.Text(
            "Check Microphone Input",
            (g.WIDTH/2, g.HEIGHT/2-250),
            60,
            pg.Color(0, 0, 0)
        ))
        self.sprites.add(
            sprites.ui.text.Text(
            "Try Clapping!",
            (g.WIDTH/2, g.HEIGHT/2-200),
            40,
            pg.Color(0, 0, 0)
        ))
        self.sprites.add(
            sprites.ui.scene_button.SceneButton(
            "Assets/Art/UI/Options-Button.png",
            (g.WIDTH/2, g.HEIGHT/2+200),
            load_scene="options",
            size=g.font_size
        ))
    
    def update(self):
        if not self.first_load:
            self.redraw_screen()
        self.update_clap_detected_text()
        self.sprites.draw(g.screen)
        self.__handle_click()
