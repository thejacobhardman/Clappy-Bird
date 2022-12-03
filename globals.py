import pygame as pg
import itertools

pg.init()

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
