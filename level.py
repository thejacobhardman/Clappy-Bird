import librosa
import warnings


class Level:
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

        # credit: https://stackoverflow.com/questions/43877971/librosa-pitch-tracking-stft
        def detect_pitch(t, magnitude, pitches):
            index = magnitude[:, t].argmax()
            pitch = pitches[index, t]
            return pitch

        # try to normalize pitch list with level height
        for x in beat_frames:
            pitch_list.append(detect_pitch(x, magnitude, pitches))

        done = False
        pitches_processed = 0
        chunk_size = 10
        pipe_height_list = []

        while not done:
            mx = pitch_list[pitches_processed]
            mn = pitch_list[pitches_processed]
            for i in range(chunk_size):
                if pitches_processed + i >= len(pitch_list):
                    break
                if pitch_list[pitches_processed + i] > mx:
                    mx = pitch_list[pitches_processed + i]
                if (pitch_list[pitches_processed + i] < mn and pitch_list[pitches_processed + i] != 0) or mn == 0:
                    mn = pitch_list[pitches_processed + i]

            for i in range(chunk_size):
                if pitches_processed + i >= len(pitch_list):
                    break
                if pitch_list[i] == 0:
                    pipe_height_list.append(570)
                else:
                    if mx - mn == 0:
                        pipe_height_list.append(375)
                    else:
                        pipe_height_list.append(-420 * ((pitch_list[i] - mn) / (mx - mn)) + 570)

            if pitches_processed >= len(pitch_list) - 1:
                done = True

            pitches_processed += 1

        return pipe_height_list
