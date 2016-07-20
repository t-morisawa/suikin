#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import atexit
import time

import numpy as np
import pyaudio
import threading

class Spectrum(threading.Thread):

    FORMAT = pyaudio.paFloat32
    CHANNELS = 1
    RATE = 16000

    def __init__(self):
        super(Spectrum, self).__init__()
        self.pa = pyaudio.PyAudio()
        self.last_samples = None
        self.pr = []
        atexit.register(self.pa.terminate)

    def fft(self, samples):
        win = np.hanning(len(samples))
        res = np.fft.fftshift(np.fft.fft(win*samples))
        freq = np.fft.fftfreq(len(samples), d=self.RATE**-1)
        return zip(freq, 20*np.log10(np.abs(res)))

    def callback(self, in_data, frame_count, time_info, status):
        data = np.fromstring(in_data, np.float32)
        for f,v in self.fft(data)[256-64:256]:
            self.pr.append(str(min(9, max(0, int((v+50)/10)))))
        # print ''.join(pr)
        return (in_data, self.recording)

    def run(self):
        self.recording = pyaudio.paContinue
        stream = self.pa.open(format = self.FORMAT,
                        channels = self.CHANNELS, 
                        rate = self.RATE, 
                        input = True,
                        output = False,
                        #frames_per_buffer = self.FRAME_LEN,
                        frames_per_buffer = 512,
                        stream_callback = self.callback)
        stream.start_stream()

        while stream.is_active():
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                self.recording = pyaudio.paAbort

        stream.start_stream()
        stream.close()

if __name__ == '__main__':
    spe = Spectrum()
    spe.start()

    for i in range(5):
        time.sleep(5)
        print len(spe.pr)
