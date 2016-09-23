#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import numpy as np
import sys, os
from datetime import datetime

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

import scipy.fftpack
from pylab import *

sys.path.append(os.pardir)
import output.outmod as outmod

import ConfigParser
inifile = ConfigParser.SafeConfigParser()
inifile.read("../conf/config.ini")

# /sound.wavを削除して返す
def getDirNameFromSoundFile(filename):
    return filename[0:len(filename)-10]

def openFile(filename):
    fs, data = read(filename)
    return fs, data

def data2fft(data):
    data = np.frombuffer(data, dtype= "int16") / 32768.0
    hammingWindow = np.hamming(data.shape[0])
    data = data * hammingWindow
    X = np.fft.fft(data)  # FFT
    
    return [np.sqrt(c.real ** 2 + c.imag ** 2) for c in X]  # 振幅スペクトル 

# pathはディレクトリパス
def writefft(data, path):
    # FFT解析
    fft_data = data2fft(data)
    # FFT結果を保存
    fft_filepath = path + '/fft.pkl'
    file_fft = open(fft_filepath, 'w')
    pickle.dump(fft_data[0:1000], file_fft)
    file_fft.close()

# pathはディレクトリパス
def writeImage(fs, data, path):
    # 画像生成
    # fs, data = read(WAVE_OUTPUT_FILENAME)
    cq_spec, freqs = cq_fft(data, fs)
    w, h = cq_spec.shape
    fig = pl.figure()
    fig.add_subplot(111)
    pl.imshow(abs(cq_spec).T, aspect = "auto", origin = "lower")
    pl.tick_params(labelbottom='off')
    pl.tick_params(labelleft='off')
    filepath = path + '/img.png'
    pl.savefig(filepath, bbox_inches='tight')
    
    # dumpを保存
    raw_filepath = path + '/data.pkl'
    f = open(raw_filepath, 'w')
    pickle.dump(cq_spec, f)
    f.close()

if __name__ == "__main__":
    path = '../clustering/'+inifile.get("config","sound_dir")+'/001'
    sound = path + '/sound.wav'
    # fsはサンプリング周波数
    fs, data = openFile(sound)
    writefft(data, path)
    writeImage(fs, data, path)
