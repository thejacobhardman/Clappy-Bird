import pygame as pg
import itertools
import pyaudio

pg.init()
pg.key.set_repeat(500, 100)

# Constants
WIDTH = 1280
HEIGHT = 720
FPS = 60
PIPE_SPEED = 10

# Audio Devices - This code came from: https://stackoverflow.com/a/39677871
def get_audio_devices():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    input_devices = []
    input_devices_display_list = []

    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            input_devices.append(p.get_device_info_by_host_api_device_index(0, i))
            input_devices_display_list.append(p.get_device_info_by_host_api_device_index(0, i).get('name'))

    return input_devices, input_devices_display_list

def get_default_audio_device():
    p = pyaudio.PyAudio()
    return p.get_default_input_device_info(), p.get_default_input_device_info().get('name')

audio_devices, audio_devices_display = get_audio_devices()
selected_audio_device, selected_audio_device_display = get_default_audio_device()

absolute_unit_mode = False

fps_clock = pg.time.Clock()

title_font = pg.font.SysFont(None, 64)
game_font = pg.font.SysFont(None, 48)

org_screen = pg.display.set_mode((WIDTH, HEIGHT))
screen = org_screen.copy()

icon = pg.image.load('Assets/Art/Bird Sprite/frame-1.png')

sounds = []

jump_sound = pg.mixer.Sound("Assets/SFX/slime_jump.wav")
jump_sound.set_volume(0.75)
sounds.append(jump_sound)

death_sound = pg.mixer.Sound("Assets/SFX/death.wav")
death_sound.set_volume(0.75)
sounds.append(death_sound)

countdown_sound = pg.mixer.Sound("Assets/SFX/Countdown.wav")
countdown_sound.set_volume(0.25)
sounds.append(countdown_sound)

birds_sound = pg.mixer.Sound("Assets/SFX/birds-isaiah658.wav")
birds_sound.set_volume(0.25)
sounds.append(birds_sound)

gem_sound = pg.mixer.Sound("Assets/SFX/collect.wav")
gem_sound.set_volume(0.25)
sounds.append(gem_sound)

applause_sound = pg.mixer.Sound("Assets/SFX/applause.mp3")
applause_sound.set_volume(0.25)
sounds.append(applause_sound)

vec = pg.math.Vector2

Song_win = pg.USEREVENT + 1

# Used to shake the screen upon player death.
offset = itertools.repeat((0, 0))  # <- Set with "scripts.shake()"

backgrounds = pg.sprite.Group()

# Do not manually change this, use scrips.set_scene() instead
current_scene = "login"

# This is set to pg.event.get() every tick
events = []

# HTTP Stuffs :DDDDDD
api_url = "https://clap-api.herokuapp.com"
logged_in = False
username = ""
token = ""
userId = ""

# Big list it's a list now hehehe of song mappings
songs = [
    "Levels/Blue Skies - Silent Partner.wav",
    "Levels/Buddha.wav",
    "Levels/C Major Scale.wav",
    "Levels/Jam Jam Jam.wav",
    "Levels/Octagon of Destiny.wav",
    "Levels/Parking.wav",
    "Levels/Remix 10.wav",
    "Levels/Spartacus.wav",
    "Levels/Stuffing Your Face.wav",
    "Levels/Uk.wav",
    # etc
]

font_size = 55
