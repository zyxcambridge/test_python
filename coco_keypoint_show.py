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
pylab.rcParams['figure.figsize'] = (8.0, 10.0)



annFile = '/media/root/software/data_utils/coco_json/deepblue_output_json.json'
coco = COCO(annFile)
#
cats = coco.loadCats(coco.getCatIds())
nms = [cat['name'] for cat in cats]
print('COCO categories: \n{}\n'.format(' '.join(nms)))
#
nms = set([cat['supercategory'] for cat in cats])
print('COCO supercategories: \n{}'.format(' '.join(nms)))

# get all images containing given categories, select one at random
catIds = coco.getCatIds(catNms=['person']);
imgIds = coco.getImgIds(catIds=catIds );
imgIds = coco.getImgIds(imgIds = [259])
img = coco.loadImgs(imgIds[np.random.randint(0,len(imgIds))])[0]

# load and display image
dataDir = '/media/root/software/data_utils/point_coco'
I = io.imread('%s/%s'%(dataDir,img['file_name']))

coco_kps=COCO(annFile)

plt.imshow(I);

print(img['id'])
annIds = coco_kps.getAnnIds(imgIds=img['id'], catIds=catIds, iscrowd=None)
anns = coco_kps.loadAnns(annIds)
coco_kps.showAnns(anns)

plt.show()