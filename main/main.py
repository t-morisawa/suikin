#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
sys.path.insert(0, 'input')
sys.path.insert(0, 'clustering')
sys.path.insert(0, 'output')

import input.writingWavAndPng as input
import clustering.templateMatching as tm
import output.test_out as output

if __name__ == '__main__':
    fname = input.recordingAndWriting()
    im = tm.ImageMatching()
    classfilename = im.run(fname)
    classfilename = '../clustering/' + classfilename
    output.output(classfilename)
