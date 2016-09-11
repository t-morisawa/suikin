# _*_ coding: utf-8 _*_
from __future__ import print_function

import numpy as np
import chainer
from chainer import cuda
import chainer.functions as F
from chainer import optimizers
from chainer import serializers
from random import randint
import cv2

from model import LeNet



point = 1
predict_num = 1
model = LeNet(predict_num)
img_size = 32
"""
if model_name == 'AlexNet':
    from cnn import AlexNet
    model = AlexNet(predict_num)
    img_size = 227
"""

gpu = -1
if gpu >= 0:
    cuda.get_device(args.gpu).use()
    model.to_gpu()
xp = np if gpu < 0 else cuda.cupy
optimizer = optimizers.Adam()
optimizer.setup(model)

"""
def img_load(dname, size=227):
    img = cv2.imread(dname, 0)
    img = cv2.resize(img, (size, size))
    img = np.array(img, dtype=np.float32)
    img = np.reshape(img, (1, 1, size, size))
    print(img.shape)
    return img
"""

def predict(x):
    x = chainer.Variable(xp.asarray(x, dtype=xp.float32))
    return model(x)

def train(x, t, training=True):
    y_predict = predict(x)
    t = chainer.Variable(xp.asarray(t, dtype=xp.float32))
    if training is True:
        # return F.softmax_cross_entropy(y_predict, t)
        return F.mean_squared_error(y_predict, t)
    else:
        # return F.accuracy(y_predict, t)
        return t - F.sigmoid(y_predict)

def CNN_predict(data):
    size = 32
    data = cv2.resize(data, (size, size))
    data = np.reshape(data, (1, 1, size, size))
    return predict(data).data

if __name__ == "__main__" :

    import argparse
    import sys
    import os
    import re
    sys.path.append('../')
    from util import data_search


    parser = argparse.ArgumentParser(description='Predict Waveform')
    parser.add_argument('--initmodel', '-m', default='',
                        help='Initialize the model from given file')
    parser.add_argument('--resume', '-r', default='',
                        help='Resume the optimization from snapshot')
    parser.add_argument('--save', '-s', type=bool, default='False',
                        help='Save model and resume or not')
    parser.add_argument('--gpu', '-g', default=-1, type=int,
                        help='GPU ID (negative value indicates CPU)')
    parser.add_argument('--epoch', '-e', default=100, type=int,
                        help='number of epochs to learn')
    parser.add_argument('--batchsize', '-b', type=int, default=20,
                        help='learning minibatch size')
    parser.add_argument('--modelname', default='LeNet',
                        help='model form')
    parser.add_argument('--dataname', default="namamugi")
    parser.add_argument('--modeldir', default=None)
    args = parser.parse_args()
    if args.modeldir is None: args.modeldir = "models_cnn/{}".format(args.dataname)
    if not os.path.exists(args.modeldir): os.makedirs(args.modeldir)

    epoch_num = args.epoch
    batch_num = args.batchsize
    model_name = args.modelname
    print('GPU: {}'.format(args.gpu))
    print('# epoch: {}'.format(epoch_num))
    print('# Minibatch-size: {}'.format(batch_num))
    print('# unit: {}'.format(model_name))
    print('')



    """
    データの形考える
    dirlist, sample_num = data_search("./data")
    print(dirlist, sample_num)
    all_img = np.empty((0,1,img_size,img_size), dtype=np.float32)
    #a = 0 # debug
    for dname in dirlist:
        _dname = dname + "/img.png"
        img = img_load(_dname, img_size)
        #img.fill(a) # debug
        #a += 1 # debug
        all_img = np.append(all_img, img, axis=0)
    """

    input_data = None
    output_data = None
    save_file = np.empty(0,dtype=np.float32)
    for epoch in range(1, epoch_num):
        loss_sum = 0
        optimizer.zero_grads()
        loss = train(training_input_data, training_output_data)
        loss.backward()
        optimizer.update()
        sum_loss = chainer.cuda.to_cpu(loss.data)
        print('epoch: {}, total loss: {}'.format(epoch,sum_loss))
        if epoch%10 == 0:
            save_file = np.append(save_file, loss_sum)
            print('save the model')
            serializers.save_npz('{}/{}_model_{}.npz'.format(args.modeldir, cross_num, epoch), model)
            print('save the optimizer')
            serializers.save_npz('{}/{}_optimizer_{}.npz'.format(args.modeldir, cross_num, epoch), optimizer)

