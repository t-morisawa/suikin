# -*- coding: utf-8 -*-
import outmod
import random
import cPickle as pickle
import numpy.random as rd
import os
#import cv2

import ConfigParser
inifile = ConfigParser.SafeConfigParser()
inifile.read("../conf/config.ini")
varfile = ConfigParser.SafeConfigParser()
varfile.read("../conf/var.ini")

MAX_PLAY_NUM = varfile.getint("output","max_play_num")
TIME_INTVL = varfile.getfloat("output","time_intvl")

DATA_DIR="../clustering/"+inifile.get("config","sound_dir")
SOUND_FILE=inifile.get("config","sound_file")

def setTiming():
    seq_list = []
    for i in range( MAX_PLAY_NUM ):
        timing = TIME_INTVL * i
        #timing = TIME_INTVL * i / rd.beta(a=4, b=1)
        #timing = TIME_INTVL * i + rd.randn() * 0.4
        timing = timing if timing >= 0 else 0
        seq_list.append( timing )
        #for ii in range( 0, i ):
        #    seq_list.append( TIME_INTVL*(i-1) )
    return seq_list

def setAudioFile( player_pack ):
    dir_list = []
    path = DATA_DIR
    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path,item)):
            dir_list.append(item)

    for i in range(MAX_PLAY_NUM): # 
        out_wav_num = random.choice(dir_list)
        print out_wav_num
        player_pack[i].setAudioFile( DATA_DIR + "/" + out_wav_num + "/" + SOUND_FILE )
    return 


def setAudioFileFromClassLabelPath( class_label_path, player_pack ):
    # ラベルリストから
    f = open( class_label_path , 'r' ) #read
    same_label_list = pickle.load( f ) #np
    f.close()

    for i in range(MAX_PLAY_NUM): # 
        out_wav_num = random.choice( same_label_list )
        player_pack[i].setAudioFile( "../clustering/"+inifile.get("config","sound_dir")+"/" + "{0:03d}".format(int(out_wav_num)) + "/sound.wav" )
    return 

def output( class_label_path = None, source_dir='hayakuti_data' ):
    #print "{0:04d}".format(1)
    """player1 = outmod2.AudioPlayer()
    player1.setAudioFile( "./data/loop_117.wav" )
    player1.setAudioWaitTime( 0 )
    player1.setAudioLoopTimes( 1 )
    #play_time = player1.getAudioPlayTime()
    """
    global DATA_DIR
    DATA_DIR="../clustering/"+source_dir# +inifile.get("config","sound_dir")
    seq_list = setTiming()
    
    # Listとして設定
    player_pack = []
    for i in range(MAX_PLAY_NUM): # 
        player_pack.append( outmod.AudioPlayer() ) # 新たなAudioPlayerをListに追加
        # out_wav_num = random.choice( same_label_list )
        # player_pack[i].setAudioFile( "../clustering/"+inifile.get("config","sound_dir")+"/" + "{0:03d}".format(int(out_wav_num)) + "/sound.wav" )
        player_pack[i].setAudioWaitTime( seq_list[i]  )
        player_pack[i].setAudioLoopTimes( 0 )
        player_pack[i].setDampRatio( 1 )
        #player_pack[i].setDampRatio( 3*float(MAX_PLAY_NUM - i)/MAX_PLAY_NUM  )

    if class_label_path is None:
        setAudioFile( player_pack )
    
    if class_label_path is not None:
        setAudioFileFromClassLabelPath( class_label_path, player_pack )

    # 基本再生
    # outmod2.playLoop( player1 )

    # List再生
    for player_i in player_pack:
        outmod.playLoop( player_i )

if __name__ == "__main__":

    #input_label = 0 # 入力音声のラベルが1とする    
    input_label = random.randint( 0,9 ) # 入力音声のラベルが1とする    
    
    output( "../clustering/"+ str(input_label) +".pkl" )
