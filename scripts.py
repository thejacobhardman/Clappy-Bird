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

def reset_game(all_sprites, pipes, backgrounds, player):
    all_sprites.empty()
    pipes.empty()
    backgrounds.empty()
    player.reset()
    all_sprites.add(player)
