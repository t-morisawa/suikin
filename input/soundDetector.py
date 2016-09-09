#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 音が閾値超えたら録音するクラス
# 参考サイト
# http://stackoverflow.com/questions/892199/detect-record-audio-in-python

from sys import byteorder
from array import array
from struct import pack
from datetime import datetime

import pyaudio
import wave

THRESHOLD = 1000 #音量の閾値
PERIOD = 40 #持続時間
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100
FTIME = 0.05 #前の時間（多分s）

#録音開始時刻
STARTTIME = -1

#チャンク音圧の最大値が閾値を下回っているか
def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    count = 0

    #print max(snd_data)
    return max(snd_data) < THRESHOLD

def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r

## 終了フラグが立ってからの音を切る
def trim(snd_data):
    "Trim the blank spots at the start and end"
    def _trim(snd_data):
        snd_started = False
        r = array('h')
        count = 0

        for i in snd_data:
            if not snd_started and i>THRESHOLD:
                snd_started = True
                r.append(i)
            elif snd_started:
                r.append(i)
        return r
    def __trim(snd_data):
        snd_started = False
        r = array('h')
        count = 0

        for i in snd_data:
            if not snd_started and i>THRESHOLD/3:
                snd_started = True
                r.append(i)
            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    snd_data = _trim(snd_data)

    # Trim to the right
    # snd_data.reverse()
    # snd_data = __trim(snd_data)
    # snd_data.reverse()
    return snd_data

def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    r = array('h', [0 for i in xrange(int(seconds*RATE))])
    r.extend(snd_data)
    r.extend([0 for i in xrange(int(seconds*RATE))])
    return r

def record():
    """
    Record a word or words from the microphone and 
    return the data as an array of signed shorts.

    Normalizes the audio, trims silence from the 
    start and end, and pads with 0.5 seconds of 
    blank sound to make sure VLC et al can play 
    it without getting chopped off.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=RATE,
        input=True, output=True,
        frames_per_buffer=CHUNK_SIZE)

    num_silent = 0
    snd_started = False

    r = array('h')

    while 1:
        # little endian, signed short
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)

        silent = is_silent(snd_data)

        if silent and snd_started:
            num_silent += 1
        elif not silent and not snd_started:
            snd_started = True
            global STARTTIME
            STARTTIME = datetime.now()

        if snd_started and num_silent > PERIOD:
            break

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = trim(r)
    r = normalize(r)
    r = add_silence(r, FTIME)
    return sample_width, r

def record_wrap():
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    data = pack('<' + ('h'*len(data)), *data)
    
    print 'finish recording'
    return data, STARTTIME

    # wf = wave.open(path, 'wb')
    # wf.setnchannels(1)
    # wf.setsampwidth(sample_width)
    # wf.setframerate(RATE)
    # wf.writeframes(data)
    # wf.close()

def write(path):
    sample_width, data = record()
    data = pack('<' + ('h'*len(data)), *data)
    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()
    
if __name__ == '__main__':
    print("please speak a word into the microphone")
    #record_wrap()
    write('demo.wav')
    print("done - result written to demo.wav")
