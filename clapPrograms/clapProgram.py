import pyaudio
import struct
import matplotlib.pyplot as plt
import numpy as np

FORMAT = pyaudio.paInt16 
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 1
RATE = 44100  
INPUT_BLOCK_TIME = 0.1
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)

class TapTester(object):
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.stream = self.open_mic_stream()
        self.errorcount = 0

    def stop(self):
        self.stream.close()

    def open_mic_stream( self ):

        stream = self.pa.open(   format = FORMAT,
                                 channels = CHANNELS,
                                 rate = RATE,
                                 input = True,
                                 frames_per_buffer = INPUT_FRAMES_PER_BLOCK)
        return stream

    def listen(self):

        fig,ax = plt.subplots()
        x = np.arange(0,INPUT_FRAMES_PER_BLOCK*2,2)
        line, = ax.plot(x, np.random.rand(INPUT_FRAMES_PER_BLOCK),'r')
        ax.set_ylim(-32700,32700)
        ax.set_xlim = (0,INPUT_FRAMES_PER_BLOCK)
        fig.show()

        while 1:
            try:
                data = self.stream.read(INPUT_FRAMES_PER_BLOCK)
                dataInt = struct.unpack(str(INPUT_FRAMES_PER_BLOCK) + 'h', data)
                #listData = list(dataInt)
                for x in dataInt:
                    num = x * SHORT_NORMALIZE
                    if num > .8:
                        print("loud object")
                        print(np.amax(dataInt))
                        break
                line.set_ydata(dataInt)
                fig.canvas.draw()
                fig.canvas.flush_events()
            except IOError as e:
                # dammit. 
                self.errorcount += 1
                print( "(%d) Error recording: %s"%(self.errorcount,e) )
                return
            

if __name__ == "__main__":
    tt = TapTester()
    print("working")
    tt.listen()