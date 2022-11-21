import pygame as pg
import globals as g
import scripts
import sprites.entities.gem
import sprites.entities.pipe
import sprites.entities.player


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

    def set_song(self, path, data):
        self.song_path = path
        self.level = data

    def spawn_pipe_set(self, height, gap_size, has_gem):
        top_pipe = sprites.entities.pipe.Pipe("top", 500, height - gap_size)
        bottom_pipe = sprites.entities.pipe.Pipe("bottom", 500, height + gap_size)

        if has_gem:
            gem = sprites.entities.gem.Gem(500, height, top_pipe, bottom_pipe)
            self.gems.add(gem)

        self.pipes.add(top_pipe)
        self.pipes.add(bottom_pipe)

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

    def update(self):

        # Oof
        self.levelTick += 1
        musicTick = (pg.time.get_ticks() - self.start_ticks) / 1000
        pipe_list = self.level.pipe_list
        if self.levelTick == 140 and not self.music_started:
            self.music_started = True
            pg.mixer.music.play(-1)
        if self.pipeIncr < len(pipe_list) and musicTick >= pipe_list[self.pipeIncr]['spawn']:
            self.spawn_pipe_set(self.level.pipe_list[self.pipeIncr]['height'], 520, True)
            self.pipeIncr += 1
            self.noMiddlePipe = True
        elif self.pipeIncr < len(pipe_list) and self.pipeIncr != 0 and musicTick >= pipe_list[self.pipeIncr - 1]['spawn'] + (
                (pipe_list[self.pipeIncr]['spawn'] - pipe_list[self.pipeIncr - 1]['spawn']) / 2) and self.noMiddlePipe:
            self.spawn_pipe_set(pipe_list[self.pipeIncr - 1]['height'] + (
                        pipe_list[self.pipeIncr]['height'] - pipe_list[self.pipeIncr - 1]['height']) / 2, 520, False)
            self.noMiddlePipe = False

        # Only update the background when the game is happening
        g.backgrounds.update()

        # Update and draw the sprites
        self.players.update()
        self.gems.update()
        self.pipes.update()
        self.players.draw(g.screen)
        self.gems.draw(g.screen)
        self.pipes.draw(g.screen)

        # Draw the player's score
        scripts.draw_text(str(round(self.player.score)), g.game_font, (0, 0, 0), g.screen, 50, 50)
