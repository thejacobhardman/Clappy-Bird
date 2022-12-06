import random
import pygame as pg
import globals as g
import scripts
import sprites.entities.gem
import sprites.entities.pipe
import sprites.entities.player
import hashlib
import requests
import json


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
        self.customSong = False
        self.gemValue = 50
        self.pipe_gap = 620
        self.midpipe_gap = 580
        self.variance = 0

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
        self.set_static_difficulty_changes(self.difficulty)
        random.seed(self.songseed)
        pg.mixer.music.set_endevent(g.Song_win)

    # Called every frame that this scene is active (see scene.py)
    def update(self):

        # Oof
        self.set_nonstatic_difficulty_changes(self.difficulty)

        self.levelTick += 1

        musicTick = (pg.time.get_ticks() - self.start_ticks) / 1000

        if self.levelTick == 140 and not self.music_started:
            self.start_music()

        if self.is_beat_pipe_spawn(musicTick=musicTick):
            self.spawn_pipe_set(
                self.level.pipe_list[self.pipeIncr]['height'], self.pipe_gap + self.variance, True, False)
            self.pipeIncr += 1
            self.noMiddlePipe = True

        elif self.is_mid_pipe_spawn(musicTick=musicTick):
            self.spawn_pipe_set(self.level.pipe_list[self.pipeIncr - 1]['height'] + (
                self.level.pipe_list[self.pipeIncr]['height'] - self.level.pipe_list[self.pipeIncr - 1]['height']) / 2, self.midpipe_gap + self.variance, False, True)
            self.noMiddlePipe = False


        print(self.song_path)
        if self.player.life <= 0:
            pg.mixer.music.stop()
            self.gems.empty()
            if g.logged_in & (self.song_path in g.songs) & (self.customSong == False) & (self.player.absolute_unit == False):

                headers = {"Authorization": g.token}
                response = requests.get(g.api_url + "/score/" +
                                        g.userId + "/" + str(g.songs.index(self.song_path) + 1), headers=headers)
                print(json.dumps(response.json(), indent=4))

                # First time playing level, so post score
                if response.status_code == 500:
                    bodyData = {"player": g.userId,
                                "username": g.username,
                                "leaderboard": g.songs.index(self.song_path) + 1,
                                "highscore": int(self.player.score)}
                    response = requests.post(
                        (g.api_url + "/score/" + g.userId), json=bodyData, headers=headers)

                    if response.status_code != 201:
                        # Save data from HTTP response
                        print("Error updating score")
                    print(json.dumps(response.json(), indent=4))
                    print(int(self.player.score))
                    scripts.change_scene("game_over")

                # Already has score, so update if new score is higher
                else:
                    high_score = response.json()["data"]["data"]["highscore"]

                    if self.player.score > high_score:

                        bodyData = {"player": g.userId,
                                    "username": g.username,
                                    "leaderboard": g.songs.index(self.song_path) + 1,
                                    "highscore": int(self.player.score)}
                        response = requests.put(
                            (g.api_url + "/score/" + g.userId + "/" + str(g.songs.index(self.song_path) + 1)), json=bodyData, headers=headers)

                        if response.status_code != 200:
                            # Save data from HTTP response
                            print("Error updating score")

                            # Navigate to new menu
                        scripts.change_scene("game_over")
                    else:
                        scripts.change_scene("game_over")
            else:
                scripts.change_scene("game_over")

        for event in g.events:
            if event.type == g.Song_win:
                if g.logged_in & (g.songs.index(self.song_path) != None) & (self.customSong == False) & (self.player.absolute_unit == False):

                    headers = {"Authorization": g.token}
                    response = requests.get(g.api_url + "/score/" +
                                            g.userId + "/" +
                                            str(g.songs.index(self.song_path) + 1),
                                            headers=headers)

                    # First time playing level, so post score
                    if response.status_code == 500:
                        bodyData = {"player": g.userId,
                                    "username": g.username,
                                    "leaderboard": g.songs.index(self.song_path) + 1,
                                    "highscore": int(self.player.score)}
                        response = requests.post(
                            (g.api_url + "/score/" + g.userId), json=bodyData, headers=headers)

                        if response.status_code != 201:
                            # Save data from HTTP response
                            print("Error updating score")

                        scripts.change_scene("game_over")

                    # Already has score, so update if new score is higher
                    else:
                        high_score = response.json(
                        )["data"]["data"]["highscore"]

                        if self.player.score > high_score:

                            bodyData = {"player": g.userId,
                                        "username": g.username,
                                        "leaderboard": str(g.songs.index(self.song_path) + 1),
                                        "highscore": int(self.player.score)}
                            response = requests.put(
                                (g.api_url + "/score/" + g.userId + "/" + str(g.songs.index(self.song_path) + 1)), json=bodyData, headers=headers)

                            if response.status_code != 200:
                                # Save data from HTTP response
                                print("Error updating score")

                                # Navigate to new menu
                            scripts.change_scene("Win_screen")
                        else:
                            scripts.change_scene("Win_screen")
                else:
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
        scripts.draw_text(str(round(self.player.score)),
                            g.game_font, (0, 0, 0), g.screen, 50, 50)
        scripts.draw_text("Hitpoints: "+str(round(self.player.life)),
                            g.game_font, (0, 0, 0), g.screen, 300, 50)

    #Song Methods -------------------------------------------------------

    def set_song(self, path, data):
        self.song_path = path
        self.level = data
        # Hashing code taken from - https://stackoverflow.com/questions/16008670/how-to-hash-a-string-into-8-digits
        self.songseed = int(hashlib.sha1(
            path.encode("utf-8")).hexdigest(), 16) % (10 ** 8)

    def set_songFlag(self, flag):
        self.customSong = flag

    def start_music(self):
        self.music_started = True
        pg.mixer.music.play()

    #Spawn pipe Method --------------------------------------------------

    def spawn_pipe_set(self, height, gap_size, has_gem, mid_pipe):
        top_pipe = sprites.entities.pipe.Pipe("top", 500, height - gap_size)
        bottom_pipe = sprites.entities.pipe.Pipe(
            "bottom", 500, height + gap_size)

        if has_gem:
            gem = sprites.entities.gem.Gem(
                500, height, top_pipe, bottom_pipe, self.gemValue)
            self.gems.add(gem)

        if mid_pipe:
            top_pipe.set_width(100)
            bottom_pipe.set_width(100)

        self.pipes.add(top_pipe)
        self.pipes.add(bottom_pipe)

    def is_beat_pipe_spawn(self, musicTick):

        # return if the pipe_list still has pipes to spawn, and the music tick matches or exceeds the pipe spawn time
        if self.pipeIncr < len(self.level.pipe_list) and musicTick >= self.level.pipe_list[self.pipeIncr]['spawn']:
            return True

    def is_mid_pipe_spawn(self, musicTick):

        # return if the pipe_list still has pipes to spawn, the music tick matches or exceeds the pipe spawn time, and a middle pipe can spawn
        # middle pipe conditions - no middle pipe already, and must spawn at the average distance between two beat pipes
        if self.pipeIncr < len(self.level.pipe_list) and self.pipeIncr != 0 and musicTick >= self.level.pipe_list[self.pipeIncr - 1]['spawn'] + (
                (self.level.pipe_list[self.pipeIncr]['spawn'] - self.level.pipe_list[self.pipeIncr - 1]['spawn']) / 2) and musicTick < self.level.pipe_list[self.pipeIncr - 1]['spawn'] + (
                ((self.level.pipe_list[self.pipeIncr]['spawn'] - self.level.pipe_list[self.pipeIncr - 1]['spawn']) / 2) + .05) and self.noMiddlePipe and self.spawnChance == 2:
            return True

    #Difficulty Methods --------------------------------------------------------

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

    def set_static_difficulty_changes(self, difficulty):
        if difficulty == 'Easy':
            self.spawnChance = 0
            self.gemValue = 5
            self.player.life = 10
            self.player.change = 4
            self.pipe_gap = 620
            self.midpipe_gap = 580
        elif difficulty == 'Normal':
            self.gemValue = 10
            self.player.life = 5
            self.player.change = 3
            self.pipe_gap = 600
            self.midpipe_gap = 560
        elif difficulty == 'Hard':
            self.gemValue = 15
            self.player.life = 4
            self.pipe_gap = 600
            self.midpipe_gap = 540
        elif difficulty == 'Extreme':
            self.gemValue = 25
            self.spawnChance = 2
            self.player.life = 2
            self.player.change = 1.5
            self.pipe_gap = 600
            self.midpipe_gap = 550

    def set_nonstatic_difficulty_changes(self, difficulty):
        if difficulty == 'Normal':
            self.spawnChance = random.randint(0, 20)
        elif difficulty == 'Hard':
            self.spawnChance = random.randint(0, 10)
            self.variance == random.randint(-20,0)
        elif difficulty == 'Extreme':
            self.variance == random.randint(-50,-20)