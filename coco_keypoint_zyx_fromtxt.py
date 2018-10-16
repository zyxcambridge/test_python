# @author: zhangboshen
# @Email: zhangbs@whu.edu.cn
#
# 提取COCO关键点并保存在CSV文件中 Date: 2018.3.22

from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import pylab
import os
from PIL import Image
from PIL import ImageDraw
import csv
import copy

import  json

import sys
sys.path.append('.')

from cube_point_comon import  *


print(path)
print(model)
# initialize COCO api for person keypoints annotations
dataDir='coco_json'
dataType='val2017'
annFile = '{}/person_keypoints_{}.json'.format(dataDir,dataType)
coco_kps=COCO(annFile)

dataset = []
annotations = []
images = []
info = coco_kps.dataset['info']
licenses = coco_kps.dataset['licenses']
categories = coco_kps.dataset['categories']

#
# {
#     "coco_url":"http://images.cocodataset.org/val2017/000000000139.jpg",
#     "height":426,
#     "width":640,
#     "flickr_url":"http://farm9.staticflickr.com/8035/8024364858_9c41dc1666_z.jpg",
#     "file_name":"000000000139.jpg",
#     "date_captured":"2013-11-21 01:34:01",
#     "license":2,
#     "id":139
# }

image_json_demo = '/media/root/software/data_utils/coco_json/image_id_139.json'
with open(image_json_demo,'r') as f:
    image = json.load(f)

annotations_json_demo = '/media/root/software/data_utils/coco_json/anno_image_id_139_id_230831.json'
with open(annotations_json_demo,'r') as f:
    annotations_json = json.load(f)


for x in range(0, len(imgs)):
    currentImg = x

    print("--------------------------------")
    tmp = os.path.splitext(imgs[currentImg])[0].split('/')[-1]
    image_name = tmp + '.jpg'
    print("currentImg num: ", currentImg,image_name)
    id = int(tmp)
    if 259==id:
        print("here is :")



    image_item = copy.deepcopy(image)

    image_item["height"] = 600
    image_item["width"] = 800
    image_item["file_name"] = image_name
    image_item["id"] = id
    images.append(image_item)


    #
    # {
    #     "bbox": [
    #         412.8,
    #         157.61,
    #         53.05,
    #         138.01
    #     ],
    #     "area": 2913.1104,
    #     "num_keypoints": 15,
    #     "segmentation": "",
    #     "category_id": 1,
    #     "iscrowd": 0,
    #     "keypoints": Array[51],
    #     "image_id": 139,
    #     "id": 230831
    # }
    global point, obj, objs
    objs.clear()
    obj.clear()
    point.clear()
    # objs = loadTxt(currentImg)
    name = os.path.splitext(imgs[currentImg])[0] + '.txt'

    if os.path.exists(name):
        with open(name, 'r') as f:
            lines = f.readline()
            # shape 是图片宽高
            shape = f.readline()
            line = ''
            for i in range(int(lines)):
                line = f.readline().strip()
                o = line.split(',')
                obj.append(o[0])
                obj.append(o[1])
                for j in range((int)((len(o) - 2) / 3)):

                    for k in range(3):
                        if k == 2:
                            point.append((o[j * 3 + k + 2]) == "True")

                        else:
                            point.append((int)(o[j * 3 + k + 2]))
                        '''
                        if  k % 2 ==0:
                            print(o[j * 3 + k + 2])
                            point.append( o[j * 3 + k + 2] == 'True')
                        else:
                            print(o[j * 3 + k + 2])
                            point.append((int)(o[j * 3 + k + 2]))
                        '''
                    obj.append(point)
                    point = []

                objs.append(obj)
                obj = []
        print(objs)


    print("objs->size :", len(objs))
    numobj = 0;
    for obj in objs:
        if obj[0] == 'point':
            numobj = numobj + 1
            annotations_json_item = copy.deepcopy(annotations_json)
            annotations_json_item['num_keypoints'] = 3
            annotations_json_item['image_id'] = id
            annotations_json_item['iscrowd'] = 0
            annotations_json_item['id'] = currentImg*1000 + numobj
            first_point = obj[2]
            secon_point = obj[3]
            three_point = obj[4]
            # "keypoints": [x1, y1, v1, ...],
            # 第一和第二个元素分别是x和y坐标值，第三个元素是个标志位v，v为0时表示这个关键点没有标注（这种情况下x = y = v = 0），
            # v为1时表示这个关键点标注了但是不可见（被遮挡了），v为2时表示这个关键点标注了同时也可见。
            if first_point[2] == False:
                first_point[2] = 1
            else:
                first_point[2] = 2
            if secon_point[2] == False:
                secon_point[2] = 1
            else:
                secon_point[2] = 2

            if three_point[2] == False:
                three_point[2] = 1
            else:
                three_point[2] = 2

            annotations_json_item["keypoints"][0]=first_point[0]
            annotations_json_item["keypoints"][1]=first_point[1]
            annotations_json_item["keypoints"][2]=first_point[2]
            annotations_json_item["keypoints"][3]=secon_point[0]
            annotations_json_item["keypoints"][4]=secon_point[1]
            annotations_json_item["keypoints"][5]=secon_point[2]
            annotations_json_item["keypoints"][6]=three_point[0]
            annotations_json_item["keypoints"][7]=three_point[1]
            annotations_json_item["keypoints"][8]=three_point[2]
            annotations.append(annotations_json_item)



deepblue_images_name = '/media/root/software/data_utils/coco_json/deepblue_images_name.json'
with open(deepblue_images_name,'w') as f:
    json.dump(images,f)
    print("end -deepblue_images_name--- ")

origin_images_name = '/media/root/software/data_utils/coco_json/origin_images_name.json'
with open(origin_images_name, 'w') as f:
    json.dump(coco_kps.dataset['images'], f)
    print("end -origin_images_name--- ")

deepblue_annotations_name = '/media/root/software/data_utils/coco_json/deepblue_annotations_name.json'
with open(deepblue_annotations_name,'w') as f:
    json.dump(annotations,f)
    print("end -deepblue_annotations_name--- ")

origin_annotations_name = '/media/root/software/data_utils/coco_json/origin_annotations_name.json'
with open(origin_annotations_name,'w') as f:
    json.dump(coco_kps.dataset['annotations'],f)
    print("end -origin_annotations_name--- ")

coco_kps.dataset["images"] = images
coco_kps.dataset["annotations"] = annotations


deepblue_output_json = "/media/root/software/data_utils/coco_json/" + "deepblue_output_json"+'.json'
with open(deepblue_output_json ,'w') as f:
    json.dump(coco_kps.dataset,f)
    print("end -deepblue_output_json--- ")


# for image in coco_kps.dataset['images']:
#     print(image)
#     image_json_name = "/media/root/software/data_utils/coco_json/image/image_id_" + str(image['id'])+'.json'
#     with open(image_json_name, 'w') as f:
#         json.dump(image, f)
#         print("end:-image_json_name-")
#
#
# for annotations in coco_kps.dataset['annotations']:
#     print(annotations)
#     annotations_json_name = "/media/root/software/data_utils/coco_json/anno_json/anno_image_id_" + str(annotations['image_id'])+'_id_'+ str(annotations['id'])+'.json'
#     with open(annotations_json_name, 'w') as f:
#         json.dump(annotations, f)
#         print("end:-annotations_json_name-")

# annotations_json_name = "/media/root/software/data_utils/coco_json/anno_json/" + "annotations_json.json"
# with open(annotations_json_name,'w') as f:
#     json.dump(coco_kps.dataset['annotations'],f)
#     print("end:-annotations_json_name-")



# categories_json_name = "/media/root/software/data_utils/coco_json/" + "categories_json_name.json"
# with open(annotations_json_name,'w') as f:
#     json.dump(coco_kps.dataset['categories'],f)
#     print("end:-categories_json_name-")
#
#
# info_json_name = "/media/root/software/data_utils/coco_json/" + "info_json_name.json"
# with open(info_json_name,'w') as f:
#     json.dump(coco_kps.dataset['info'],f)
#     print("end:-info_json_name-")
#
#
# license_json_name = "/media/root/software/data_utils/coco_json/" + "license_json_name.json"
# with open(license_json_name,'w') as f:
#     json.dump(coco_kps.dataset['licenses'],f)
#     print("end:-license_json_name-")



if __name__ == "__main__":
    print ('Writing bndbox and keypoints to csv files..."')
