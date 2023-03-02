# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 23:03:31 2023

@author: Pavan Kumar J

"""
import numpy as np
from scipy.signal import find_peaks
import soundfile as sf
import matplotlib.pyplot as plt

def simple_vad_trail(sig):
    
    rxx = np.abs(np.correlate(sig,sig,mode='full'))    
    th1 = np.max(rxx)
    th2 = np.mean(rxx)
    th3 = np.median(rxx)
    p = 0.1
    q = 0.5
    th = (p*th1)+(q*th2)+((1-p-q)*th3)
    r = np.zeros(np.shape(rxx))
    idx = np.where(rxx>=th)[0]
    r[idx] = rxx[idx]
    
    peaks,_ = find_peaks(r)
    peaks = len(peaks)
    return (r,peaks)


def simple_vad(sig):
    rxx = np.abs(np.correlate(sig,sig,mode='full'))    
    ths = np.std(rxx)
    peaks,_ = find_peaks(rxx, threshold=0.15*ths,width=3)
    peaks = len(peaks)
    return (rxx,peaks)

fs = 16000 #sampling rate 


signal, Fs = sf.read("openday_test2.wav")
#signal = signal/np.linalg.norm(signal)

win = 1000 # Short time window length =40ms
steps = int(len(signal)/win)

peaks = []
rxx = []
for i in range(steps):
    sig = signal[i*win:(i+1)*win]
    r,p = simple_vad(sig)
    plt.plot(r)
    peaks.append(p)
    rxx.append(r)

    

rxx = np.array(rxx)
rxx = np.transpose(rxx)
peaks = np.array(peaks)
n = np.linspace(0,len(peaks)-1,len(peaks))

fig, axs = plt.subplots(2,1,figsize=(8.27, 11.69))
fig.suptitle("Results", fontsize=16)
axs = axs.ravel()

axs[0].plot(signal)
axs[0].set_title('audio_signal')


axs[1].step(n,peaks)
axs[1].set_title('Peaks detected')
axs[1].set_xlabel('n')
axs[1].set_ylabel('Peaks')

fig.tight_layout()
fig.subplots_adjust(top=0.88)
#plt.show()
plt.savefig("openday_code_test2.pdf", format="pdf")
plt.close()






