# -*- coding: utf-8 -*-
# 参考）http://qiita.com/serinuntius/items/ce8183a283795d9fdb01
import pyaudio
import wave
import time
import threading
import numpy as np
from pylab import *
import struct

import ConfigParser
inifile = ConfigParser.SafeConfigParser()
inifile.read("../conf/config.ini")
varfile = ConfigParser.SafeConfigParser()
varfile.read("../conf/var.ini")

CHUNK = 1024
FADEOUT = varfile.getfloat("output", "fade_out")

class AudioPlayer:
    """ A Class For Playing WAV Audio """

    def __init__(self):

        self.audio_file = "" # 空の名前でイニシャライズ
        self.paused = threading.Event() # 止める用のフラグ
        self.loop_times = 0
        self.loop_count = 0
        self.wait_time = 0
        self.play_time = 0
        self.damp_ratio = 2

    def setAudioFile( self, audio_file ):
        self.audio_file = audio_file
        ##K1
        if (self.audio_file == ""):
            return
        self.wf = wave.open(self.audio_file, "rb")
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                             channels=self.wf.getnchannels(),
                             rate=self.wf.getframerate(),
                             output=True)

    def setAudioWaitTime( self, wait_time ):
        self.wait_time = wait_time

    def setAudioLoopTimes( self, loop_times ):
        self.loop_times = loop_times
    ########
    def getAudioPlayTime( self ):
        return float(self.wf.getnframes()) / self.wf.getframerate()

    def setAudioBPM( self , bpm ):
        self.bpm = bpm

    def setDampRatio( self, damp_ratio ):
        self.damp_ratio = damp_ratio
        
    def playLoopAudio( self ):
        ## K1
        if (self.audio_file == ""):
            return
        #再生方法１
        time.sleep( self.wait_time )       
        t = time.time()
        data = self.wf.readframes(CHUNK)
        # While毎にCHUNKの分だけ出力，出力が返らなくなればBreak
        ii = 1
        while len(data) > 0:
            data = np.frombuffer(data, dtype="int16") /  32768.0
            data = [int(x*32768.0)*self.damp_ratio/ii for x in data ]##################################
            data = struct.pack("h" * len(data), *data)
            self.stream.write(data)
            data = self.wf.readframes(CHUNK)
            ii += FADEOUT
        #print time.time() - t 

        """#再生方法２
        time.sleep( self.wait_time )
        t = time.time()
        data = self.wf.readframes(self.wf.getnframes())
        data = frombuffer(data, dtype="int16") /  32768.0
        data = [int(x*32768.0)*0.3 for x in data ]#
        data = struct.pack("h" * len(data), *data)
        print time.time() - t 
        sp = 0  # 再生位置ポインタ
        buffer = data[sp:sp+CHUNK]
        while buffer != '':
            self.stream.write(buffer)
            sp = sp + CHUNK
            buffer = data[sp:sp+CHUNK]
            """
            
        # 後処理
        self.stream.stop_stream()
        self.stream.close()
        # close PyAudio (5)
        self.p.terminate()

        # Loop再生
        if self.loop_count < self.loop_times:
            #self.audio_thread = threading.Timer( self.wait_time, self.playLoopAudio )
            self.audio_thread = threading.Timer( 0, self.playLoopAudio )
            self.audio_thread.start()
            self.loop_count += 1

def playLoop( player ):
    #time.sleep( player.dely_time )
    # 再生は別のスレッドでする
    audio_thread = threading.Thread( target = player.playLoopAudio )
    #time = player.getAudioPlayTime( player )
    audio_thread.start()

#改行区切りのファイルをintのListにして返す
def loadFile2List( file_path ):
    file_list = []
    for line in open( file_path ):
        tmplist = line[:-1].split("\n")
        file_list += [int(tmplist[0])]
    return file_list

def data_search(data_dir="./data"):
    dirlist = []
    sample_num = []
    for dirName, subdirList, fileList in os.walk(data_dir):
        for dname in subdirList:
            if dname.isdigit() is True:
                dirlist.append(dirName+"/"+dname)
                sample_num.append(int(dname))
    return dirlist, sample_num




    
