import librosa
import warnings



class OtherLevel():
    def __init__(self, song: str):
        self.song = song
        self.pipe_spawnList = self.get_beat_times(song)

    def get_beat_times(self, song):
        x, sr = librosa.load(song)
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            tempo, beat_times = librosa.beat.beat_track(x, sr=sr, start_bpm=60, units='time')
            return beat_times