import pygame
import globals as g
import scene
import random
import sprites.ui.text
import sprites.ui.scene_button

# Draws text to the screen


def draw_text(text, font, color, surface, x, y):
    text = font.render(text, 1, color)
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    surface.blit(text, text_rect)


# Shakes the screen upon player death
def shake():
    s = -1
    for _ in range(0, 3):
        for x in range(0, 20, 5):
            yield x * s, 0
        for x in range(20, 0, 5):
            yield x * s, 0
        s *= -1
    while True:
        yield 0, 0


def check_collisions(sprite, group):
    is_collision = pygame.sprite.spritecollide(sprite, group, False)
    if is_collision:
        return True
    return False


def animate_sprite(frames, index):
    if index == len(frames):
        return frames[0]
    else:
        return frames[index+1]


def draw_image(image, surface, x, y):
    image = pygame.image.load(image)
    image_rect = image.get_rect()
    image_rect.center = (x, y)
    surface.blit(image, image_rect)

# This will generate a random funny hint on the loading screen.


def generate_loading_hint():
    strings = [
        "Don't die.",
        "Be better at the game.",
        "Do better.",
        "Avoid the pipes.",
        "The cake is a lie.",
        "42",
        "Use the force.",
        "Live long and prosper.",
        "Do, or do not. There is no try.",
        "Use the hidden ability!",
        "help me they're in my house",
        "you guys have hands, don't you?",
        "bird up",
        "snappy bird was already taken",
        "Skill issue",
        "Good luck on your exams!",
        ":D",
        "Visit the Clappy Bird Wiki for tips",
        "holy cow",
        "I eat, Jon. it's what I do",
        "I ate those food",
    ]

    hint = "Hint: " + strings[random.randint(0, len(strings)-1)]

    return hint

# Toggles absolute unit mode on and off
def toggle_absolute_unit_mode():
    g.absolute_unit_mode = not g.absolute_unit_mode

# Run this whenever you need to change the scene, as it initializes the new scene


def change_scene(new_scene):
    scene.scenes[new_scene].init()
    g.current_scene = new_scene

# This executes a scripts that is called by a toggle button
def execute_script(function=None):
    method_name = function
    possibles = globals().copy()
    possibles.update(locals())
    method = possibles.get(method_name)
    if not method:
        raise NotImplementedError("Method %s not implemented" % method_name)
    method()

# Dynamically generates a list of audio devices
def generate_input_devices():
    elements = []
    elements.append(
        [
            sprites.ui.text.Text(
                "Your Input Devices",
                (g.WIDTH/2, g.HEIGHT/2-300),
                60,
                pygame.Color(0, 0, 0)
            ),
            sprites.ui.text.Text(
                "Change your default input device in your system settings to change the in-game microphone.",
                (g.WIDTH/2, g.HEIGHT/2-250),
                30,
                pygame.Color(0, 0, 0)
            ),
            sprites.ui.text.Text(
                "Restart the game after changing your system settings.",
                (g.WIDTH/2, g.HEIGHT/2-200),
                30,
                pygame.Color(0, 0, 0)
            )
        ]
    )
    for i in range(0, len(g.audio_devices_display)):
        elements.append(
            sprites.ui.text.Text(
                str(g.audio_devices_display[i]),
                (g.WIDTH/2, g.HEIGHT/2-(30*i)),
                20,
                pygame.Color(0, 0, 0)
            )
        )

    elements.append(
        sprites.ui.text.Text(
            ("Currently Selected Input Device: " + g.selected_audio_device_display),
            (g.WIDTH/2, g.HEIGHT/2+200),
            30,
            pygame.Color(0, 0, 0)
        )
    )

    elements.append(
        sprites.ui.scene_button.SceneButton(
            "Assets/Art/UI/Options-Button.png",
            (g.WIDTH/2, g.HEIGHT/2+275),
            load_scene="options"
        )
    )

    return elements

def update_clap_detected_text():
    with open('interactions\interactions.txt', 'r') as reader:
        if reader.readline() == "CLAP":
            g.clap_detected_text = "CLAP DETECTED"

# # This is supposed to dynamically return a variable from the globals based on input
# def get_updated_global_variable(variable):
#     return g.variable
