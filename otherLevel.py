import librosa
import warnings



class OtherLevel():
    def __init__(self, song: str):
        self.song = song
        x, sr = librosa.load(song)
        self.beat_frames = self.get_beat_frames(x, sr)
        self.pipe_height_list = self.get_pitch_range(self.beat_frames, x , sr)
        self.pipe_spawnList = self.get_times(self.beat_frames, sr)
        self.pipe_list = []
        for x in range(len(self.pipe_spawnList)):
            self.pipe_list += [dict(spawn=self.pipe_spawnList[x], height=self.pipe_height_list[x])]


    # get time signature beat onsets as frames
    def get_beat_frames(self, x, sr):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            tempo, beat_frames = librosa.beat.beat_track(x, sr=sr, start_bpm=60, units='frames')
            return beat_frames

    # convert frames to times
    def get_times(self, beat_frames, sr):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            beat_times = librosa.frames_to_time(beat_frames, sr=sr)
            return beat_times
    # collect pitch and magnitude ranges
    def get_pitch_range(self, beat_frames, x, sr):
            pitches, magnitude = librosa.piptrack(y=x, sr=sr)
            pitch_list = []

            #credit: https://stackoverflow.com/questions/43877971/librosa-pitch-tracking-stft
            def detect_pitch(t, magnitude, pitches):
                index = magnitude[:, t].argmax()
                pitch = pitches[index, t]
                return pitch

            # try to normalize pitch list with level height
            for x in range(len(beat_frames)):
                pitch_list.append(detect_pitch(x, magnitude, pitches))
            mx = pitch_list[0]
            mn = pitch_list[0]
            for pitch in pitch_list:
                if pitch > mx:
                    mx = pitch
                if (pitch < mn and pitch != 0) or mn == 0:
                    mn = pitch
            pipe_height_list = []
            for i in range(len(pitch_list)):
                pipe_height_list.append(-420 * ((pitch_list[i] - mn) / (mx - mn))+570)
            return pipe_height_list