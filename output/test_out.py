# -*- coding: utf-8 -*-
import outmod
import random
import cPickle as pickle
import cv2

MAX_PLAY_NUM = 4


def output( class_label_path ):
    #print "{0:04d}".format(1)

    """player1 = outmod2.AudioPlayer()
    player1.setAudioFile( "./data/loop_117.wav" )
    player1.setAudioWaitTime( 0 )
    player1.setAudioLoopTimes( 1 )
    #play_time = player1.getAudioPlayTime()
    """
    # 
    seq_list = []
    x =2.0
    p = 0
    i = 0
    for i in range( 0, 10 ):
        seq_list.append( 2*(i-1)+2 )
        for ii in range( 0, i ):
            p = p + x/(i) 
            #seq_list.append( 3*(i-1)+1 )
    print seq_list
    #seq_list

    
    f = open( class_label_path , 'r' ) #read
    same_label_list = pickle.load( f ) #np
    f.close()
    #same_label_list = outmod2.loadFile2List( "./data/L" + str(input_label) + "-List.txt" ) # 改行区切りのリストファイルをList型へ変換
    
    # Listとして設定
    player_pack = []
    for i in range(MAX_PLAY_NUM): # 
        player_pack.append( outmod.AudioPlayer() ) # 新たなAudioPlayerをListに追加
        out_wav_num = random.choice( same_label_list )
        #out_wav_num = same_label_list[i-1]
        player_pack[i].setAudioFile( "../clustering/hayakuti_data/" + "{0:03d}".format(int(out_wav_num)) + "/sound.wav" )
        player_pack[i].setAudioWaitTime( random.uniform( seq_list[i] , seq_list[i] ) )
        player_pack[i].setAudioLoopTimes( random.randint( 0, 0 ) )

    # 基本再生
    # outmod2.playLoop( player1 )

    # List再生
    for player_i in player_pack:
        outmod.playLoop( player_i )


if __name__ == "__main__":

    input_label = 4 # 入力音声のラベルが1とする    
    
    output( "../clustering/"+ str(input_label) +".pkl" )
