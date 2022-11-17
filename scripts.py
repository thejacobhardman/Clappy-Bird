import pygame
import globals as g
import scene


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


# Run this whenever you need to change the scene, as it initializes the new scene
def change_scene(new_scene):
    scene.scenes[new_scene].init()
    g.current_scene = new_scene
