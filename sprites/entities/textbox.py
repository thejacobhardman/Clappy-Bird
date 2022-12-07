import pygame as pg
import globals as g
import pyperclip

class TextBox(pg.sprite.Sprite):

    def __init__(self, pos, hidden_text=False):
        pg.sprite.Sprite.__init__(self)
        self.text = ""
        self.hidden_text = ""
        self.has_hidden_text = hidden_text
        self.font = pg.font.SysFont("Arial", 30, bold=True)
        self.image = self.font.render(self.text, True, pg.Color(0, 0, 0))
        self.position = pos
        self.rect = self.image.get_rect(center=self.position)

        self.color_active = pg.Color('yellow')
        self.color_passive = pg.Color('lightskyblue3')
        self.color = self.color_passive
        self.active = False

        self.drawTextBox()

    def drawTextBox(self):
        if self.has_hidden_text:
            self.image = self.font.render(self.hidden_text, True, pg.Color(0, 0, 0))
        else:
            self.image = self.font.render(self.text, True, pg.Color(0, 0, 0))
        pg.draw.rect(g.screen, self.color, self.rect)
        g.screen.blit(self.image, (self.rect.x + 5, self.rect.y + 5))
        self.rect.w = max(200, self.image.get_width() + 10)

        if self.active:
            self.color = self.color_active
        else:
            self.color = self.color_passive

    def addText(self, event):
        self.text += event.unicode

    def removeText(self):
        self.text = self.text[:-1]

    def getText(self):
        return self.text

    def update(self):

        self.hidden_text = ""
        for char in self.text:
            self.hidden_text += "*"

        for event in g.events:
            if self.active:
                if event.type == pg.KEYDOWN:
                    # print(event.key)
                    keys = pg.key.get_pressed()
                    #if keys[pg.K_RETURN]:
                    #    self.text = ''
                    if keys[pg.K_BACKSPACE]:
                        self.removeText()
                    elif keys[pg.K_LCTRL] and keys[pg.K_v]:
                        self.text = pyperclip.paste()
                    else:
                        self.addText(event)

            if event.type == pg.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False

        self.drawTextBox()
        pg.display.flip()
