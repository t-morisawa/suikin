# coding: utf-8
import os
import shutil
import numpy as np
from sklearn.cluster import KMeans
import cv2

def data_search(data_dir="./data"):
    dirlist = []
    sample_num = []
    for dirName, subdirList, fileList in os.walk(data_dir):
        for dname in subdirList:
            if dname.isdigit() is True:
                dirlist.append(dirName+"/"+dname)
                sample_num.append(int(dname))
    return dirlist, sample_num


def img_load(dname, size=227):
    img = cv2.imread(dname, 0)
    img = cv2.resize(img, (size, size))
    # cv2.imshow("result", img)
    # cv2.waitKey(0)
    #img = np.array(img, dtype=np.float32)
    #img = np.reshape(img, (1, 1, size, size))
    #print(img.shape)
    return img

img_size = 32
dirlist, sample_num = data_search("./data")
print(dirlist, sample_num)
all_img = np.empty((0,img_size,img_size), dtype=np.float32)
for dname in dirlist:
    _dname = dname + "/img.png"
    img = img_load(_dname, img_size)
    print img.shape
    #img.fill(a) # debug
    #a += 1 # debug
    all_img = np.append(all_img, [img], axis=0)

all_img_2d = np.reshape(all_img, (all_img.shape[0], all_img.shape[1]*all_img.shape[2]))
print all_img.shape

index = np.array([i for i in range(all_img.shape[0])])

# K-means クラスタリングをおこなう
# この例では 3 つのグループに分割 (メルセンヌツイスターの乱数の種を 10 とする)
kmeans_model = KMeans(n_clusters=10, random_state=10).fit(all_img_2d)

# 分類先となったラベルを取得する
labels = kmeans_model.labels_


# ラベル (班) 、成績、三科目の合計得点を表示する
ii = 0
for label, feature, origin, dname in zip(labels, all_img_2d, all_img, dirlist):
    ii += 1
    print(label, feature.shape, feature.sum(), origin.sum())
    if not os.path.exists("cluster/"+str(label)):
        os.mkdir("cluster/"+str(label))
    shutil.copytree(dname, "cluster/"+str(label)+"/"+str(origin.sum()))
    cv2.imwrite("cluster/{}/{}.png".format(label, origin.sum()), origin)

