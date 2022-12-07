import scripts
import sprites.ui.button
import globals as g
import scene


# Button that navigates pages by calling a tab_over method in the specified menu.
class ArrowButton(sprites.ui.button.Button):

    def __init__(self, position, menu="", facing_right=True):
        self.facing_right = facing_right
        self.menu = menu
        img = "Assets/Art/UI/Arrow-Button-Right.png" if self.facing_right else "Assets/Art/UI/Arrow-Button-Left.png"
        super().__init__(img, position)

    def on_click(self):
        scene.scenes[self.menu].tab_over(self.facing_right)
