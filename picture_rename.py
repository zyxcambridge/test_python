#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

class BatchRename():
    '''
    批量重命名文件夹下的图片文件
    '''
    def __init__(self):
        self.path = "/media/root/software/data_utils/point_coco/"
    def rename(self):
        filelist = os.listdir(self.path)
        print("filelist = ", filelist)
        print("=====", os.path.abspath(self.path))
        total_num = len(filelist)
        i = 200
        for item in filelist:  # 循环文件夹所有图片文件
            if item.endswith(".jpg"):
                src = os.path.join(os.path.abspath(self.path), item)
                file_before = item.split('.')[0]
                srctxt = os.path.join(os.path.abspath(self.path), file_before)+'.txt'
                # 0000 0000 0139.jpg

                file_name_1 = "%012d" % i + '.jpg'
                file_name_txt = '%012d' % i + '.txt'
                dst = os.path.join(os.path.abspath(self.path) ,file_name_1)
                dsttxt = os.path.join(os.path.abspath(self.path) ,file_name_txt)
                try:
                    os.rename(src, dst)
                    os.rename(srctxt, dsttxt)
                    print("converting %s to %s     " % (src, dst))
                    i = i+1
                except:
                    continue
        print('total %d to rename & converted %d jpgs' % (total_num, i))

if __name__ == '__main__':
    demo = BatchRename()
    demo.rename()
