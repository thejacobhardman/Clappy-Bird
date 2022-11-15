# Version 0.2.0

# Gem image credit - https://pngtree.com/freepng/purple-luminous-gemstone-diamond_6070400.html

# Gem sound credit - https://freesound.org/people/bradwesson/sounds/135936/
# Author - Brad Wesson

import pygame, random, math, sys
from itertools import repeat
from pygame import mixer
import scripts
from level import Level
from otherLevel import OtherLevel
from os import listdir
from os.path import isfile, join

pygame.init()

vec = pygame.math.Vector2

WIDTH = 1280
HEIGHT = 720
MAX_SPEED = 4
FPS = 60
PIPE_SPEED = 10
fps_clock = pygame.time.Clock()
title_font = pygame.font.SysFont(None, 64)
game_font = pygame.font.SysFont(None, 48)


org_screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen = org_screen.copy()
pygame.display.set_caption("Clappy Bird")
icon = pygame.image.load('Assets/Art/Bird Sprite/frame-1.png')
pygame.display.set_icon(icon)

jump_sound = mixer.Sound("Assets/SFX/slime_jump.wav")
jump_sound.set_volume(0.75)
death_sound = mixer.Sound("Assets/SFX/death.wav")
death_sound.set_volume(0.75)
countdown_sound = mixer.Sound("Assets/SFX/Countdown.wav")
countdown_sound.set_volume(0.25)
birds_sound = mixer.Sound("Assets/SFX/birds-isaiah658.wav")
birds_sound.set_volume(0.25)
gem_sound = mixer.Sound("Assets/SFX/collect.wav")
gem_sound.set_volume(0.25)

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

class Button(pygame.sprite.Sprite):
    def __init__(self, image_file, position, text=""):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.position = position
        self.rect = self.image.get_rect(center=self.position)
        self.id = "button"
        self.text = text
        self.font = pygame.font.SysFont("Arial", 30, bold=True)
        self.text_renderer = self.font.render(text, True, pygame.Color(255, 255, 255))
        self.image.blit(self.text_renderer, [self.image.get_width() / 2 - self.text_renderer.get_width() / 2,
                                        self.image.get_height() / 2 - self.text_renderer.get_height() / 2])

    def click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.frames = scripts.load_player_sprite()
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.original_image = self.image
        self.position = vec(WIDTH/2-250, HEIGHT/2)
        self.rect = self.image.get_rect(center=self.position)
        self.vel = vec(0, 0)
        self.acceleration = vec(0, 0)
        self.score = 0
        self.id = "player"
        self.dev_mode = False # <- Set this to True to disable the hopping movement for testing because I'm bad at Flappy Bird lol.

    def reset(self):
        self.position = vec(WIDTH/2-250, HEIGHT/2)
        self.image = pygame.transform.rotate(self.original_image, 0)
        self.rect = self.image.get_rect(center=self.position)
        self.vel = vec(0, 0)
        self.score = 0
        self.acceleration = vec(0, 0)

    def update(self):
        if self.dev_mode == False: # Normal bouncy movement.
            self.acceleration += vec(0, 0.4)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.acceleration += vec(0, -4)
                if self.frame_index == 7:
                    self.frame_index = 0
                self.image = scripts.animate_sprite(self.frames, self.frame_index)
                self.frame_index += 1

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
    def __init__(self, y_side, x_offset, height):
        pygame.sprite.Sprite.__init__(self)
        self.y_side = y_side
        self.image = pygame.image.load("Assets/Art/pipe.png")
        self.original_image = self.image
        if self.y_side == "top":
            self.position=vec((WIDTH+x_offset), height)
            self.image = pygame.transform.rotate(self.original_image, 180)
        elif self.y_side == "bottom": 
            self.position = vec(WIDTH+x_offset, height)
        self.rect = self.image.get_rect(center= self.position)
        self.vel = vec(-PIPE_SPEED, 0)
        self.passed_player = False
        self.id = "pipe"

    def update(self):
        self.position += self.vel
        self.rect.center = self.position
        self.did_leave_screen()

    def did_leave_screen(self):
        if self.position.x < -152:
            pipes.remove(self)
            all_sprites.remove(self)

class Gem(pygame.sprite.Sprite):
    def __init__(self, x_offset, height, top_pipe, bottom_pipe):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Assets/Art/purpleGem.png")
        self.image = pygame.transform.scale(self.image, (35,35))
        self.position=vec((WIDTH+x_offset), height)
        self.rect = self.image.get_rect(center= self.position)
        self.vert_speed = -6
        self.vel = vec(-PIPE_SPEED, self.vert_speed)
        self.id = "gem"
        self.top_pipe = top_pipe
        self.bottom_pipe = bottom_pipe

    def update(self):
        self.position += self.vel
        self.rect.center = self.position

    def change_direction(self):
        self.vert_speed = self.vert_speed * -1
        self.vel = vec(-PIPE_SPEED, self.vert_speed)

    def play_collect_sound(self):
        gem_sound.play()

    def did_leave_screen(self):
        if self.position.x < -152:
            return True

all_sprites = pygame.sprite.Group()
pipes = pygame.sprite.Group()
backgrounds = pygame.sprite.Group()
buttons = pygame.sprite.Group()
player = Player()
pipe_count = 0

def main_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset):
    scripts.reset_game(all_sprites, pipes, backgrounds, buttons, player)

    background_1 = Background(vec(WIDTH/2, HEIGHT/2))
    background_2 = Background(vec(WIDTH/2+2560, HEIGHT/2))
    backgrounds.add(background_1, background_2)

    play_button = Button("Assets/Art/UI/Play-Button.png", (WIDTH/2-175, HEIGHT/2))
    leaderboard_button = Button("Assets/Art/UI/Leaderboard-Button.png", (WIDTH/2+175, HEIGHT/2))
    options_button = Button("Assets/Art/UI/Options-Button.png", (WIDTH/2-175, HEIGHT/2+100))
    quit_button = Button("Assets/Art/UI/Quit-Button.png", (WIDTH/2+175, HEIGHT/2+100))
    buttons.add(play_button, leaderboard_button, options_button, quit_button)

    if not mixer.get_busy():
        birds_sound.play(-1)

    while True:
        screen.fill((0, 0, 0))
        backgrounds.draw(screen)
        buttons.draw(screen)

        scripts.draw_image("Assets/Art/clappy-bird-logo.png", screen, WIDTH/2, HEIGHT/2-150)

        mouseX, mouseY = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_button.click((mouseX, mouseY)):
                        song_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)
                    if leaderboard_button.click((mouseX, mouseY)):
                        leaderboard_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)
                    if options_button.click((mouseX, mouseY)):
                        options_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)
                    if quit_button.click((mouseX, mouseY)):
                        pygame.quit()
                        sys.exit()

        fps_clock.tick(FPS)
        org_screen.blit(screen, next(offset))
        pygame.display.update()

def leaderboard_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset):
    main_menu_button = Button("Assets/Art/UI/Main-Menu-Button.png", (WIDTH/2-175, HEIGHT/2))
    leaderboard_button = Button("Assets/Art/UI/Leaderboard-Button.png", (WIDTH/2+175, HEIGHT/2))
    options_button = Button("Assets/Art/UI/Options-Button.png", (WIDTH/2-175, HEIGHT/2+100))
    quit_button = Button("Assets/Art/UI/Quit-Button.png", (WIDTH/2+175, HEIGHT/2+100))
    buttons.add(main_menu_button, leaderboard_button, options_button, quit_button)

    while True:
        screen.fill((0, 0, 0))
        backgrounds.draw(screen)
        buttons.draw(screen)

        scripts.draw_text("LEADERBOARD", title_font, (0, 0, 0), screen, WIDTH/2, HEIGHT/2-100)
        
        mouseX, mouseY = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if main_menu_button.click((mouseX, mouseY)):
                        main_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)
                    if leaderboard_button.click((mouseX, mouseY)):
                        leaderboard_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)
                    if options_button.click((mouseX, mouseY)):
                        options_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)
                    if quit_button.click((mouseX, mouseY)):
                        pygame.quit()
                        sys.exit()

        fps_clock.tick(FPS)
        org_screen.blit(screen, next(offset))
        pygame.display.update()

def options_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset):
    main_menu_button = Button("Assets/Art/UI/Main-Menu-Button.png", (WIDTH/2-175, HEIGHT/2))
    leaderboard_button = Button("Assets/Art/UI/Leaderboard-Button.png", (WIDTH/2+175, HEIGHT/2))
    options_button = Button("Assets/Art/UI/Options-Button.png", (WIDTH/2-175, HEIGHT/2+100))
    quit_button = Button("Assets/Art/UI/Quit-Button.png", (WIDTH/2+175, HEIGHT/2+100))
    buttons.add(main_menu_button, leaderboard_button, options_button, quit_button)

    while True:
        screen.fill((0, 0, 0))
        backgrounds.draw(screen)
        buttons.draw(screen)

        scripts.draw_text("OPTIONS", title_font, (0, 0, 0), screen, WIDTH/2, HEIGHT/2-100)
        
        mouseX, mouseY = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if main_menu_button.click((mouseX, mouseY)):
                        main_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)
                    if leaderboard_button.click((mouseX, mouseY)):
                        leaderboard_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)
                    if options_button.click((mouseX, mouseY)):
                        options_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)
                    if quit_button.click((mouseX, mouseY)):
                        pygame.quit()
                        sys.exit()

        fps_clock.tick(FPS)
        org_screen.blit(screen, next(offset))
        pygame.display.update()

def song_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset):

    buttons.empty()
    level_paths = [f for f in listdir("Levels") if isfile(join("Levels", f))]

    level_buttons = []
    i = 0
    for level in level_paths:
        level_buttons.append(Button("Assets/Art/UI/Empty-Button.png", (WIDTH/2, (HEIGHT/4) + (100 * i)), level))
        i += 1

    quit_button = Button("Assets/Art/UI/Quit-Button.png", (WIDTH / 2, (HEIGHT / 2) + 300))

    for level in level_buttons:
        buttons.add(level)

    buttons.add(quit_button)

    while True:
        screen.fill((0, 0, 0))
        backgrounds.draw(screen)
        buttons.draw(screen)

        scripts.draw_text("Level Select", title_font, (0, 0, 0), screen, WIDTH / 2, HEIGHT / 2 - 300)

        mouseX, mouseY = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if quit_button.click((mouseX, mouseY)):
                        main_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)
                    for i in level_buttons:
                        if i.click((mouseX, mouseY)):
                            game_loop(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset, "Levels/" + i.text)

        fps_clock.tick(FPS)
        org_screen.blit(screen, next(offset))
        pygame.display.update()

def game_loop(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset, song=""):
    gems = pygame.sprite.Group()
    mixer.music.load(song)
    mixer.music.set_volume(0.5)
    level = OtherLevel(song)
    start_ticks=pygame.time.get_ticks()
    music_started = False
    pipeIncr = 0
    levelTick = 0
    first_run = True
    counter = 3
    birds_sound.stop()
    while True:
        # Plays a countdown at the start of the game.
        if first_run:
            pygame.time.set_timer(pygame.USEREVENT, 1000)
            countdown_sound.play()
        while first_run == True:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    counter -= 1

            org_screen.fill((255, 255, 255))
            screen.fill((0, 0, 0))
            backgrounds.draw(screen)

            if counter > 0:
                scripts.draw_text(str(counter), title_font, (0, 0, 0), screen, WIDTH/2, HEIGHT/2)
            else:
                scripts.draw_text("GO!!!", title_font, (0, 0, 0), screen, WIDTH/2, HEIGHT/2)

            org_screen.blit(screen, next(offset))
            pygame.display.update()
            if counter == -1:
                start_ticks=pygame.time.get_ticks()
                first_run = False

        random_height = (random.randint(-300,300))
        levelTick += 1
        musicTick=(pygame.time.get_ticks()-start_ticks)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jump_sound.play()

        pipe_list = getattr(level, 'pipe_list')

        if levelTick == 140 and not music_started:
            music_started = True
            mixer.music.play(-1)
        if pipeIncr < len(pipe_list) and musicTick >= pipe_list[pipeIncr]['spawn']:  
            top_pipe = Pipe("top", 500, pipe_list[pipeIncr]['height'] - 540)
            bottom_pipe = Pipe("bottom", 500, pipe_list[pipeIncr]['height'] + 540)
            gem = Gem(500, pipe_list[pipeIncr]['height'], top_pipe, bottom_pipe)
            pipes.add(top_pipe)
            pipes.add(bottom_pipe) 
            gems.add(gem)
            all_sprites.add(top_pipe)
            all_sprites.add(bottom_pipe)
            pipeIncr += 1
        
        gems.update()
        backgrounds.update()
        all_sprites.update()

        org_screen.fill((255, 255, 255))
        screen.fill((0, 0, 0))

        for pipe in pipes:
            scripts.check_score_increase(player, pipe)
        
        for gem in gems:
            if gem.rect.colliderect(gem.top_pipe.rect) or gem.rect.colliderect(gem.bottom_pipe.rect):
                gem.change_direction()
            if scripts.check_gem_increase(player, gem.rect):
                gem.play_collect_sound()
                player.score += 50 
                gems.remove(gem)
            if gem.did_leave_screen():
                gems.remove(gem)

        backgrounds.draw(screen)
        gems.draw(screen)
        all_sprites.draw(screen)
        scripts.draw_text(str(round(player.score)), game_font, (0, 0, 0), screen, 50, 50)

        if player.did_leave_screen():
            death_sound.play()
            offset = scripts.shake()
            gems.empty()
            game_over(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)

        did_player_collide = scripts.check_collisions(player, pipes)
        if did_player_collide == True and not player.dev_mode:
            gems.empty()
            death_sound.play()
            offset = scripts.shake()
            game_over(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)
        org_screen.blit(screen, next(offset)) 
        pygame.display.update()
        fps_clock.tick(FPS)

def game_over(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset):
    buttons.empty()
    mixer.music.load("Assets/SFX/happy.mp3")
    mixer.music.set_volume(0.5)
    # mixer.music.play(-1) # Uncomment this to play menu music.
    click = False
    pipe_count = 0

    main_menu_button = Button("Assets/Art/UI/Main-Menu-Button.png", (WIDTH/2-175, HEIGHT/2))
    leaderboard_button = Button("Assets/Art/UI/Leaderboard-Button.png", (WIDTH/2+175, HEIGHT/2))
    options_button = Button("Assets/Art/UI/Options-Button.png", (WIDTH/2-175, HEIGHT/2+100))
    quit_button = Button("Assets/Art/UI/Quit-Button.png", (WIDTH/2+175, HEIGHT/2+100))
    buttons.add(main_menu_button, leaderboard_button, options_button, quit_button)

    background_1 = Background(vec(WIDTH/2, HEIGHT/2))
    backgrounds.add(background_1)

    while True:
        screen.fill((0, 0, 0))
        backgrounds.draw(screen)
        buttons.draw(screen)

        scripts.draw_text("GAME OVER", title_font, (0, 0, 0), screen, WIDTH/2, HEIGHT/2-250)
        scripts.draw_text("Final Score: "+str(round(player.score)), title_font, (0, 0, 0), screen, WIDTH/2, HEIGHT/2-100)

        mouseX, mouseY = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if main_menu_button.click((mouseX, mouseY)):
                        main_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)
                    if leaderboard_button.click((mouseX, mouseY)):
                        leaderboard_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)
                    if options_button.click((mouseX, mouseY)):
                        options_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)
                    if quit_button.click((mouseX, mouseY)):
                        pygame.quit()
                        sys.exit()

        fps_clock.tick(FPS)
        org_screen.blit(screen, next(offset))
        pygame.display.update()

main_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)
