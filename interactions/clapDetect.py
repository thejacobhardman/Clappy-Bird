import pyaudio
import struct
import time
from pynput.keyboard import Key, Controller
import globals as g


# Base16 format that .wav is saved as
FORMAT = pyaudio.paInt16 

# Normalize audio by dividing it by 32,768 (this is max value for our base16 format)
SHORT_NORMALIZE = (1.0/32768.0)

# Audio Channels
CHANNELS = 1

# Rate is the audio quality, indicates how many frames we save per second
RATE = 44100  

# Length of time (in seconds) for each audio block
INPUT_BLOCK_TIME = 0.1

# Total frames per block (length of our numpy array)
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)

# Clap detect minimum interval - claps cannot be detected faster than this float in seconds
MIN_CLAP = 0.2



class ClapTester(object):
    def __init__(self):

        # Our pyAudio object initialization
        self.pa = pyaudio.PyAudio()

        # Return an open mic stream
        self.stream = self.open_mic_stream()

        # Count for errors encountered
        self.errorcount = 0

    def stop(self):
        self.stream.close()

    def open_mic_stream( self ):

        # stream is a py.audio object that we open using our parameters
        stream = self.pa.open(   format = FORMAT,
                                 channels = CHANNELS,
                                 rate = RATE,
                                 input = True,
                                 frames_per_buffer = INPUT_FRAMES_PER_BLOCK,
                                 input_device_index=g.selected_audio_device.get('index'))
        print(g.selected_audio_device.get('index'))
        print(g.selected_audio_device.get('name'))
        return stream

    # listens for loud objects, and prints them to console
    def listen(self):                                                       

        start = time.time()

        # memory to store amp values
        amp_mem = []
        for i in range(200): # initializes 200 slots to memory
            amp_mem.append(0)

        amp_itter = 0

        # while true
        while 1:
            try:
                # read stream for next audio block
                data = self.stream.read(INPUT_FRAMES_PER_BLOCK)
                # convert to int from base16
                dataInt = struct.unpack(str(INPUT_FRAMES_PER_BLOCK) + 'h', data)
                # iterate audio block
                for x in dataInt:
                    if x > 0:
                        amp_mem[amp_itter] = x
                        amp_itter += 1
                        if amp_itter == 200:
                            amp_itter = 0              

                    # average amplitude of the noise
                    amplitude_noise = sum(amp_mem) / len(amp_mem)

                    count = 0

                    if x > amplitude_noise + 20000:
                        stop = time.time()

                        for amp in amp_mem:
                            if amp > amplitude_noise + 20000:
                                count += 1
                            if count > 2: 
                                break
                        if count <= 2 and count > 0 and stop - start > MIN_CLAP:     
                            start = time.time()

                            # clap in clappy bird
                            with open('interactions\interactions.txt', 'w') as writer:
                                writer.write("CLAP")    

                            break
            
            # return upon error
            except:
                return
            
# runs on main thread
if __name__ == "__main__":
    tt = ClapTester()
    tt.listen()