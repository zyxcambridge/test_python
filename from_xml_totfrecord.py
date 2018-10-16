#coding=utf-8
import cv2
import os, xml.dom.minidom, sys

from lxml import etree
import PIL.Image
import tensorflow as tf

import hashlib
import io
import logging
import os
import random
import re


path="/media/root/dataset/deepblue_small_blue/201809061424"
model="point"

f_name="05242_000000_1.png"
label_before="dls001"
label_after="dls002"

className_list='''
ops-m104=红牛~红罐
ops-m102=小茗同学~青柠红茶
ops-m103=海之言~柠檬味
ops-m135=统一~阿萨姆
ops-m136=统一~绿茶
ops-m137=茶π 蜜桃味
ops-m138=雪花~纯生8度
ops-m129=安慕希~希腊风味酸奶原味
ops-m140=生和堂~龟苓膏
ops-m141=蒙牛~纯甄风味酸奶
ops-m083=百岁山~矿泉水
ops-m063=怡宝~纯净水
ops-m144=椰树牌~椰汁
ops-m145=统一~冰红茶
ops-m131=加多宝~
ops-m147=家家红~橘片爽
ops-m148=百事可乐`
ops-m149=伊利~麦香早餐奶
ops-m150=蒙牛~核桃奶
ops-m151=蒙牛~红枣早餐奶
ops-m152=欢乐家~椰子汁
ops-m153=康伯爵~苏打水
ops-m154=天蕴泉~苏打水1800
ops-m155=陶然楼~卤味坊
ops-m156=益达~泡泡薄荷味
'''


if sys.version_info.major == 2:
	path = path.decode("utf-8").encode("gbk")


def saveToXml(name, objs,cls,w, h):
    with open(name, "w") as xml:
        xml.write("<annotation><size><width>%d</width><height>%d</height></size>" % (w, h))

        for obj in objs:
            fmt = """
            <object>
                <name>%s</name>
                <bndbox>
                    <xmin>%d</xmin>
                    <ymin>%d</ymin>
                    <xmax>%d</xmax>
                    <ymax>%d</ymax>
                </bndbox>
            </object>
            """
            if obj[0] == "cube":
            	# class_biaozhu = obj[1]
            	# xmin = obj[2][0]
            	# ymin = obj[2][1]
            	# xmax = obj[3][0]
            	# ymax = obj[3][1]
                d = obj[2]
                e = obj[3]
                pmin = (min(d[0], e[0]), min(d[1], e[1]))
                pmax = (max(d[0], e[0]), max(d[1], e[1]))

                cls_str = "obj"
				# cls = "obj"
                xml.write(fmt % (cls_str, pmin[0], pmin[1], pmax[0], pmax[1]))

        xml.write("</annotation>")


def hsv2rgb(h, s, v):
	h_i = int(h * 6)
	f = h * 6 - h_i
	p = v * (1 - s)
	q = v * (1 - f * s)
	t = v * (1 - (1 - f) * s)
	r = 0
	g = 0
	b = 0
	if h_i == 0:
		r=v
		g=t
		b=p
	elif h_i == 1:
		r=q
		g=v
		b=p
	elif h_i == 2:
		r=p
		g=v
		b=t
	elif h_i == 3:
		r=p
		g=q
		b=v
	elif h_i == 4:
		r=t
		g=p
		b=v
	elif h_i == 5:
		r=v
		g=p
		b=q
	else:
		r=1
		g=1
		b=1
	return (int(r*255), int(g*255), int(b*255))

g_colors = []
def getColor(n, num=0):
	global g_colors, check_label
	
	if len(g_colors) == 0:
		for i in range(100):
			h = i / float(num)
			g_colors.append(hsv2rgb(h, 1, 1))
	return g_colors[n % len(g_colors)]



def saveBreakPoint():
	with open("breakpoint.txt", 'w') as f:
		f.write(str(currentImg))
	f.close()
	
def loadBreakPoint():
	if os.path.exists("breakpoint.txt"):
		with open("breakpoint.txt", 'r') as f:
			a = f.read()
		f.close()
		return a
	else:
		return 0


def loadTxt(number):	
	global point, obj, objs
	name = os.path.splitext(imgs[currentImg])[0] + '.txt'

	print(name)

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
				for j in range( (int)((len(o) - 2) / 3) ):

					for k in range(3):
						if k == 2:      
							point.append((o[j * 3 + k + 2]) == "True" )
							
						else:
							point.append((int)(o[j * 3 + k + 2]) )
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
		# print(objs)
		return objs
	else:
		return []


if __name__ == "__main__":

	num = int(sys.argv[2]) if len(sys.argv) > 2 else 3
	path = path + "/" if not path.endswith("/") else path

	className = []
	className_hz = []
	basic = 0

	listarr = className_list.split("\n")
	for i in range(len(listarr)):
		if listarr[i].find("=") != -1:
			tarr = listarr[i].split("=")
			className.append(tarr[0])
			className_hz.append(tarr[1])

	stop = False
	imgs = os.listdir(path)

	imgs = [path + imgs[i] for i in range(len(imgs))]

	for i in range(len(imgs)-1, -1, -1):
		if not imgs[i].lower().endswith("jpg") and not imgs[i].lower().endswith("png") and not imgs[i].lower().endswith("jpeg"):
			del imgs[i]

	colors = []
	getColor(0, len(className))

	for i in range(len(className)):
		colors.append(getColor(i))

	obj = []
	objs = []
	point = []
	currentImg = 0
	currentPoint = 0
	currentClass = 0
	hidden = False

	currentImg = int(loadBreakPoint())

	if path + f_name in imgs:
		currentImg = imgs.index(path + f_name)

	currentImg = 0 if currentImg < 0 else (len(imgs)-1 if currentImg >= len(imgs) else currentImg)
	# 图片变换,但是需要重新去取图片文件


	print(len(imgs))
	num = 0;

	writer = tf.python_io.TFRecordWriter("train.record")

	for x in range(0, len(imgs)):
		currentImg = x
		print("image -- index : ",currentImg)
		img_path = os.path.splitext(imgs[currentImg])[0] + ".jpg"

		with tf.gfile.GFile(img_path, 'rb') as fid:
			encoded_jpg = fid.read()
		encoded_jpg_io = io.BytesIO(encoded_jpg)
		image = PIL.Image.open(encoded_jpg_io)
		if image.format != 'JPEG':
			raise ValueError('Image format not JPEG')
		key = hashlib.sha256(encoded_jpg).hexdigest()

		width = 800
		height = 600
		xmin = []
		ymin = []
		xmax = []
		ymax = []
		classes = []
		classes_text = []
		truncated = []
		poses = []
		difficult_obj = []

		objs.clear()
		objs = loadTxt(currentImg)
		print("objs->size :",len(objs))
		for obj in objs:
			difficult_obj.append(int(0))
			if obj[0] == "cube":
				d = obj[2]
				e = obj[3]
				pmin = (min(d[0], e[0]), min(d[1], e[1]))
				pmax = (max(d[0], e[0]), max(d[1], e[1]))

				xmin.append(float(pmin[0]) / width)
				ymin.append(float(pmin[1]) / height)
				xmax.append(float(pmax[0]) / width)
				ymax.append(float(pmax[1]) / height)

				class_name = obj[1]
				classes_text.append(class_name.encode('utf8'))

				# classes.append(label_map_dict[class_name])
				truncated.append(int(0))
				poses.append('Unspecified'.encode('utf8'))

		print("start---to tfrecord example:")
		example = tf.train.Example(features=tf.train.Features(feature={
			'image/height': dataset_util.int64_feature(height),
			'image/width': dataset_util.int64_feature(width),
			'image/filename': dataset_util.bytes_feature(
				data['filename'].encode('utf8')),
			'image/source_id': dataset_util.bytes_feature(
				data['filename'].encode('utf8')),
			'image/key/sha256': dataset_util.bytes_feature(key.encode('utf8')),
			'image/encoded': dataset_util.bytes_feature(encoded_jpg),
			'image/format': dataset_util.bytes_feature('jpeg'.encode('utf8')),
			'image/object/bbox/xmin': dataset_util.float_list_feature(xmin),
			'image/object/bbox/xmax': dataset_util.float_list_feature(xmax),
			'image/object/bbox/ymin': dataset_util.float_list_feature(ymin),
			'image/object/bbox/ymax': dataset_util.float_list_feature(ymax),
			'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
			'image/object/class/label': dataset_util.int64_list_feature(classes),
			'image/object/difficult': dataset_util.int64_list_feature(difficult_obj),
			'image/object/truncated': dataset_util.int64_list_feature(truncated),
			'image/object/view': dataset_util.bytes_list_feature(poses),
		}))


	#
	# tf_example = dict_to_tf_example(data, label_map_dict, image_dir)
	#
	# writer.write(tf_example.SerializeToString())
	#
	#
	# writer.close()


	print("end transform number : ",num)
