#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--source', '-s', default='hayakuti_data')
args = parser.parse_args()

source_dir = args.source

sys.path.append('..')

import output.test_out as output

if __name__ == '__main__':
    output.output(source_dir=source_dir)
