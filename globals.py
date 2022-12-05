import pygame as pg
import itertools

pg.init()
pg.key.set_repeat(500, 100)

# Constants
WIDTH = 1280
HEIGHT = 720
FPS = 60
PIPE_SPEED = 10


fps_clock = pg.time.Clock()

title_font = pg.font.SysFont(None, 64)
game_font = pg.font.SysFont(None, 48)

org_screen = pg.display.set_mode((WIDTH, HEIGHT))
screen = org_screen.copy()

icon = pg.image.load('Assets/Art/Bird Sprite/frame-1.png')

jump_sound = pg.mixer.Sound("Assets/SFX/slime_jump.wav")
jump_sound.set_volume(0.75)

death_sound = pg.mixer.Sound("Assets/SFX/death.wav")
death_sound.set_volume(0.75)

countdown_sound = pg.mixer.Sound("Assets/SFX/Countdown.wav")
countdown_sound.set_volume(0.25)

birds_sound = pg.mixer.Sound("Assets/SFX/birds-isaiah658.wav")
birds_sound.set_volume(0.25)

gem_sound = pg.mixer.Sound("Assets/SFX/collect.wav")
gem_sound.set_volume(0.25)

applause_sound = pg.mixer.Sound("Assets/SFX/applause.mp3")
applause_sound.set_volume(0.25)

vec = pg.math.Vector2

Song_win = pg.USEREVENT + 1

# Used to shake the screen upon player death.
offset = itertools.repeat((0, 0))  # <- Set with "scripts.shake()"

backgrounds = pg.sprite.Group()

current_scene = "login"  # Do not manually change this, use scrips.set_scene() instead

# This is set to pg.event.get() every tick
events = []

# HTTP Stuffs :DDDDDD
api_url = "https://clap-api.herokuapp.com"
logged_in = False
username = ""
token = ""
userId = ""

# Big dictionary of song mappings
songs = {
    "Levels\\Blue Skies - Silent Partner.mp3": 1,
    "Levels\\Buddha.mp3": 2,
    "Levels\\C Major Scale.mp3": 3,
    "Levels\\Jam Jam Jam.mp3": 4,
    "Levels\\Octagon of Destiny.mp3": 5,
    "Levels\\Parking.mp3": 6,
    "Levels\\Remix 10.mp3": 7,
    "Levels\\Spartacus.mp3": 8,
    "Levels\\Stuffing Your Face.mp3": 9,
    "Levels\\Uk.mp3": 10,
    # etc
}
