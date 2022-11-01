from tkinter.tix import MAX
import pygame, random, math, sys
from itertools import repeat
from pygame import K_SPACE, mixer
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
        if self.position.x < -(WIDTH/2 + 1020):
            self.position = vec(WIDTH/2+1600, HEIGHT/2)

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

    def reset(self):
        self.position = vec(WIDTH/2-250, HEIGHT/2)
        self.image = pygame.transform.rotate(self.original_image, 0)
        self.rect = self.image.get_rect(center=self.position)
        self.vel = vec(0, 0)
        self.acceleration = vec(0, 0)

    def update(self):
        self.acceleration += vec(0, 0.4)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.acceleration += vec(0, -4)

        if self.acceleration.length() > MAX_SPEED:
            self.acceleration.scale_to_length(MAX_SPEED)
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)

        self.vel += self.acceleration
        self.position += self.vel
        self.rect.center = self.position

    def did_leave_screen(self):
        if self.position.y > HEIGHT:
            return True
        if self.position.y < 0:
            return True

class Pipe(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Assets/Art/pipe.png")

all_sprites = pygame.sprite.Group()
pipes = pygame.sprite.Group()
backgrounds = pygame.sprite.Group()
player = Player()

def main_menu(all_sprites, pipes, backgrounds, player, offset):
    mixer.music.load("Assets/SFX/happy.mp3")
    mixer.music.set_volume(0.5)
    mixer.music.play(-1)
    click = False

    scripts.reset_game(all_sprites, pipes, backgrounds, player)

    background_1 = Background(vec(WIDTH/2, HEIGHT/2))
    background_2 = Background(vec(WIDTH/2+1920, HEIGHT/2))
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
                game_loop(all_sprites, pipes, backgrounds, player, offset)
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

def game_loop(all_sprites, pipes, backgrounds, player, offset):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        all_sprites.update()
        backgrounds.update()

        org_screen.fill((255, 255, 255))
        screen.fill((0, 0, 0))

        backgrounds.draw(screen)

        fps_clock.tick(FPS)
        all_sprites.draw(screen)

        if player.did_leave_screen():
            offset = scripts.shake()
            game_over(all_sprites, pipes, backgrounds, player, offset)

        org_screen.blit(screen, next(offset))
        pygame.display.update()

def game_over(all_sprites, pipes, backgrounds, player, offset):
    mixer.music.load("Assets/SFX/happy.mp3")
    mixer.music.set_volume(0.5)
    mixer.music.play(-1)
    click = False

    scripts.reset_game(all_sprites, pipes, backgrounds, player)

    background = Background()
    backgrounds.add(background)

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
                main_menu(all_sprites, pipes, backgrounds, player, offset)
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

main_menu(all_sprites, pipes, backgrounds, player, offset)