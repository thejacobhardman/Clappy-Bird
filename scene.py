import globals as g
import sprites.ui.song_button
import sprites.ui.scene_button
import sprites.ui.quit_button
import scenes.menu
import sprites.ui.sprite
import sprites.ui.text
import pygame as pg
import scenes.songs
import scenes.load_song
import scenes.game
import scenes.countdown

game_scene = scenes.game.Game()

# Data-driven scenes (sorry if this reminds you of Flutter lol, but still better than writing a bunch of boilerplate)
scenes = {

    "main_menu": scenes.menu.Menu(
        [
            sprites.ui.sprite.Sprite(
                "Assets/Art/clappy-bird-logo.png",
                (g.WIDTH/2, g.HEIGHT/2-150)
            ),
            sprites.ui.scene_button.SceneButton(
                "Assets/Art/UI/Play-Button.png",
                (g.WIDTH/2-175, g.HEIGHT/2),
                load_scene="songs"
            ),
            sprites.ui.scene_button.SceneButton(
                "Assets/Art/UI/Leaderboard-Button.png",
                (g.WIDTH/2+175, g.HEIGHT/2),
                load_scene="leaderboard"
            ),
            sprites.ui.scene_button.SceneButton(
                "Assets/Art/UI/Options-Button.png",
                (g.WIDTH/2-175, g.HEIGHT/2+100)
            ),
            sprites.ui.quit_button.QuitButton(
                "Assets/Art/UI/Quit-Button.png",
                (g.WIDTH/2+175, g.HEIGHT/2+100)
            )
        ]
    ),

    "leaderboard": scenes.menu.Menu(
        [
            sprites.ui.text.Text(
                "Leaderboard",
                (g.WIDTH/2, g.HEIGHT/2-150),
                60,
                pg.Color(0, 0, 0)
            ),
            sprites.ui.scene_button.SceneButton(
                "Assets/Art/UI/Main-Menu-Button.png",
                (g.WIDTH/2-175, g.HEIGHT/2+100),
                load_scene="main_menu"
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
                "Assets/Art/UI/Main-Menu-Button.png",
                (g.WIDTH/2-175, g.HEIGHT/2),
                load_scene="main_menu"
            ),
            sprites.ui.scene_button.SceneButton(
                "Assets/Art/UI/Leaderboard-Button.png",
                (g.WIDTH/2+175, g.HEIGHT/2),
                load_scene="leaderboard"
            ),
            sprites.ui.scene_button.SceneButton(
                "Assets/Art/UI/Options-Button.png",
                (g.WIDTH/2-175, g.HEIGHT/2+100)
            ),
            sprites.ui.quit_button.QuitButton(
                "Assets/Art/UI/Quit-Button.png",
                (g.WIDTH/2+175, g.HEIGHT/2+100)
            )
        ]
    ),

    "songs": scenes.songs.Songs(
        [
            sprites.ui.text.Text(
                "Select Level",
                (g.WIDTH/2, g.HEIGHT/8),
                60,
                pg.Color(0, 0, 0)
            ),
            sprites.ui.scene_button.SceneButton(
                "Assets/Art/UI/Main-Menu-Button.png",
                (g.WIDTH / 2, (g.HEIGHT / 2) + 300),
                load_scene="main_menu"
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
