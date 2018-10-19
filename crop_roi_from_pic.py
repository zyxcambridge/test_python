#coding=utf-8
'''
crop roi
from pic

'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys
import time
import os
import numpy as np
import random
import string

import cv2
import copy

import cv2
import  os

img = np.zeros((500, 500, 3), np.uint8)

def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print("11111")

        # crop_roi = frame[x-50:y-50, x+50:y+50]

        x1 = x - 64
        x2 = x + 64
        y1 = y - 64
        y2 = y + 64

        if x1 < 1 or x2 < 1 or y1 < 1 or y2 < 1 or x1 > 800 or x2 >800 or y1>600 or y2>600:
            print(" 请选择合适区域")
            return
        print("roi postion : min ({0} ,{1})".format(x1,y1))
        print("roi postion : max ({0} ,{1})".format(x2, y2))
        tmp_frame = copy.deepcopy(frame)
        crop_roi = frame[y1:y2,x1:x2]

        time_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        item_path = file_save_path + time_str +'.jpg'
        print("save roi : name ")
        print(item_path)
        cv2.imshow("crop_roi", crop_roi)
        cv2.imwrite(item_path, crop_roi)


# 创建图像与窗口并将窗口与回调函数绑定
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_circle)

global frame

filepath = '/media/root/dataset/deepblue_small_blue/JPEGImages/'
file_save_path = "/media/root/dataset/deepblue_small_blue/blank/"

for root, dirs, filelist in os.walk(filepath):
    for item in filelist:
        if item.endswith(".jpg"):
            print(item)
            print(os.path.join(root, item))

            item_path = os.path.join(root, item)

            frame = cv2.imread(item_path)

            cv2.imshow("image",frame)

            k = cv2.waitKey(0)
            if k == ord('n'):
                print("next ")
            elif k == ord('q'):
                print("quit ")
                break
            else:
                print("wait ")
                cv2.waitKey(1)

            # exit(0)
            print("next 2 ")

            # frame = cv2.resize(frame, (512, 512))
            # cv2.imwrite(item_path,frame)

