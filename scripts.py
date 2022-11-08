import pygame

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
            yield (x*s, 0)
        for x in range(20, 0, 5):
            yield (x*s, 0)
        s *= -1
    while True:
        yield (0, 0)

def check_collisions(sprite, group):
    is_collision = False
    is_collision = pygame.sprite.spritecollide(sprite, group, False)
    if is_collision:
        return True
    return False

def load_player_sprite():
    player_sprite = [
        pygame.image.load("Assets/Art/Bird Sprite/frame-1.png"),
        pygame.image.load("Assets/Art/Bird Sprite/frame-2.png"),
        pygame.image.load("Assets/Art/Bird Sprite/frame-3.png"),
        pygame.image.load("Assets/Art/Bird Sprite/frame-4.png"),
        pygame.image.load("Assets/Art/Bird Sprite/frame-5.png"),
        pygame.image.load("Assets/Art/Bird Sprite/frame-6.png"),
        pygame.image.load("Assets/Art/Bird Sprite/frame-7.png"),
        pygame.image.load("Assets/Art/Bird Sprite/frame-8.png")
    ]

    for i in range(8):
        player_sprite[i] = pygame.transform.scale(player_sprite[i], (100, 68))

    return player_sprite

def animate_sprite(frames, index):
    if index == len(frames):
        return frames[0]
    else:
        return frames[index+1]

def reset_game(all_sprites, pipes, backgrounds, buttons, player):
    all_sprites.empty()
    pipes.empty()
    backgrounds.empty()
    buttons.empty()
    player.reset()
    all_sprites.add(player)
