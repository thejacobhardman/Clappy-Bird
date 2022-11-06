
def get_pitches(song, tol):
    # Credit: https://stackoverflow.com/questions/54612204/trying-to-get-the-frequencies-of-a-wav-file-in-python
    from aubio import source, pitch
    win_s = 1000
    hop_s = 1000
    your_file = song
    s = source(your_file, 0, hop_s)
    samplerate = s.samplerate
    tolerance = 0.8
    pitch_o = pitch("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(tolerance)
    pitches = []
    confidences = []
    total_frames = 0
    while True:
        samples, read = s()
        pitch = pitch_o(samples)[0]
        pitches += [pitch]
        confidence = pitch_o.get_confidence()
        confidences += [confidence]
        total_frames += read
        if read < hop_s:
            break
    for i in range(len(pitches)):
        if confidences[i] < tol and i != 0:
            pitches[i] = pitches[i - 1]
    return pitches


class Level:

    def __init__(self, song: str):

        self.song = song
        self.tickRate = 0.8
        self.tick = 0
        self.nextPipeTick = 0
        self.currentPipe = 0
        self.data = []
        self.generate()

    # Generates the level data from the song
    def generate(self):

        pitches = get_pitches(self.song, 0.9)

        # Find maximum and minimum of pitches
        mx = pitches[0]
        mn = pitches[0]
        for pitch in pitches:
            if pitch > mx:
                mx = pitch
            if (pitch < mn and pitch != 0) or mn == 0:
                mn = pitch

        # For now, I will try to manually detect onsets
        dist = 1
        tol = 0.5
        for i in range(1, len(pitches)):
            diff = pitches[i] - pitches[i - 1]
            if (diff > tol or diff < -tol) and pitches[i] != 0:
                height = (-420 * ((pitches[i] - mn) / (mx - mn))) + 570
                self.data += [dict(dist=dist, height=height)]
                dist = 0
            dist += 1

    # This should be called every game loop iteration.
    # Returns the height of a potential pipe to be spawned in, or -1 if no pipe should be spawned in
    # Might split into multiple methods later for tighter cohesion
    def spawn_update(self):
        if self.nextPipeTick == -1:
            return -1
        pipe = self.data[self.currentPipe]
        distanceToNext = self.nextPipeTick - self.tick
        if distanceToNext <= 0:
            self.tick += self.tickRate
            self.currentPipe += 1
            if self.currentPipe < len(self.data):
                self.nextPipeTick += self.data[self.currentPipe]["dist"]
            else:
                self.nextPipeTick = -1
            return pipe["height"]
        self.tick += self.tickRate
        return -1
