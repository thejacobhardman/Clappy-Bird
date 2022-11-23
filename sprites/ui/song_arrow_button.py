import scripts
import sprites.ui.button
import globals as g
import scene


# Button that navigates pages when there are many songs.
class SongArrowButton(sprites.ui.button.Button):

    def __init__(self, position, facing_right):
        self.facing_right = facing_right
        img = "Assets/Art/UI/Arrow-Button-Right.png" if self.facing_right else "Assets/Art/UI/Arrow-Button-Left.png"
        super().__init__(img, position)

    def on_click(self):
        scene.scenes["songs"].tab_over(self.facing_right)
