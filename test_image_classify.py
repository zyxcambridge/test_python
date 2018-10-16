#coding=utf-8
'''
origin_path = 
des_path =
des_fold
    normal
    cover
    nobody
    phone
    smoke
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys
import time
import os
import numpy as np
import tensorflow as tf
import shutil

# os.environ["TF_CPP_MIN_LOG_LEVEL"]='1' # 这是默认的显示等级，显示所有信息  
# os.environ["TF_CPP_MIN_LOG_LEVEL"]='2' # 只显示 warning 和 Error   
os.environ["TF_CPP_MIN_LOG_LEVEL"]='3' # 只显示 Error 

origin_path = "/home/zyx/Desktop/pictures2_1801181750"
des_path = "/home/zyx/Desktop/1701"



def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph

def read_tensor_from_image_file(file_name, input_height=299, input_width=299,
				input_mean=0, input_std=255):
  input_name = "file_reader"
  output_name = "normalized"
  file_reader = tf.read_file(file_name, input_name)
  if file_name.endswith(".png"):
    image_reader = tf.image.decode_png(file_reader, channels = 3,
                                       name='png_reader')
  elif file_name.endswith(".gif"):
    image_reader = tf.squeeze(tf.image.decode_gif(file_reader,
                                                  name='gif_reader'))
  elif file_name.endswith(".bmp"):
    image_reader = tf.image.decode_bmp(file_reader, name='bmp_reader')
  else:
    image_reader = tf.image.decode_jpeg(file_reader, channels = 3,
                                        name='jpeg_reader')
  float_caster = tf.cast(image_reader, tf.float32)
  dims_expander = tf.expand_dims(float_caster, 0);
  resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  sess = tf.Session()
  result = sess.run(normalized)

  return result

def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label

def copyfile_to_desdir(file_name,lable):
#   print('start copy file_name{file_name} {lable}to des dir'.format(file_name, lable))
#   print (" %s  %s"%(file_name,lable))
  des_dir = os.path.join(des_path,lable)
  if False == os.path.exists(des_dir):
     os.makedirs(des_dir)
  oldname_path = os.path.join(origin_path,file_name)
  newname_path = os.path.join(des_dir,file_name)
#   print ("oldname_path %s \nnewname_path %s"%(oldname_path,newname_path))
#   start = time.time()
  shutil.copyfile(oldname_path,newname_path)
#   end=time.time()
#   print('\copyfile copyfile (1-copyfile): {:.3f}s\n'.format(end-start))
  return 

def run_main(file_name):
    file_input = os.path.join(origin_path,file_name)
    model_file = "tf_files/retrained_graph_phone.pb"
    label_file = "tf_files/retrained_graph_phone.txt"
    input_height = 224
    input_width = 224
    input_mean = 128
    input_std = 128
    input_layer = "input"
    output_layer = "final_result"

    parser = argparse.ArgumentParser()
    parser.add_argument("--image", help="image to be processed")
    parser.add_argument("--graph", help="graph/model to be executed")
    parser.add_argument("--labels", help="name of file containing labels")
    parser.add_argument("--input_height", type=int, help="input height")
    parser.add_argument("--input_width", type=int, help="input width")
    parser.add_argument("--input_mean", type=int, help="input mean")
    parser.add_argument("--input_std", type=int, help="input std")
    parser.add_argument("--input_layer", help="name of input layer")
    parser.add_argument("--output_layer", help="name of output layer")
    args = parser.parse_args()

    if args.graph:
        model_file = args.graph
    if args.image:
        file_name = args.image
    if args.labels:
        label_file = args.labels
    if args.input_height:
        input_height = args.input_height
    if args.input_width:
        input_width = args.input_width
    if args.input_mean:
        input_mean = args.input_mean
    if args.input_std:
        input_std = args.input_std
    if args.input_layer:
        input_layer = args.input_layer
    if args.output_layer:
        output_layer = args.output_layer

    graph = load_graph(model_file)
    t = read_tensor_from_image_file(file_input,
                                    input_height=input_height,
                                    input_width=input_width,
                                    input_mean=input_mean,
                                    input_std=input_std)

    input_name = "import/" + input_layer
    output_name = "import/" + output_layer
    input_operation = graph.get_operation_by_name(input_name);
    output_operation = graph.get_operation_by_name(output_name);

    with tf.Session(graph=graph) as sess:
        start = time.time()
        results = sess.run(output_operation.outputs[0],
                        {input_operation.outputs[0]: t})
        end=time.time()
    results = np.squeeze(results)

    top_k = results.argsort()[-5:][::-1]
    labels = load_labels(label_file)

    # print('\nEvaluation time (1-image): {:.3f}s\n'.format(end-start))

    # for i in top_k:
        # print(labels[i], results[i])
    # copy to first
    copyfile_to_desdir(file_name,labels[top_k[0]])

if __name__ == "__main__":

    filelist=os.listdir(origin_path)#该文件夹下所有的文件（包括文件夹）
    for file_name in filelist:#遍历所有文件
        start = time.time()
        Olddir=os.path.join(origin_path,file_name);#原来的文件路径                               
        if os.path.isdir(Olddir):#如果是文件夹则跳过
            continue;
        run_main(file_name)
        end=time.time()
        # print('\copyfile copyfile (1-copyfile): {:.3f}s\n'.format(end-start))
