import argparse
import numpy as np
import os

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

ROOT = "data"
if not os.path.exists(ROOT):
    os.mkdir(ROOT)
PATH = os.path.join(ROOT, args.savename)
if not os.path.exists(PATH):
    os.mkdir(PATH)

WAVE_OUTPUT_FILENAME = PATH + "/sound.wav"
IMAGE_OUTPUT_FILENAME = PATH + "/img.png"
RAW_OUTPUT_FILENAME = PATH + "/data.pkl"

if __name__ == "__main__":
    stream=p.open(format = pyaudio.paInt16,
                  channels = CHANNELS,
                  rate = RATE,
                  frames_per_buffer = CHUNK,
                  input = True)
    
    frames = []
    print "start"
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        input = stream.read(CHUNK)
        frames.append(input)
    
    print "stop"
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    print WAVE_OUTPUT_FILENAME
    data = b''.join(frames)
    wf = wave.open(WAVE_OUTPUT_FILENAME, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()
    
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

    
