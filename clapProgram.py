import pyaudio
import struct
import matplotlib.pyplot as plt
import numpy as np
import time
from pynput.keyboard import Key, Controller


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

        
        #fig, (ax,ax1) = plt.subplots(2)  
        #x_fft = np.linspace(0, RATE, INPUT_FRAMES_PER_BLOCK)                                           
        #x = np.arange(0,INPUT_FRAMES_PER_BLOCK*2,2)                        
        #line, = ax.plot(x, np.random.rand(INPUT_FRAMES_PER_BLOCK),'r')
        #line_fft, = ax1.semilogx(x_fft, np.random.rand(INPUT_FRAMES_PER_BLOCK), 'b')  #makes another graph for frequency
              


        #ax.set_ylim(-32000,3200)                                           
        #ax.set_xlim = (0,INPUT_FRAMES_PER_BLOCK)
        #ax1.set_xlim(20,RATE/2)           #                                
        #ax1.set_ylim = (0,1)              #sets y to be 0-1 due to normalization              
        # fig.show()                                                          

        start = time.time()

        # memory to store amp values
        amp_mem = []
        for i in range(200): # initializes 200 slots to memory
            amp_mem.append(0)

        amp_itter = 0

        keyboard = Controller()

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
                        amp_mem[amp_itter % 200] = x
                        amp_itter += 1

                    amplitude_noise = sum(amp_mem) / len(amp_mem)

                    count = 0

                    if x > amplitude_noise + 20000:
                        stop = time.time()

                        for amp in amp_mem:
                            if amp > amplitude_noise + 20000:
                                count += 1
                            if count > 2: 
                                print("Sustained Noise")
                                break
                        if count <= 2 and count > 0 and stop - start > 0.3:     
                            start = time.time()

                            # jump in clappy bird    
                            keyboard.press(Key.space)
                            time.sleep(0.1)
                            keyboard.release(Key.space)

                            print("Detected Clap")
                            print(x)
                            break
                    

                    # break out of audio block if loud object found (if x is above certain amplitude)
                    """if x > 20000 and stop - start > 0.2:
                        start = time.time()
                        print(amp_mem)
                        
                        print("loud object")
                        print(x)
                        break"""
                
                # constantly redraw audio data to plot
                #line.set_ydata(dataInt)
                #line_fft.set_ydata(np.abs(np.fft.fft(dataInt))*2/(11000*INPUT_FRAMES_PER_BLOCK)) # gets frequency with fast fourier transform
                #fig.canvas.draw()
                #fig.canvas.flush_events()
            
            # errors printed to console
            except IOError as e:
                self.errorcount += 1
                print( "(%d) Error recording: %s"%(self.errorcount,e) )
                return
            
# runs on main thread
if __name__ == "__main__":
    tt = ClapTester()
    tt.listen()