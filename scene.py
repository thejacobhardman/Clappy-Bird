import globals as g
import sprites.ui.song_button
import sprites.ui.scene_button
import sprites.ui.quit_button
import sprites.ui.difficulty_button
import sprites.ui.upload_button
import scenes.menu
import scenes.win_screen
import sprites.ui.sprite
import sprites.ui.text
import sprites.entities.textbox
import pygame as pg
import scenes.songs
import scenes.custom_songs
import scenes.load_song
import scenes.game
import scenes.countdown
import scenes.upload
import scenes.login_signup
import sprites.ui.logout_button
import scenes.leaderboard

game_scene = scenes.game.Game()

# Data-driven scenes (sorry if this reminds you of Flutter lol, but still better than writing a bunch of boilerplate)

# scenes is a dictionary that expects a key that is a string, and a value that is an object of some kind of scene class
# (by some kind of scene class, I mean a class that has an init() and an update() method).

# The global variable current_scene determines what scene is currently active; this is just a string that should match
# one of the keys in the dictionary below. When current_scene is set to a key in the below dictionary, its value (which
# is a scene object) has its update method called every game tick.

# For example, if current_scene is set to "main_menu", the Menu object in the scenes dictionary below has its update()
# method called every tick.

########################################################################################################################

# The Menu class is used for simple menus. You can think of Menu instances as being basic menus that allow the user
# to click buttons to navigate around.

# The Menu class takes only a list of objects of classes that inherit from pygame.sprite.Sprite. Because of this, I
# have made some classes that do just that, and that render a certain kind of sprite:

# sprites.ui.sprite.Sprite(image, position)
# This represents a basic image sprite with no functionality

# sprites.ui.text.Text(text, position, size, color)
# This represents a basic text sprite with no functionality

# sprites.ui.scene_button.Scene_Button(image, position, load_scene)
# This represents a button that you can click to navigate between scenes


# If you need a sprite with custom functionality, you can create your own class that inherits from pygame.sprite.Sprite


scenes = {

    "login": scenes.login_signup.LoginSignup(True),
    "signup": scenes.login_signup.LoginSignup(False),

    "main_menu": scenes.menu.Menu(
        [
            sprites.ui.sprite.Sprite(
                "Assets/Art/clappy-bird-logo.png",
                (g.WIDTH/2, g.HEIGHT/2-150)
            ),
            sprites.ui.scene_button.SceneButton(
                "Assets/Art/UI/Empty-Button.png",
                (g.WIDTH/2-175, g.HEIGHT/2),
                load_scene="play_menu",
                text="Play",
                size=g.font_size
            ),
            sprites.ui.scene_button.SceneButton(
                "Assets/Art/UI/Empty-Button-Blue.png",
                (g.WIDTH/2+175, g.HEIGHT/2),
                load_scene="leaderboard",
                text="Leaderboard",
                size=g.font_size
            ),
            sprites.ui.scene_button.SceneButton(
                "Assets/Art/UI/Empty-Button-Orange.png",
                (g.WIDTH/2+175, g.HEIGHT/2+100),
                load_scene="options",
                text="Options",
                size=g.font_size
            ),
            sprites.ui.scene_button.SceneButton(
                "Assets/Art/UI/Empty-Button-Magenta.png",
                (g.WIDTH/2-175, g.HEIGHT/2+100),
                text="Upload",
                load_scene="Upload_screen",
                size=g.font_size
            ),
            sprites.ui.logout_button.LogoutButton(
                "Assets/Art/UI/Empty-Button-Teal.png",
                (g.WIDTH/2-175, g.HEIGHT/2+200),
                text="Log Out",
                size=g.font_size
            ),
            sprites.ui.quit_button.QuitButton(
                "Assets/Art/UI/Empty-Button-Red.png",
                (g.WIDTH/2+175, g.HEIGHT/2+200),
                text="Quit",
                size=g.font_size
            )
        ]
    ),

    "play_menu": scenes.menu.Menu(
        [
            sprites.ui.text.Text(
                "Select Mode",
                (g.WIDTH/2, g.HEIGHT/12),
                60,
                pg.Color(0, 0, 0)
            ),
            sprites.ui.scene_button.SceneButton(
                "Assets/Art/UI/Empty-Button-Blue.png",
                (g.WIDTH/2-175, g.HEIGHT/2),
                text="Songs",
                load_scene="songs",
                size=g.font_size
            ),
            sprites.ui.scene_button.SceneButton(
                "Assets/Art/UI/Empty-Button-Orange.png",
                (g.WIDTH/2+175, g.HEIGHT/2),
                text="Custom Songs",
                load_scene="custom_songs",
                size=g.font_size
            ),
            sprites.ui.scene_button.SceneButton(
                "Assets/Art/UI/Empty-Button.png",
                (g.WIDTH/2, g.HEIGHT/2+100),
                text="Main Menu",
                load_scene="main_menu",
                size=g.font_size
            ),
        ]
    ),

    "leaderboard": scenes.leaderboard.Leaderboard(),

    "options": scenes.menu.Menu(
        [
            sprites.ui.text.Text(
                "Options",
                (g.WIDTH/2, g.HEIGHT/2-150),
                60,
                pg.Color(0, 0, 0)
            ),
            sprites.ui.scene_button.SceneButton(
                "Assets/Art/UI/Empty-Button.png",
                (g.WIDTH/2-175, g.HEIGHT/2+100),
                load_scene="main_menu",
                text="Main Menu",
                size=g.font_size
            ),
        ]
    ),

    "game_over": scenes.menu.Menu(
        [
            sprites.ui.text.Text(
                "GAME OVER",
                (g.WIDTH/2, g.HEIGHT/2-150),
                60,
                pg.Color(0, 0, 0)
            ),
            sprites.ui.scene_button.SceneButton(
                "Assets/Art/UI/Empty-Button.png",
                (g.WIDTH/2, g.HEIGHT/2+200),
                text="Replay",
                load_scene="difficulty"
            ),
            sprites.ui.scene_button.SceneButton(
                "Assets/Art/UI/Main-Menu-Button.png",
                (g.WIDTH/2-175, g.HEIGHT/2),
                load_scene="main_menu",
                text="Main Menu",
                size=g.font_size
            ),
            sprites.ui.scene_button.SceneButton(
                "Assets/Art/UI/Empty-Button-Blue.png",
                (g.WIDTH/2+175, g.HEIGHT/2),
                load_scene="leaderboard",
                text="Leaderboard",
                size=g.font_size
            ),
            sprites.ui.quit_button.QuitButton(
                "Assets/Art/UI/Empty-Button-Red.png",
                (g.WIDTH/2+175, g.HEIGHT/2+100),
                text="Quit",
                size=g.font_size
            )
        ]
    ),

    "Win_screen": scenes.win_screen.WinScreen(
        [
            sprites.ui.text.Text(
                "SONG COMPLETED!!!",
                (g.WIDTH/2, g.HEIGHT/2-150),
                60,
                pg.Color(0, 0, 0)
            ),
            sprites.ui.scene_button.SceneButton(
                "Assets/Art/UI/Empty-Button.png",
                (g.WIDTH / 2 - 175, g.HEIGHT / 2),
                load_scene="main_menu",
                text="Main Menu",
                size=g.font_size
            ),
            sprites.ui.scene_button.SceneButton(
                "Assets/Art/UI/Empty-Button-Blue.png",
                (g.WIDTH / 2 + 175, g.HEIGHT / 2),
                load_scene="leaderboard",
                text="Leaderboard",
                size=g.font_size
            ),
            sprites.ui.scene_button.SceneButton(
                "Assets/Art/UI/Empty-Button-Orange.png",
                (g.WIDTH / 2 - 175, g.HEIGHT / 2 + 100),
                load_scene="options",
                text="Options",
                size=g.font_size
            ),
            sprites.ui.quit_button.QuitButton(
                "Assets/Art/UI/Empty-Button-Red.png",
                (g.WIDTH / 2 + 175, g.HEIGHT / 2 + 100),
                text="Quit",
                size=g.font_size
            )
        ]
    ),

    "Upload_screen": scenes.upload.UploadScreen(
        [
            sprites.ui.text.Text(
                "Upload a Song",
                (g.WIDTH/2, g.HEIGHT/2-270),
                60,
                pg.Color(0, 0, 0)
            ),
            sprites.ui.text.Text(
                "Enter a Youtube url",
                (g.WIDTH/2, g.HEIGHT/2-220),
                30,
                pg.Color(0, 0, 0)
            ),
            sprites.ui.scene_button.SceneButton(
                "Assets/Art/UI/Empty-Button.png",
                (g.WIDTH/2-175, g.HEIGHT/2),
                load_scene="main_menu",
                text="Main Menu",
                size=g.font_size
            ),
        ],
    ),
    "difficulty": scenes.menu.Menu(
        [
            sprites.ui.text.Text(
                "Choose Difficulty",
                (g.WIDTH/2, g.HEIGHT/2-150),
                60,
                pg.Color(0, 0, 0)
            ),
            sprites.ui.difficulty_button.DifficultyButton(
                "Assets/Art/UI/Empty-Button.png",
                (g.WIDTH/2-175, g.HEIGHT/2),
                text="Easy",
                size=g.font_size
            ),
            sprites.ui.difficulty_button.DifficultyButton(
                "Assets/Art/UI/Empty-Button-Blue.png",
                (g.WIDTH/2+175, g.HEIGHT/2),
                text="Normal",
                size=g.font_size
            ),
            sprites.ui.difficulty_button.DifficultyButton(
                "Assets/Art/UI/Empty-Button-Orange.png",
                (g.WIDTH/2-175, g.HEIGHT/2+100),
                text="Hard",
                size=g.font_size
            ),
            sprites.ui.difficulty_button.DifficultyButton(
                "Assets/Art/UI/Empty-Button-Red.png",
                (g.WIDTH/2+175, g.HEIGHT/2+100),
                text="Extreme",
                size=g.font_size
            )
        ]
    ),

    "songs": scenes.songs.Songs(
        [
            sprites.ui.text.Text(
                "Select Level",
                (g.WIDTH/2, g.HEIGHT/12),
                60,
                pg.Color(0, 0, 0)
            ),
            sprites.ui.scene_button.SceneButton(
                "Assets/Art/UI/Empty-Button.png",
                (g.WIDTH / 2, (g.HEIGHT / 2) + 300),
                load_scene="main_menu",
                text="Main Menu",
                size=g.font_size
            )
        ]
    ),

    "custom_songs": scenes.custom_songs.CustomSongs(
        [
            sprites.ui.text.Text(
                "Select Level",
                (g.WIDTH/2, g.HEIGHT/12),
                60,
                pg.Color(0, 0, 0)
            ),
            sprites.ui.scene_button.SceneButton(
                "Assets/Art/UI/Empty-Button.png",
                (g.WIDTH / 2, (g.HEIGHT / 2) + 300),
                load_scene="main_menu",
                text="Main Menu",
                size=g.font_size
            )
        ]
    ),

    "load_song": scenes.load_song.LoadSong(
        [
            sprites.ui.text.Text(
                "LOADING",
                (g.WIDTH/2, g.HEIGHT/2),
                60,
                pg.Color(0, 0, 0)
            ),
        ]
    ),

    "countdown": scenes.countdown.Countdown(),

    "game": game_scene,

}
