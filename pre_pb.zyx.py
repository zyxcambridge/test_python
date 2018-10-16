import time
import tensorflow as tf
import numpy as np
import cv2
import config
import matplotlib.pyplot as plt
from scipy.misc import imresize, imsave, imread


def load_graph(model_file):
    graph = tf.Graph()
    graph_def = tf.GraphDef()

    with open(model_file, "rb") as f:
        graph_def.ParseFromString(f.read())
    with graph.as_default():
        tf.import_graph_def(graph_def)
    return graph


if __name__ == "__main__":
    # 载入配置
    config = config.load_config()
    INPUT_FILE = config['input']
    OUTPUT_FILE = config['output']
    image = imread(INPUT_FILE)
    IMG_H, IMG_W = image.shape[0], image.shape[1]
    small_img = imresize(image, (80, 160, 3))
    small_img = np.array(small_img)
    small_img = small_img[None, :, :, :]
    # 模型配置信息
    model_file = config['pb_model']
    input_layer = config['input_layer']
    output_layer = config['output_layer']

    # 载入模型
    graph = load_graph(model_file)
    input_name = "import/" + input_layer
    output_name = "import/" + output_layer
    input_operation = graph.get_operation_by_name(input_name)
    output_operation = graph.get_operation_by_name(output_name)

    # 创建tf计算图
    with tf.Session(graph=graph) as sess:

        start = time.time()
        # 模型预测
        results = sess.run(output_operation.outputs[0], {input_operation.outputs[0]: small_img})
        end = time.time()
        print('Image_size: ' + str(IMG_H) + '*' + str(IMG_W) + '\n')
        print('Evaluation time (1-image): {:.3f}s\n'.format(end - start))

        # 预测结果叠加于原图
        prediction = results[0] * 255
        blanks = np.zeros_like(prediction).astype(np.uint8)
        lane_drawn = np.dstack((blanks, prediction, blanks))
        lane_image = imresize(lane_drawn, (IMG_H, IMG_W, 3))
        result = cv2.addWeighted(image, 1, lane_image, 1, 0)

        # 保存结果
        imsave(OUTPUT_FILE, result)

        # 展示结果
        plt.imshow(result)
        plt.show()
        print('==========Done!===========')
