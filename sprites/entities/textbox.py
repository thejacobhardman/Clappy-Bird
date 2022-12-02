import pygame as pg
import globals as g

class TextBox(pg.sprite.Sprite):

    def __init__(self, x_axis, y_axis):
        pg.sprite.Sprite.__init__(self)
        self.text = ""
        self.input_rect = pg.Rect(x_axis, y_axis, 300, 50)
        self.font = pg.font.SysFont("Arial", 30, bold=True)

        self.color_active = pg.Color('yellow')
        self.color_passive = pg.Color('lightskyblue3')
        self.color = self.color_passive
        self.active = False

        self.drawTextBox()
          

    def drawTextBox(self):
        self.text_renderer = self.font.render(self.text, True, pg.Color(0, 0, 0))
        pg.draw.rect(g.screen, self.color, self.input_rect)
        g.screen.blit(self.text_renderer, (self.input_rect.x+5, self.input_rect.y+5))
        self.input_rect.w = max(100, self.text_renderer.get_width()+10)

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
            
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.input_rect.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False

                    
        self.drawTextBox()
        pg.display.flip()