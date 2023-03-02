# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 23:03:31 2023
@author: Pavan Kumar J
"""
import numpy as np
from scipy.signal import find_peaks
import soundfile as sf
import matplotlib.pyplot as plt
import librosa

from server_latest import sending_data

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


    # return (r,peaks)

i = 0
peaks_avg = list()
FRAME_LEN = 10

def simple_vad(sig, connection,  FRAME_LEN=FRAME_LEN, i=i):
    # print('simple_vad:before reshape sig = ', sig.shape)
    sig = np.reshape(sig, sig.size)
    # print('simple_vad: after reshaping sig = ', sig.shape)
    rxx = np.abs(np.correlate(sig,sig,mode='full'))    
    ths = np.std(rxx)
    peaks,_ = find_peaks(rxx, threshold=0.25*ths,width=3)
    # peaks = len(peaks)
    # Pavan added the below line. commenting to test if just len(peaks) will make the fan run more frequentlu
    #peaks = round(len(peaks)*rxx[len(sig)-1])
    peaks = round(len(peaks))


    # global i
    global peaks_avg
    # global FRAME_LEN
    
    peaks_avg.append(peaks)
    i += 1

    # def scale_values(pass_list):
    #     scaled_list=[]
    #     for i in pass_list:
    #         i=i/10
    #         i=

    print(f'frame len = {FRAME_LEN}')
    if  len(peaks_avg) == FRAME_LEN :
        val = np.mean(peaks_avg)

        val = (val/10)
        #val= 100/(1+np.exp(-val/30))
        val = np.log10(val+10)*62

        # val = np.tanh(val/50)*100 # Did not get the fan to move fast enough. Also stopped the fan
        val_new = val if 0 < val < 100 else 99
        print(f"!PEAKS! pavan code -- peaks-{peaks}, peaks_avg {np.mean(peaks_avg)}, val{val}, val_new{val_new}, i{i}")
        print("Array = ", peaks_avg)
        peaks_avg = [val_new, peaks]
        i = 0

        # map 0-640 to 30-70


        sending_data(str(int(np.round(peaks))), connection)
    
   
    #return (rxx,peaks)


def calc_speech_rate(signal, fs=16_000, win=640):

    fs = 16000 #sampling rate 


    signal = signal/np.linalg.norm(signal)

    # win = 640 # Short time window length =40ms
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

    return rxx, peaks

def process_file(filename, fs=16_000):
    data, fs = librosa.load(filename, sr=fs)

    # sf.write('resampled_file.wav', samplerate=fs, format='PCM_24')
    return calc_speech_rate(data, fs)

def main_func():

    signal, Fs = sf.read("openday_test.wav")

    rxx, peaks = calc_speech_rate(signal, Fs)
    n = np.linspace(0,len(peaks)-1,len(peaks))

    fig, axs = plt.subplots(3,1,figsize=(8.27, 11.69))
    fig.suptitle("Results", fontsize=16)
    axs = axs.ravel()

    axs[0].plot(signal)
    axs[0].set_title('audio_signal')

    axs[1].imshow(rxx,cmap="gray")
    axs[1].set_title('ST_Autocorrelation')

    axs[2].step(n,peaks)
    axs[2].set_title('Peaks detected')

    fig.tight_layout()
    fig.subplots_adjust(top=0.88)
    plt.show()

if __name__=="__main__":
    main_func()