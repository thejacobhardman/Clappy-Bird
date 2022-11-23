import pygame as pg
import globals as g

class TextBox(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.text = ""
        self.font = pg.font.SysFont("Arial", 30, bold=True)
        self.text_renderer = self.font.render(self.text, True, pg.Color(0, 0, 0))
        g.screen.blit(self.text_renderer, [self.text_renderer.get_width() / 2,
                                             self.text_renderer.get_height() / 2])

    def addText(self, event):
        self.text += event.unicode
    
    def removeText(self):
        self.text = self.text[:-1]

    def getText(self):
        return self.text

    def update(self):
        for event in g.events:
            if event.type == pg.KEYDOWN:
                #print(event.key)
                if event.key == pg.K_RETURN:
                    print(self.getText())
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.removeText()
                else:
                    self.addText(event)
        self.text_renderer = self.font.render(self.text, True, pg.Color(0, 0, 0))
        g.screen.blit(self.text_renderer, [self.text_renderer.get_width() / 2,
                                             self.text_renderer.get_height() / 2])