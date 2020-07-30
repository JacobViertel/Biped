from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
from subprocess import call

jaw_data =[]
sample_rate, data = wavfile.read('test.wav')
sam = 25

amount_of_samples = len(data)
length_of_sound = amount_of_samples / sample_rate
# print("Sample rate:", sample_rate)
# print("Amount of samples:", amount_of_samples)
# print("Length of sound:", round(length_of_sound, 2), "seconds")
avg = 0
cnt = 0
for i in range(len(data)):
    if cnt == 0 or cnt % (sample_rate/2) ==0:
        for j in range(sam):
            avg += data[i]
        if avg < 0:
            jaw_data.append(-avg/sam)
        else:
            jaw_data.append(avg/sam)
    avg = 0
    cnt+=1
cnt = amount_of_samples-1
for i in range(sam):
    avg += data[cnt]
    cnt -=1
if avg < 0:
    jaw_data.append(-avg/sam)
else:
    jaw_data.append(avg/sam)
# print(jaw_data)
avg = 0
cnt = 0
minvalue = min(jaw_data)
maxvalue = max(jaw_data)
# print(minvalue)
# print(maxvalue)
# print(jaw_data)

jaw_motions = []
for i in range(len(jaw_data)):
    norm_val = float(jaw_data[i]-minvalue)/maxvalue
    # print(norm_val)
    if norm_val <= 0.01:
        jaw_motions.append("000")
    elif norm_val <= 0.05:
        jaw_motions.append("001")
    elif norm_val <= 0.1:
        jaw_motions.append("010")  
    elif norm_val <= 0.17:
        jaw_motions.append("011")
    elif norm_val <= 0.225:
        jaw_motions.append("100")  
    elif norm_val <= 0.275:
        jaw_motions.append("101")  
    else: 
        jaw_motions.append("110")
# print(jaw_motions)  

for i in range(2):
    x = jaw_motions[i]
    z = call("python3.7 /home/biped/catkin_ws/src/jacob/sound2jaw/half_adder_voice.py {}".format(x), shell=True)
	

#include qunatum adder!

spf = wave.open("test.wav", "r")
# 
# Extract Raw Audio from Wav File
#signal = spf.readframes(-1)
#signal = np.fromstring(signal, "Int16")

# 
# If Stereo
#if spf.getnchannels() == 2:
#    print("Just mono files")
#    sys.exit(0)
# 
#plt.figure(1)
#plt.title("Signal Wave...")
#plt.plot(signal)
#plt.show()