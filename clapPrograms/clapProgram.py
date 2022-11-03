import pyaudio
import struct
import matplotlib.pyplot as plt
import numpy as np
import time


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
                                 frames_per_buffer = INPUT_FRAMES_PER_BLOCK)
        return stream

    # listens for loud objects, and prints them to console
    def listen(self):

        
        fig,ax = plt.subplots()                                             #
        x = np.arange(0,INPUT_FRAMES_PER_BLOCK*2,2)                         # Set up our graph plot with random np data, arange puts the spaced time numbers
        line, = ax.plot(x, np.random.rand(INPUT_FRAMES_PER_BLOCK),'r')      #


        ax.set_ylim(-32700,32700)                                           #
        ax.set_xlim = (0,INPUT_FRAMES_PER_BLOCK)                            # Set the x and y limits for our graph and show it
        fig.show()                                                          #

        start = time.time()

        # while true
        while 1:
            try:
                # read stream for next audio block
                data = self.stream.read(INPUT_FRAMES_PER_BLOCK)
                # convert to int from base16
                dataInt = struct.unpack(str(INPUT_FRAMES_PER_BLOCK) + 'h', data)

                # iterate audio block
                for x in dataInt:
                    # TODO -- normalize each data point

                    stop = time.time()

                    # break out of audio block if loud object found (if x is above certain amplitude)
                    if x > 10000 and stop - start > 0.2:
                        start = time.time()
                        print("loud object")
                        print(x)
                        break
                
                # constantly redraw audio data to plot
                line.set_ydata(dataInt)
                fig.canvas.draw()
                fig.canvas.flush_events()
            
            # errors printed to console
            except IOError as e:
                self.errorcount += 1
                print( "(%d) Error recording: %s"%(self.errorcount,e) )
                return
            
# runs on main thread
if __name__ == "__main__":
    tt = ClapTester()
    tt.listen()