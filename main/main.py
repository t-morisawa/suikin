#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append('..')

import input.writingWavAndPng as input
import clustering.processing as ps
import clustering.templateMatching as tm
import output.test_out as output

if __name__ == '__main__':
    for i in range(1) : 
        wavname, starttime = input.recordingAndWriting()
        fs, data = ps.openFile(wavname)
        dirname = ps.getDirNameFromSoundFile(wavname)
        ps.writefft(data,dirname)
        im = tm.ImageMatching()
        fftname = dirname+'/fft.pkl'
        classfilename = im.run(fftname)
        classfilename = '../clustering/' + classfilename
        output.output(classfilename)
