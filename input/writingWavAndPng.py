#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import numpy as np
import sys, os

from scipy import arange, ceil, complex128, dot, exp, float64, hamming, log2, zeros
from scipy import pi as mpi
from scipy.fftpack import fft
from scipy.sparse import lil_matrix, csr_matrix
from scipy.io.wavfile import read

from matplotlib import pylab as pl
from constant_q_trans import *

import pyaudio
import wave

import cPickle as pickle

import soundDetector

import scipy.fftpack
from pylab import *


sys.path.append(os.pardir)
import output.outmod as outmod

parser = argparse.ArgumentParser(description='Predict Waveform')
parser.add_argument('--savename', '-s', default='sample',
                    help='file name to save')
parser.add_argument('--recordingtime', '-r', type=float, default=5,
                    help='Recording time')
args = parser.parse_args()


CHUNK=1024
RATE=44100
p=pyaudio.PyAudio()
RECORD_SECONDS = args.recordingtime
CHANNELS = 1

def data2fft(data):
    hammingWindow = np.hamming(data.shape[0])
    data = data * hammingWindow
    X = np.fft.fft(data)  # FFT                                                                    
    return [np.sqrt(c.real ** 2 + c.imag ** 2) for c in X]  # 振幅スペクトル 

def get_dir_name(data_dir="../clustering/hayakuti_data/"):
    count = 0
    for dirName, subdirList, fileList in os.walk(data_dir):
        for dname in subdirList:
            if dname.isdigit() is True:
                count+=1
    count+=1
    return data_dir + "{0:03d}".format(count)

#ROOT = "../data"
ROOT = get_dir_name()
if not os.path.exists(ROOT):
    os.mkdir(ROOT)
PATH = ROOT    
# PATH = os.path.join(ROOT, args.savename)
# if not os.path.exists(PATH):
#     os.mkdir(PATH)

WAVE_OUTPUT_FILENAME = PATH + "/sound.wav"
IMAGE_OUTPUT_FILENAME = PATH + "/img.png"
RAW_OUTPUT_FILENAME = PATH + "/data.pkl"

def recordingAndWriting():
    # stream=p.open(format = pyaudio.paInt16,
    #               channels = CHANNELS,
    #               rate = RATE,
    #               frames_per_buffer = CHUNK,
    #               input = True)
    
    # frames = []
    # print "start"
    # for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    #     input = stream.read(CHUNK)
    #     frames.append(input)
    
    # print "stop"
    # stream.stop_stream()
    # stream.close()
    # p.terminate()

    #wav書込
    data = soundDetector.record_wrap()


    #print WAVE_OUTPUT_FILENAME
    #data = b''.join(frames)
    wf = wave.open(WAVE_OUTPUT_FILENAME, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()
    start = 0
    data = frombuffer(data, dtype= "int16") / 32768.0
    amplitudeSpectrum = data2fft(data)
    N = data.shape[0]
    freqList = np.fft.fftfreq(N, d=1.0/44100)
    subplot(311)  # 3行1列のグラフの1番目の位置にプロット
    plot(range(start, start+N), data[start:start+N])
    axis([start, start+N, -1.0, 1.0])
    xlabel("time [sample]")
    ylabel("amplitude")
    fs = 44100
    # 振幅スペクトルを描画
    subplot(312)
    hogehoge = np.array(freqList)
    hagehage = np.array(amplitudeSpectrum)
    print hogehoge.shape, hagehage.shape
    plot(freqList, amplitudeSpectrum, marker= 'o', linestyle='-')
    axis([0, fs/2, 0, 50])
    xlabel("frequency [Hz]")
    ylabel("amplitude spectrum")
    show()

    #outputの関数を呼ぶ
    ap = outmod.AudioPlayer()
    ap.setAudioFile(WAVE_OUTPUT_FILENAME)
    outmod.playLoop(ap)
    
    #画像生成
    fs, data = read(WAVE_OUTPUT_FILENAME)
    cq_spec, freqs = cq_fft(data, fs)
    w, h = cq_spec.shape
    fig = pl.figure()
    fig.add_subplot(111)
    pl.imshow(abs(cq_spec).T, aspect = "auto", origin = "lower")
    pl.tick_params(labelbottom='off')
    pl.tick_params(labelleft='off')
    pl.savefig(IMAGE_OUTPUT_FILENAME, bbox_inches='tight')

    f = open(RAW_OUTPUT_FILENAME, 'w')
    pickle.dump(cq_spec, f)
    f.close()

    return IMAGE_OUTPUT_FILENAME

if __name__ == "__main__":
    recordingAndWriting()
