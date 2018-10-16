#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import shutil

class BatchRename():
    '''
    批量重命名文件夹下的图片文件
    '''
    def __init__(self):
        self.path = "/media/root/dataset/fashion_tmp/"
    def rename(self):
        # filelist = os.listdir(self.path)
        # print("filelist = ", filelist)
        # print("=====", os.path.abspath(self.path))
        total_num = 0
        i = 200
        for root, dirs, filelist in os.walk(self.path):
            for item in filelist:
                if item.endswith(".jpg"):
                    print(item)
                    print(os.path.join(root, item))
                    src = os.path.join(root, item)
                    file_before = item.split('.')[0]

                    file_name_1 = "%012d" % i + '.jpg'
                    des_dir = '/media/root/dataset/all_cloth'

                    dst = os.path.join(os.path.abspath(des_dir) ,file_name_1)
                    total_num = total_num + 1
                    # os.rename(src, dst)
                    shutil.copy(src, dst)

        print('total %d to rename & converted %d jpgs' % (total_num, i))

if __name__ == '__main__':
    demo = BatchRename()
    demo.rename()
