import pygame, random, math, sys
from itertools import repeat
from pygame import mixer
import scripts

pygame.init()

vec = pygame.math.Vector2

WIDTH = 1280
HEIGHT = 720
MAX_SPEED = 9
FPS = 60
fps_clock = pygame.time.Clock()
title_font = pygame.font.SysFont(None, 64)
game_font = pygame.font.SysFont(None, 48)

org_screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen = org_screen.copy()
pygame.display.set_caption("Clappy Bird")

offset = repeat((0, 0)) # <- Set with "scripts.shake()"

def main_menu():
    print("This is the main menu loop.")
    click = False
    while True:
        screen.fill((0, 0, 0))

        scripts.draw_text("CLAPPY BIRD", title_font, (255, 255, 255), screen, WIDTH/2, HEIGHT/2-100)
        mouseX, mouseY = pygame.mouse.get_pos()
        play_button = pygame.Rect(WIDTH/2, HEIGHT/2, 200, 50)
        play_button.center=(WIDTH/2, HEIGHT/2)
        quit_button = pygame.Rect(WIDTH/2, HEIGHT/2+75, 200, 50)
        quit_button.center=(WIDTH/2, HEIGHT/2+75)
        if play_button.collidepoint((mouseX, mouseY)):
            if click:
                game_loop()
        if quit_button.collidepoint((mouseX, mouseY)):
            if click:
                pygame.quit()
                sys.exit()
        pygame.draw.rect(screen, (255, 255, 255), play_button)
        scripts.draw_text("PLAY", game_font, (0, 0, 0), screen, WIDTH/2, HEIGHT/2)
        pygame.draw.rect(screen, (255, 255, 255), quit_button)
        scripts.draw_text("QUIT", game_font, (0, 0, 0), screen, WIDTH/2, HEIGHT/2+75)

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

def game_loop():
    print("This is the main game loop.")

def game_over():
    print("This is the game over screen.")

main_menu()