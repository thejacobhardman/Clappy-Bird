import pygame, random, math, sys
from itertools import repeat
from pygame import mixer
import scripts

pygame.init()

vec = pygame.math.Vector2

WIDTH = 1280
HEIGHT = 720
MAX_SPEED = 6
FPS = 60
fps_clock = pygame.time.Clock()
title_font = pygame.font.SysFont(None, 64)
game_font = pygame.font.SysFont(None, 48)

org_screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen = org_screen.copy()
pygame.display.set_caption("Clappy Bird")
icon = pygame.image.load('Assets/Art/duo_lingo.png')
pygame.display.set_icon(icon)

jump_sound = mixer.Sound("Assets/SFX/slime_jump.wav")
death_sound = mixer.Sound("Assets/SFX/death.ogg")

# Used to shake the screen upon player death.
offset = repeat((0, 0)) # <- Set with "scripts.shake()"

class Background(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Assets/Art/background.png").convert()
        self.position = position
        self.vel = vec(-4, 0)
        self.rect = self.image.get_rect(center=self.position)
        self.id = "background"

    def update(self):
        self.position += self.vel
        self.rect.center = self.position
        self.wrap_around_screen()

    def wrap_around_screen(self):
        if self.position.x < -(WIDTH/2 + 1920):
            self.position = vec(WIDTH/2+1900, HEIGHT/2)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Assets/Art/duo_lingo.png")
        self.original_image = self.image
        self.position = vec(WIDTH/2-250, HEIGHT/2)
        self.rect = self.image.get_rect(center=self.position)
        self.vel = vec(0, 0)
        self.acceleration = vec(0, 0)
        self.id = "player"
        self.dev_mode = False # <- Set this to True to disable the hopping movement for testing because I'm bad at Flappy Bird lol.

    def reset(self):
        self.position = vec(WIDTH/2-250, HEIGHT/2)
        self.image = pygame.transform.rotate(self.original_image, 0)
        self.rect = self.image.get_rect(center=self.position)
        self.vel = vec(0, 0)
        self.acceleration = vec(0, 0)

    def update(self):
        if self.dev_mode == False: # Normal bouncy movement.
            self.acceleration += vec(0, 0.4)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.acceleration += vec(0, -4)

            if self.acceleration.length() > MAX_SPEED:
                self.acceleration.scale_to_length(MAX_SPEED)
            if self.vel.length() > MAX_SPEED:
                self.vel.scale_to_length(MAX_SPEED)
            self.vel += self.acceleration
        else: # Complete control for testing.
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.vel += vec(0, -0.4)
            if keys[pygame.K_s]:
                self.vel += vec(0, 0.4)
            if keys[pygame.K_a]:
                self.vel += vec(-0.4, 0)
            if keys[pygame.K_d]:
                self.vel += (0.4, 0)

        self.position += self.vel
        self.rect.center = self.position

    def did_leave_screen(self):
        if self.position.y > HEIGHT:
            return True
        if self.position.y < 0:
            return True

class Pipe(pygame.sprite.Sprite):
    def __init__(self, y_side, x_offset):
        pygame.sprite.Sprite.__init__(self)
        self.y_side = y_side
        self.image = pygame.image.load("Assets/Art/pipe.png")
        self.original_image = self.image
        if self.y_side == "top":
            self.position=vec((WIDTH+x_offset), self.generate_height())
            self.image = pygame.transform.rotate(self.original_image, 180)
        elif self.y_side == "bottom": 
            self.position = vec(WIDTH+x_offset, self.generate_height())
        self.rect = self.image.get_rect(center= self.position)
        self.vel = vec(-4, 0)
        self.id = "pipe"    

    def generate_height(self):
        if self.y_side == "top":
            return random.randint(0, 93) # Original value = (0, 133)
        elif self.y_side == "bottom":
            return random.randint(666, 720) # Original value = (626, 720)

    def update(self):
        self.position += self.vel
        self.rect.center = self.position
        self.did_leave_screen()

    def did_leave_screen(self):
        if self.position.x < -152:
            pipes.remove(self)
            all_sprites.remove(self)

all_sprites = pygame.sprite.Group()
pipes = pygame.sprite.Group()
backgrounds = pygame.sprite.Group()
player = Player()
pipe_count = 0

def main_menu(all_sprites, pipes, backgrounds, player, pipe_count, offset):
    mixer.music.load("Assets/SFX/happy.mp3")
    mixer.music.set_volume(0.5)
    # mixer.music.play(-1) # Uncomment this to play menu music.
    click = False

    scripts.reset_game(all_sprites, pipes, backgrounds, player)

    background_1 = Background(vec(WIDTH/2, HEIGHT/2))
    background_2 = Background(vec(WIDTH/2+2560, HEIGHT/2))
    backgrounds.add(background_1)
    backgrounds.add(background_2)

    while True:
        screen.fill((0, 0, 0))
        backgrounds.draw(screen)

        scripts.draw_text("CLAPPY BIRD", title_font, (0, 0, 0), screen, WIDTH/2, HEIGHT/2-100)
        mouseX, mouseY = pygame.mouse.get_pos()
        play_button = pygame.Rect(WIDTH/2, HEIGHT/2, 200, 50)
        play_button.center=(WIDTH/2, HEIGHT/2)
        quit_button = pygame.Rect(WIDTH/2, HEIGHT/2+75, 200, 50)
        quit_button.center=(WIDTH/2, HEIGHT/2+75)
        if play_button.collidepoint((mouseX, mouseY)):
            if click:
                game_loop(all_sprites, pipes, backgrounds, player, pipe_count, offset)
        if quit_button.collidepoint((mouseX, mouseY)):
            if click:
                pygame.quit()
                sys.exit()
        pygame.draw.rect(screen, (0, 0, 0), play_button)
        scripts.draw_text("PLAY", game_font, (255, 255, 255), screen, WIDTH/2, HEIGHT/2)
        pygame.draw.rect(screen, (0, 0, 0), quit_button)
        scripts.draw_text("QUIT", game_font, (255, 255, 255), screen, WIDTH/2, HEIGHT/2+75)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        fps_clock.tick(FPS)
        org_screen.blit(screen, next(offset))
        pygame.display.update()

def game_loop(all_sprites, pipes, backgrounds, player, pipe_count, offset):
    x_offset = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jump_sound.play()

        while pipe_count < 12:
            top_pipe = Pipe("top", x_offset)
            bottom_pipe = Pipe("bottom", x_offset)
            pipes.add(top_pipe)
            pipes.add(bottom_pipe)
            all_sprites.add(top_pipe)
            all_sprites.add(bottom_pipe)
            pipe_count += 2
            # This entire code is so stupid and needs a proper fix.
            if x_offset < 2250:
                fix = random.randint(0, 1)
                if fix == 0:
                    x_offset += 250
                elif fix == 1:
                    x_offset += 450
            else:
                x_offset = 0

        current_pipes = pipes.__len__()
        backgrounds.update()
        all_sprites.update()
        if pipes.__len__() < current_pipes:
            pipe_count -= 2

        org_screen.fill((255, 255, 255))
        screen.fill((0, 0, 0))

        backgrounds.draw(screen)
        all_sprites.draw(screen)

        if player.did_leave_screen():
            death_sound.play()
            offset = scripts.shake()
            game_over(all_sprites, pipes, backgrounds, player, pipe_count, offset)

        did_player_collide = scripts.check_collisions(player, pipes)
        if did_player_collide == True:
            death_sound.play()
            offset = scripts.shake()
            game_over(all_sprites, pipes, backgrounds, player, pipe_count, offset)

        org_screen.blit(screen, next(offset))
        pygame.display.update()
        fps_clock.tick(FPS)

def game_over(all_sprites, pipes, backgrounds, player, pipe_count, offset):
    mixer.music.load("Assets/SFX/happy.mp3")
    mixer.music.set_volume(0.5)
    # mixer.music.play(-1) # Uncomment this to play menu music.
    click = False
    pipe_count = 0

    scripts.reset_game(all_sprites, pipes, backgrounds, player)

    background_1 = Background(vec(WIDTH/2, HEIGHT/2))
    backgrounds.add(background_1)

    while True:
        screen.fill((0, 0, 0))
        backgrounds.draw(screen)

        scripts.draw_text("GAME OVER", title_font, (0, 0, 0), screen, WIDTH/2, HEIGHT/2-100)
        mouseX, mouseY = pygame.mouse.get_pos()
        play_button = pygame.Rect(WIDTH/2, HEIGHT/2, 200, 50)
        play_button.center=(WIDTH/2, HEIGHT/2)
        quit_button = pygame.Rect(WIDTH/2, HEIGHT/2+75, 200, 50)
        quit_button.center=(WIDTH/2, HEIGHT/2+75)
        if play_button.collidepoint((mouseX, mouseY)):
            if click:
                main_menu(all_sprites, pipes, backgrounds, player, pipe_count, offset)
        if quit_button.collidepoint((mouseX, mouseY)):
            if click:
                pygame.quit()
                sys.exit()
        pygame.draw.rect(screen, (0, 0, 0), play_button)
        scripts.draw_text("MAIN MENU", game_font, (255, 255, 255), screen, WIDTH/2, HEIGHT/2)
        pygame.draw.rect(screen, (0, 0, 0), quit_button)
        scripts.draw_text("QUIT", game_font, (255, 255, 255), screen, WIDTH/2, HEIGHT/2+75)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        fps_clock.tick(FPS)
        org_screen.blit(screen, next(offset))
        pygame.display.update()

main_menu(all_sprites, pipes, backgrounds, player, pipe_count, offset)