import random
import pygame as pg
import globals as g
import scripts
import sprites.entities.gem
import sprites.entities.pipe
import sprites.entities.player
import hashlib


# This is the scene where the player is able to actually control Clappy Bird and fly through pipes.
class Game:

    def __init__(self):
        self.player = None
        self.players = pg.sprite.Group()
        self.gems = pg.sprite.Group()
        self.pipes = pg.sprite.Group()
        self.song_path = ""
        self.level = None
        self.start_ticks = 0
        self.music_started = False
        self.pipeIncr = 0
        self.levelTick = 0
        self.noMiddlePipe = True
        self.spawnChance = 0
        self.difficulty = ""
        self.songseed = 0

    def set_song(self, path, data):
        self.song_path = path
        self.level = data
        # Hashing code taken from - https://stackoverflow.com/questions/16008670/how-to-hash-a-string-into-8-digits
        self.songseed = int(hashlib.sha1(path.encode("utf-8")).hexdigest(), 16) % (10 ** 8)

    def spawn_pipe_set(self, height, gap_size, has_gem, mid_pipe):
        top_pipe = sprites.entities.pipe.Pipe("top", 500, height - gap_size)
        bottom_pipe = sprites.entities.pipe.Pipe("bottom", 500, height + gap_size)

        if has_gem:
            gem = sprites.entities.gem.Gem(500, height, top_pipe, bottom_pipe)
            self.gems.add(gem)

        if mid_pipe:
            top_pipe.set_width(100)
            bottom_pipe.set_width(100)

        self.pipes.add(top_pipe)
        self.pipes.add(bottom_pipe)
    
    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

    # Called as soon as the game scene is switched to with scripts.change_scene()
    def init(self):
        g.birds_sound.stop()
        self.player = sprites.entities.player.Player()
        self.players = pg.sprite.Group(self.player)
        self.gems = pg.sprite.Group()
        self.pipes = pg.sprite.Group()
        self.start_ticks = pg.time.get_ticks()
        self.music_started = False
        self.pipeIncr = 0
        self.levelTick = 0
        self.noMiddlePipe = True
        random.seed(self.songseed)
        pg.mixer.music.set_endevent(g.Song_win)

    # Called every frame that this scene is active (see scene.py)
    def update(self):

        # Oof
        if self.difficulty == 'Normal':
            self.spawnChance = random.randint(0,8)
        elif self.difficulty == 'Hard':
            self.spawnChance = random.randint(0,3)
        elif self.difficulty == 'Extreme':
            self.spawnChance = 2
        self.levelTick += 1
        musicTick = (pg.time.get_ticks() - self.start_ticks) / 1000
        pipe_list = self.level.pipe_list
        if self.levelTick == 140 and not self.music_started:
            self.music_started = True
            pg.mixer.music.play()
        if self.pipeIncr < len(pipe_list) and musicTick >= pipe_list[self.pipeIncr]['spawn']:
            self.spawn_pipe_set(self.level.pipe_list[self.pipeIncr]['height'], 520, True, False)
            self.pipeIncr += 1
            self.noMiddlePipe = True
        elif self.pipeIncr < len(pipe_list) and self.pipeIncr != 0 and musicTick >= pipe_list[self.pipeIncr - 1]['spawn'] + (
                (pipe_list[self.pipeIncr]['spawn'] - pipe_list[self.pipeIncr - 1]['spawn']) / 2) and self.noMiddlePipe and self.spawnChance == 2:
            self.spawn_pipe_set(pipe_list[self.pipeIncr - 1]['height'] + (
                        pipe_list[self.pipeIncr]['height'] - pipe_list[self.pipeIncr - 1]['height']) / 2, 520, False, True)
            self.noMiddlePipe = False

        for event in g.events:
            if event.type == g.Song_win:
                scripts.change_scene("Win_screen")

        # Only update the background when the game is happening
        g.backgrounds.update()

        # Update and draw the sprites
        self.players.update()
        self.gems.update()
        self.pipes.update()
        self.players.draw(g.screen)
        self.gems.draw(g.screen)
        self.pipes.draw(g.screen)\

        # Draw the player's score
        scripts.draw_text(str(round(self.player.score)), g.game_font, (0, 0, 0), g.screen, 50, 50)
