# -*- coding: utf-8 -*-

import numpy as np
import cv2
import cPickle as pickle
import random

import glob

'''
imageMatchingのインスタンス.run(imagepath)で
最も類似度の高い画像のパス
'''

# 画像をリサイズする割合
RESIZE_PER = 0.3

class ImageMatching:
    def getClassPathList(self):
        data_dir='../clustering/'
        fileList = []
        for num in range(len(glob.glob(data_dir + '*.pkl'))):
            fileList.append(str(num)+'.pkl')
        return fileList

    def getImagePath(self, class_label_path):
        class_label_path='../clustering/' + class_label_path
        f = open( class_label_path , 'r' )
        same_label_list = pickle.load( f )
        f.close()
        select_wav_num = random.choice( same_label_list )
        return "../clustering/hayakuti_data/" + "{0:03d}".format(int(select_wav_num)) + "/img.png"

    # ダウンサイズする関数
    def resize(self, img):
        hight = img.shape[0]
        width = img.shape[1]
        return cv2.resize(img,(int(width*RESIZE_PER),
                              int(hight*RESIZE_PER)))

    # グレー画像の取得
    def read(self, imgSrc):
        #img = cv2.imread(imgSrc,0) #0はグレーで読み込ませる引数
        #img = self.resize(img)
        f = open(imgSrc, 'r')
        img = pickle.load( f )
        f.close()
        return img

    # グレー画像の取得
    def readList(self, imgSrcList):
        imgList = []
        for imgSrc in imgSrcList:
            img = self.read(imgSrc)
            imgList.append(img)
        return imgList

    # 類似度の取得
    def getSimilarity(self, img, tmp):
        '''
        imgとtmpの画像サイズが一致している場合は
        1x1の二次元配列が返される
        '''
        img = np.array(img, dtype=np.uint8)
        tmp = np.array(tmp, dtype=np.uint8)
        res = cv2.matchTemplate(img,tmp,cv2.TM_SQDIFF)
        #res = cv2.matchTemplate(img,tmp,cv2.TM_CCOEFF_NORMED)
        return res[0][0]

    # def run(self, imgSrc, tmpSrc):
    #     img = self.read(imgSrc)
    #     tmp = self.read(tmpSrc)
    #     return self.getSimilarity(img, tmp)

    #imgListの中からimgと最も類似の高いものを返す
    def getArgMaxSimilarity(self, imgSrc, imgSrcList):
        img = self.read(imgSrc)
        imgList = self.readList(imgSrcList)
        simList = []
        for tmp in imgList:
            simList.append(self.getSimilarity(img, tmp))
        #argmax = np.argmax(simList)
        argmax = np.argmin(simList) #SQDIFFなのでargminを取る
        #return imgSrcList[argmax]
        return str(argmax) + '.pkl'

    def run(self, nowImg):
        cPathList = self.getClassPathList()
        imgPathList = []
        for cPath in cPathList:
            imgPath = self.getImagePath(cPath)
            imgPathList.append(imgPath)
        return self.getArgMaxSimilarity(nowImg, imgPathList)
    
if __name__ == '__main__':
    im = ImageMatching()
    print im.read('./hayakuti_data/001/img.png')
    #print im.run('./hayakuti_data/002/img.png')
    
    #res = im.run("hayakuchi_data/0/sample/img.png", "hayakuchi_data/1/sample/img.png")
    #print res
