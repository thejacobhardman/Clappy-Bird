# Version 0.2.0

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
body_font = pygame.font.SysFont(None,24)

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
    def __init__(self, image_file, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.position = position
        self.rect = self.image.get_rect(center=self.position)
        self.id = "button"

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
        self.id = "player"
        self.score = 0
        self.dev_mode = False # <- Set this to True to disable the hopping movement for testing because I'm bad at Flappy Bird lol.

    def reset(self):
        self.position = vec(WIDTH/2-250, HEIGHT/2)
        self.image = pygame.transform.rotate(self.original_image, 0)
        self.rect = self.image.get_rect(center=self.position)
        self.vel = vec(0, 0)
        self.acceleration = vec(0, 0)
        self.score = 0

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

class Right_Hand(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Assets/Art/right_hand.png")
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

class Left_Hand(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Assets/Art/left_hand.png")
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
        self.passed_player = False
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
buttons = pygame.sprite.Group()
player = Player()
pipe_count = 0
logged_in = False

def main_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset):
    mixer.music.load("Assets/SFX/happy.mp3")
    mixer.music.set_volume(0.5)
    # mixer.music.play(-1) # Uncomment this to play menu music.
    if not mixer.get_busy():
        birds_sound.play(-1)

    scripts.reset_game(all_sprites, pipes, backgrounds, buttons, player)

    background_1 = Background(vec(WIDTH/2, HEIGHT/2))
    background_2 = Background(vec(WIDTH/2+2560, HEIGHT/2))
    backgrounds.add(background_1, background_2)


    play_button = Button("Assets/Art/UI/Play-Button.png", (WIDTH/2-175, HEIGHT/2))
    level_select_button = Button("Assets/Art/UI/Level-Select-Button.png", (WIDTH/2+175, HEIGHT/2))
    options_button = Button("Assets/Art/UI/Options-Button.png", (WIDTH/2-175, HEIGHT/2+100))

    login_button = Button("Assets/Art/UI/logintemp.png", (WIDTH/2-175, HEIGHT/2+250))
    register_button = Button("Assets/Art/UI/registertemp.png", (WIDTH/2+175, HEIGHT/2+250))
    

    quit_button = Button("Assets/Art/UI/Quit-Button.png", (WIDTH/2+175, HEIGHT/2+100))
    main_menu_buttons = [play_button, level_select_button, options_button, login_button, register_button, quit_button]
    buttons.add(main_menu_buttons)

    while True:
        screen.fill((0, 0, 0))
        backgrounds.draw(screen)
        buttons.draw(screen)

        scripts.draw_image("Assets/Art/clappy-bird-logo.png", screen, WIDTH/2, HEIGHT/2-150)

        if logged_in:
            scripts.draw_text("LOGGED IN", body_font, (0, 0, 0), screen, WIDTH/2-400, HEIGHT/2-300)
        else:
            scripts.draw_text("NOT LOGGED IN, PLEASE REGISTER", body_font, (0, 0, 0), screen, WIDTH/2-400, HEIGHT/2-300)
        
        mouseX, mouseY = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_button.click((mouseX, mouseY)):
                        game_loop(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)

                    if level_select_button.click((mouseX, mouseY)):
                        leaderboard_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)

                    if options_button.click((mouseX, mouseY)):
                        buttons.remove(main_menu_buttons)
                        options_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)

                    if login_button.click((mouseX, mouseY)):
                        #need to remove all buttons on current menu before loading new menu, otherwise they layer on top
                        buttons.remove(main_menu_buttons)
                        login_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)

                    if register_button.click((mouseX, mouseY)):
                        #need to remove all buttons on current menu before loading new menu, otherwise they layer on top
                        buttons.remove(main_menu_buttons)
                        register_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)

                    if quit_button.click((mouseX, mouseY)):
                        pygame.quit()
                        sys.exit()

        fps_clock.tick(FPS)
        org_screen.blit(screen, next(offset))
        pygame.display.update()

def leaderboard_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset):
    main_menu_button = Button("Assets/Art/UI/Main-Menu-Button.png", (WIDTH/2-175, HEIGHT/2))
    level_select_button = Button("Assets/Art/UI/Level-Select-Button.png", (WIDTH/2+175, HEIGHT/2))
    options_button = Button("Assets/Art/UI/Options-Button.png", (WIDTH/2-175, HEIGHT/2+100))
    quit_button = Button("Assets/Art/UI/Quit-Button.png", (WIDTH/2+175, HEIGHT/2+100))
    buttons.add(main_menu_button, level_select_button, options_button, quit_button)

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
                    if level_select_button.click((mouseX, mouseY)):
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
    level_select_button = Button("Assets/Art/UI/Level-Select-Button.png", (WIDTH/2+175, HEIGHT/2))
    options_button = Button("Assets/Art/UI/Options-Button.png", (WIDTH/2-175, HEIGHT/2+100))
    quit_button = Button("Assets/Art/UI/Quit-Button.png", (WIDTH/2+175, HEIGHT/2+100))

    options_menu_buttons = [main_menu_button, level_select_button, options_button, quit_button]

    buttons.add(options_menu_buttons)

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
                        buttons.remove(options_menu_buttons)
                        main_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)

                    if level_select_button.click((mouseX, mouseY)):
                        buttons.remove(options_menu_buttons)
                        leaderboard_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)

                    if options_button.click((mouseX, mouseY)):
                        buttons.remove(options_menu_buttons)
                        options_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)

                    if quit_button.click((mouseX, mouseY)):
                        pygame.quit()
                        sys.exit()

        fps_clock.tick(FPS)
        org_screen.blit(screen, next(offset))
        pygame.display.update()

def login_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset):
    back_button = Button("Assets/Art/UI/Back-Button.png", (WIDTH/2-500, HEIGHT/2-200))
    login_button = Button("Assets/Art/UI/logintemp.png", (WIDTH/2+300, HEIGHT/2+250))
    
    login_menu_buttons = [back_button, login_button]
    buttons.add(login_menu_buttons)

    username_rect = pygame.Rect(500,350,280,80)
    password_rect = pygame.Rect(500,450,280,80)

    base_font = pygame.font.Font(None, 32)

    #BACKEND - here is where username and password end up being stored
    username_entry = ''
    password_entry = ''

    color_active = pygame.Color('gold')
    color_passive = pygame.Color('lightblue3')

    username_color = color_passive
    password_color = color_passive

    usernameActive = False
    passwordActive = False

    while True:

        #Initial UI drawing
        screen.fill((0, 0, 0))
        backgrounds.draw(screen)
        buttons.draw(screen)

        scripts.draw_text("LOGIN", title_font, (0, 0, 0), screen, WIDTH/2, HEIGHT/2-100)
        scripts.draw_text("USERNAME", game_font, (0, 0, 0), screen, WIDTH/2-300, HEIGHT/2+30)
        scripts.draw_text("PASSWORD", game_font, (0, 0, 0), screen, WIDTH/2-300, HEIGHT/2+130)
        
        mouseX, mouseY = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:

                #Handling for Selecting Username Text field
                if username_rect.collidepoint(event.pos):
                    usernameActive = True
                else:
                    usernameActive = False
                    
                #Handling for Selecting Password Text field
                if password_rect.collidepoint(event.pos):
                    passwordActive = True
                else:
                    passwordActive = False
                
                #Handling for Back Button
                if event.button == 1:
                    if back_button.click((mouseX, mouseY)):
                        buttons.remove(login_menu_buttons)
                        main_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)
                        

                 #Handling for Login Button - INCOMPLETE, logged_in property also not changed yet
                    if login_button.click((mouseX, mouseY)):
                        buttons.remove(login_menu_buttons)
                        main_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)

            if event.type == pygame.KEYDOWN:

                #Handling for backspacing in username and password text entry
                if event.key == pygame.K_BACKSPACE:
                    if usernameActive:
                        username_entry = username_entry[:-1]
                    if passwordActive:
                        password_entry = password_entry[:-1]

                #Handling for typing in username and password text entry
                else:
                    if usernameActive:
                        username_entry += event.unicode
                    if passwordActive:
                        password_entry += event.unicode

        #Logic for selected color for username and password text entry
        if usernameActive:
            username_color = color_active
        else:
            username_color = color_passive

        if passwordActive:
            password_color = color_active
        else:
            password_color = color_passive

        #Drawing text boxes and rendering entry variables
        pygame.draw.rect(screen, username_color, username_rect)
        pygame.draw.rect(screen, password_color, password_rect)
        user_text_surface = game_font.render(username_entry, True, (255, 255, 255))
        pass_text_surface = game_font.render(password_entry, True, (255,255,255))

        screen.blit(user_text_surface, (username_rect.x+5, username_rect.y+5))
        screen.blit(pass_text_surface, (password_rect.x+5, password_rect.y+5))

        username_rect.w = max(100, user_text_surface.get_width()+10)
        password_rect.w = max(100, pass_text_surface.get_width()+10)

        fps_clock.tick(FPS)
        org_screen.blit(screen, next(offset))
        pygame.display.update()


def register_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset):
    back_button = Button("Assets/Art/UI/Back-Button.png", (WIDTH/2-500, HEIGHT/2-200))
    register_button = Button("Assets/Art/UI/registertemp.png", (WIDTH/2+300, HEIGHT/2+250))

    register_menu_buttons = [back_button, register_button]
    buttons.add(register_menu_buttons)

    username_rect = pygame.Rect(500,350,280,80)
    password_rect = pygame.Rect(500,450,280,80)

    base_font = pygame.font.Font(None, 32)

    #BACKEND - here is where username and password end up being stored
    username_entry = ''
    password_entry = ''

    color_active = pygame.Color('gold')
    color_passive = pygame.Color('lightblue3')

    username_color = color_passive
    password_color = color_passive

    usernameActive = False
    passwordActive = False

    while True:
        #Initial UI drawing
        screen.fill((0, 0, 0))
        backgrounds.draw(screen)
        buttons.draw(screen)

        scripts.draw_text("REGISTER", title_font, (0, 0, 0), screen, WIDTH/2, HEIGHT/2-100)

        scripts.draw_text("NEW USERNAME", game_font, (0, 0, 0), screen, WIDTH/2-300, HEIGHT/2+30)
        scripts.draw_text("NEW PASSWORD", game_font, (0, 0, 0), screen, WIDTH/2-300, HEIGHT/2+130)
        
        mouseX, mouseY = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:

                #Handling for Selecting Username Text field
                if username_rect.collidepoint(event.pos):
                    usernameActive = True
                else:
                    usernameActive = False
                    
                #Handling for Selecting Password Text field
                if password_rect.collidepoint(event.pos):
                    passwordActive = True
                else:
                    passwordActive = False

                #Handling for Back Button
                if event.button == 1:
                    if back_button.click((mouseX, mouseY)):
                        buttons.remove(register_menu_buttons)
                        main_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)

                #Handling for Register Button - INCOMPLETE, simply reroutes to main menu
                    if register_button.click((mouseX, mouseY)):
                        buttons.remove(register_menu_buttons)
                        main_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)
                    

            if event.type == pygame.KEYDOWN:

                 #Handling for backspacing in username and password text entry
                if event.key == pygame.K_BACKSPACE:
                    if usernameActive:
                        username_entry = username_entry[:-1]
                    if passwordActive:
                        password_entry = password_entry[:-1]

                #Handling for typing in username and password text entry
                else:
                    if usernameActive:
                        username_entry += event.unicode
                    if passwordActive:
                        password_entry += event.unicode

        #Logic for selected color for username and password text entry
        if usernameActive:
            username_color = color_active
        else:
            username_color = color_passive

        if passwordActive:
            password_color = color_active
        else:
            password_color = color_passive

        
         #Drawing text boxes and rendering entry variables

        pygame.draw.rect(screen, username_color, username_rect)
        pygame.draw.rect(screen, password_color, password_rect)
        user_text_surface = game_font.render(username_entry, True, (255, 255, 255))
        pass_text_surface = game_font.render(password_entry, True, (255,255,255))

        screen.blit(user_text_surface, (username_rect.x+5, username_rect.y+5))
        screen.blit(pass_text_surface, (password_rect.x+5, password_rect.y+5))

        username_rect.w = max(100, user_text_surface.get_width()+10)
        password_rect.w = max(100, pass_text_surface.get_width()+10)

        fps_clock.tick(FPS)
        org_screen.blit(screen, next(offset))
        pygame.display.update()

def game_loop(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset):
    x_offset = 0
    first_run = True
    counter = 3
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    birds_sound.stop()
    while True:
        # Plays a countdown at the start of the game.
        if first_run:
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
                first_run = False

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
        
        for pipe in pipes:
            scripts.check_score_increase(player, pipe)

        org_screen.fill((255, 255, 255))
        screen.fill((0, 0, 0))

        backgrounds.draw(screen)
        all_sprites.draw(screen)
        scripts.draw_text(str(round(player.score)), game_font, (0, 0, 0), screen, 50, 50)

        if player.did_leave_screen():
            death_sound.play()
            offset = scripts.shake()
            game_over(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)

        did_player_collide = scripts.check_collisions(player, pipes)
        if did_player_collide == True:
            death_sound.play()
            offset = scripts.shake()
            game_over(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)

        org_screen.blit(screen, next(offset))
        pygame.display.update()
        fps_clock.tick(FPS)

def game_over(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset):
    mixer.music.load("Assets/SFX/happy.mp3")
    mixer.music.set_volume(0.5)
    # mixer.music.play(-1) # Uncomment this to play menu music.
    if not mixer.get_busy():
        birds_sound.play(-1)
    pipe_count = 0

    scripts.reset_game(all_sprites, pipes, backgrounds, buttons, player)

    background_1 = Background(vec(WIDTH/2, HEIGHT/2))
    background_2 = Background(vec(WIDTH/2+2560, HEIGHT/2))
    backgrounds.add(background_1, background_2)

    main_menu_button = Button("Assets/Art/UI/Main-Menu-Button.png", (WIDTH/2-175, HEIGHT/2))
    level_select_button = Button("Assets/Art/UI/Level-Select-Button.png", (WIDTH/2+175, HEIGHT/2))
    options_button = Button("Assets/Art/UI/Options-Button.png", (WIDTH/2-175, HEIGHT/2+100))
    quit_button = Button("Assets/Art/UI/Quit-Button.png", (WIDTH/2+175, HEIGHT/2+100))
    buttons.add(main_menu_button, level_select_button, options_button, quit_button)

    while True:
        screen.fill((0, 0, 0))
        backgrounds.draw(screen)
        buttons.draw(screen)

        scripts.draw_text("GAME OVER", title_font, (0, 0, 0), screen, WIDTH/2, HEIGHT/2-100)
        mouseX, mouseY = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if main_menu_button.click((mouseX, mouseY)):
                        main_menu(all_sprites, pipes, backgrounds, buttons, player, pipe_count, offset)
                    if level_select_button.click((mouseX, mouseY)):
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