# -*- coding: utf-8 -*-
import outmod2
import random

MAX_PLAY_NUM = 10

if __name__ == "__main__":

    # 基本設定
    player1 = outmod2.AudioPlayer()
    player1.setAudioFile( "./data/loop_117.wav" )
    player1.setAudioWaitTime( 0 )
    player1.setAudioLoopTimes( 20 )
    #play_time = player1.getAudioPlayTime()
    
    # Listとして設定
    input_label = 1 # 入力音声のラベルが1とする
    same_label_list = outmod2.loadFile2List( "./data/L" + str(input_label) + "-List.txt" ) # 改行区切りのリストファイルをList型へ変換
    player_pack = []
    for i in range(0, MAX_PLAY_NUM): # 
        player_pack.append( outmod2.AudioPlayer() ) # 新たなAudioPlayerをListに追加
        out_wav_num = random.choice( same_label_list )
        #out_wav_num = same_label_list[i-1]
        player_pack[i-1].setAudioFile( "./data/" + str(out_wav_num) + ".wav" )
        player_pack[i-1].setAudioWaitTime( random.randint(0, 10) )
        #player_pack[i-1].setAudioLoopTimes( random.randint(0, 3) )

    # 基本再生
    outmod2.playLoop( player1 )

    # List再生
    for player_i in player_pack:
        outmod2.playLoop( player_i )

