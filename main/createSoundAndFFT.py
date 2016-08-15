#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 目的: データが何もない状態から、データを生成する。

import sys
sys.path.append('..')
sys.path.insert(0, 'input')
sys.path.insert(0, 'clustering')
sys.path.insert(0, 'output')

import input.writingWavAndPng as input
import clustering.processing as ps
import clustering.templateMatching as tm
import output.test_out as output

if __name__ == '__main__':
    wavname = input.recordingAndWriting()
    fs, data = ps.openFile(wavname)
    dirname = ps.getDirNameFromSoundFile(wavname)
    ps.writefft(data,dirname)
    # im = tm.ImageMatching()
    # fftname = dirname+'/fft.pkl'
    # classfilename = im.run(fftname)
    # classfilename = '../clustering/' + classfilename
    # output.output(classfilename)
