from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np

wavArray = wavfile.read("clapSample.wav", mmap=False)

data = wavArray[1]

data_length = len(data)

wav_length = data_length / wavArray[0]

amplitude_array = []
tempArray = []

for x in range(len(data)):
    tempArray = []
    for y in range(len(data[x])):
       tempNum = data[x][y] 
       tempNum = tempNum/32767.
       tempArray.append(tempNum)
    amplitude_array.append(tempArray)

amplitude_array = np.array(amplitude_array)

time = np.linspace(0., wav_length, data_length)
plt.plot(time, amplitude_array[:, 0], label="Left channel")
plt.plot(time, amplitude_array[:, 1], label="Right channel")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()