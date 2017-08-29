#!/usr/bin/env python2

import numpy as np
import os
import sys
import glob
import time
import re
sys.path.insert(0, "/home/hiromi/Downloads/caffe-rc4/python")
import caffe
import json
from skimage import io; io.use_plugin('matplotlib')


    
def classify(input_file, gpu=False):
    model_def = "/home/hiromi/Downloads/caffe-rc4/models/fr_6/deploy6.prototxt"
    pretrained_model = "/media/Kyou/FYP_DATA/snapshots/fr_style/fr_6_iter_100000.caffemodel"
    pycaffe_dir = "/home/hiromi/Downloads/caffe-rc4/python"
    image_dims = [256,256]
    mean = np.load(os.path.join(pycaffe_dir,'caffe/imagenet/ilsvrc_2012_mean.npy'))
    channel_swap = [2,1,0]
    raw_scale = 255.0
    input_scale = None
    center_only = False
    if gpu:
        caffe.set_mode_gpu()
            #print("GPU mode")
    else:
        caffe.set_mode_cpu()
            #print("CPU mode")
    classifier = caffe.Classifier(model_def, pretrained_model,
        image_dims=image_dims, mean=mean,
        input_scale=input_scale, raw_scale=raw_scale,
        channel_swap=channel_swap)
    target_class = None

    #load image
    input_file = os.path.expanduser(input_file)
    inputs = [caffe.io.load_image(input_file)]

    #load labels
    labels_file = "/media/Kyou/FYP_DATA/flickr_dl/data/synset_words.txt"
    labels = np.loadtxt(labels_file, str, delimiter='\t')

    # Classify.
    start = time.time()
    predictions = classifier.predict(inputs, not center_only)
    #print("Done in %.2f s." % (time.time() - start))

    #clasify output
    #print ('prediction shape:', predictions[0].shape)
    #print ('predicted class:', predictions[0].argmax())
    output = dict(zip(labels, predictions[0]))
    print(output)
    #print(json.dumps(output))

def main(args):
    classify(args[1])

if __name__ == '__main__':
    main(sys.argv)