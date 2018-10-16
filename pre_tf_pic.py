#coding=utf-8
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os

def distort_color(image, color_ordering=0):
    '''
    随机调整图片的色彩，定义两种处理顺序。
    注意，对3通道图像正常，4通道图像会出错，自行先reshape之
    :param image: 
    :param color_ordering: 
    :return: 
    '''
    if color_ordering == 0:
        image = tf.image.random_brightness(image, max_delta=32./255.)
        image = tf.image.random_saturation(image, lower=0.5, upper=1.5)
        image = tf.image.random_hue(image, max_delta=0.2)
        image = tf.image.random_contrast(image, lower=0.5, upper=1.5)
    else:
        image = tf.image.random_saturation(image, lower=0.5, upper=1.5)
        image = tf.image.random_brightness(image, max_delta=32./255.)
        image = tf.image.random_contrast(image, lower=0.5, upper=1.5)
        image = tf.image.random_hue(image, max_delta=0.2)

    return tf.clip_by_value(image, 0.0, 1.0)


def preprocess_for_train(image, height, width, bbox):
    '''
    对图片进行预处理，将图片转化成神经网络的输入层数据。
    :param image: 
    :param height: 
    :param width: 
    :param bbox: 
    :return: 
    '''
    # 默认整个图像是需要关注的部分
    if bbox is None:
        bbox = tf.constant(
            [0.0, 0.0, 1.0, 1.0], dtype=tf.float32, shape=[1, 1, 4])

    # 查看是否存在标注框。
    if image.dtype != tf.float32:
        image = tf.image.convert_image_dtype(image, dtype=tf.float32)

    # 随机的截取图片中一个块。
    # bbox_begin, bbox_size, _ = tf.image.sample_distorted_bounding_box(
    #     tf.shape(image), bounding_boxes=bbox, min_object_covered=0.1)

    # distorted_image = tf.slice(image, bbox_begin, bbox_size)

    # 将随机截取的图像调整为输入层的大小
    distorted_image = tf.image.resize_images(
        image, size=[height, width], method=np.random.randint(4))

    # 随机左右翻转图像
    distorted_image = tf.image.random_flip_left_right(distorted_image)

    # 使用一种随机顺序调整图像色彩
    distorted_image = distort_color(distorted_image, np.random.randint(2))
    return distorted_image


def pre_main(img,bbox=None):
    # des_location=img.split()
    if bbox is None:
        bbox = tf.constant([0.0, 0.0, 1.0, 1.0], dtype=tf.float32, shape=[1, 1, 4])
    with tf.gfile.FastGFile(img, "rb") as f:
        image_raw_data = f.read()
    with tf.Session() as sess:
        img_data = tf.image.decode_jpeg(image_raw_data)
        for i in range(9):
            result = preprocess_for_train(img_data, 299, 299, bbox)
            # {wb打开文件{矩阵编码为jpeg{格式转换为uint8}}.eval()}
            with tf.gfile.FastGFile('{}_{}.jpeg'.format(img,i),'wb') as f:
                f.write(sess.run(tf.image.encode_jpeg(tf.image.convert_image_dtype(result,dtype=tf.uint8))))

def add_image_tolist(image_path,imglist):
    #把每一个图片加到list中
    filelist=os.listdir(image_path)#该文件夹下所有的文件（包括文件夹）
    for files in filelist:#遍历所有文件
        org_image=os.path.join(image_path,files);#原来的文件路径                
        imglist.append(org_image)
    return imglist

def get_image_all(image_path):
    imglist=[]    
    #遍历文件夹,收集所有文件的名字
    for f in os.listdir(image_path):
        if os.path.isfile(image_path + os.path.sep + f):
            add_image_tolist(image_path,imglist)
        elif os.path.isdir(image_path + os.path.sep + f):
            print(image_path + os.sep + f)
            add_image_tolist(image_path + os.path.sep + f,imglist)
    return imglist


if __name__=='__main__':
    image_path = '/home/zyx/Desktop/20180115_classification_7tag/normal'
    for image in get_image_all(image_path):
        print(image)
        pre_main(image,bbox=None)
    # else:
        print("")
    # pre_main("/home/zyx/Desktop/code/Custom-Object-Detection-master/images/1514186847552.jpg",bbox=None)
    exit()
