# -*- coding: utf-8 -*-
# 参考）http://qiita.com/serinuntius/items/ce8183a283795d9fdb01
import pyaudio
import wave
import time
import threading

CHUNK = 1024

class AudioPlayer:
    """ A Class For Playing WAV Audio """

    def __init__(self):

        self.audio_file = "" # 空の名前でイニシャライズ

        self.paused = threading.Event() # 止める用のフラグ

        self.loop_times = 0

        self.loop_count = 0

        self.wait_time = 0

        self.play_time = 0

    def setAudioFile( self, audio_file ):
        self.audio_file = audio_file

    def setAudioWaitTime( self, wait_time ):
        self.wait_time = wait_time

    def setAudioLoopTimes( self, loop_times ):
        self.loop_times = loop_times
    ########
    def getAudioPlayTime( self ):
        return float(self.wf.getnframes()) / self.wf.getframerate()

    def setAudioBPM( self , bpm ):
        self.bpm = bpm

    def playLoopAudio( self ):
        if (self.audio_file == ""):
            return
        self.wf = wave.open(self.audio_file, "rb")
        p = pyaudio.PyAudio()

        self.stream = p.open(format=p.get_format_from_width(self.wf.getsampwidth()),
                             channels=self.wf.getnchannels(),
                             rate=self.wf.getframerate(),
                             output=True)

        data = self.wf.readframes(CHUNK)

        self.play_time = float(self.wf.getnframes()) / self.wf.getframerate()
        print self.play_time
        #####
        time.sleep( self.wait_time )

        # play stream (3)
        while len(data) > 0:
            # もし、止めるフラグが立ってたら
            if self.paused.is_set():
                # 再生を止める
                self.stream.stop_stream()
                # フラグを初期状態に
                self.paused.clear()
                break
            self.stream.write(data)
            data = self.wf.readframes(CHUNK)

        # stop stream (4)
        self.stream.stop_stream()
        self.stream.close()
        # close PyAudio (5)
        p.terminate()
        
        # Loop再生
        if self.loop_count < self.loop_times:
            self.audio_thread = threading.Timer( self.wait_time, self.playLoopAudio )
            self.audio_thread.start()
            self.loop_count += 1

def playLoop( player ):
    #time.sleep( player.dely_time )
    # 再生は別のスレッドでする
    audio_thread = threading.Thread( target = player.playLoopAudio )
    audio_thread.start()

#def playSerial( player ):

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
