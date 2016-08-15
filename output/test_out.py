# -*- coding: utf-8 -*-
import outmod
import random
import cPickle as pickle
#import cv2

MAX_PLAY_NUM = 10
TIME_INTVL = 0.30

def output( class_label_path ):
    #print "{0:04d}".format(1)
    """player1 = outmod2.AudioPlayer()
    player1.setAudioFile( "./data/loop_117.wav" )
    player1.setAudioWaitTime( 0 )
    player1.setAudioLoopTimes( 1 )
    #play_time = player1.getAudioPlayTime()
    """

    seq_list = []
    for i in range( MAX_PLAY_NUM ):
        seq_list.append( TIME_INTVL * i )
        #for ii in range( 0, i ):
        #    seq_list.append( TIME_INTVL*(i-1) )
    
    # ラベルリストから
    f = open( class_label_path , 'r' ) #read
    same_label_list = pickle.load( f ) #np
    f.close()
    
    # Listとして設定
    player_pack = []
    for i in range(MAX_PLAY_NUM): # 
        player_pack.append( outmod.AudioPlayer() ) # 新たなAudioPlayerをListに追加
        out_wav_num = random.choice( same_label_list )
        #out_wav_num = random.randint( 1, 16 )
        player_pack[i].setAudioFile( "../clustering/hayakuti_data/" + "{0:03d}".format(int(out_wav_num)) + "/sound.wav" )
        player_pack[i].setAudioWaitTime( seq_list[i]  )
        player_pack[i].setAudioLoopTimes( 0 )
        player_pack[i].setDampRatio( 3*float(MAX_PLAY_NUM - i)/MAX_PLAY_NUM  )

    # 基本再生
    # outmod2.playLoop( player1 )

    # List再生
    for player_i in player_pack:
        outmod.playLoop( player_i )


if __name__ == "__main__":

    #input_label = 0 # 入力音声のラベルが1とする    
    input_label = random.randint( 0,9 ) # 入力音声のラベルが1とする    
    
    output( "../clustering/"+ str(input_label) +".pkl" )
