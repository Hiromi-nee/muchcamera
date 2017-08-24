#!/usr/bin/env python2

import numpy as np
import os
import sys
import glob
import time
import re
import caffe
from skimage import io; io.use_plugin('matplotlib')

class CNN:
    
    def classify(input_file, gpu=False):
        model_def = "~/Downloads/caffe-rc4/models/fr_8/deploy8.prototxt"
        pretrained_model = "/media/Kyou/FYP_DATA/snapshots/fr_style/fr_8_aug_iter_100000.caffemodel"
        pycaffe_dir = os.path.dirname(__file__)
        image_dims = [256,256]
        mean = os.path.join(pycaffe_dir,'caffe/imagenet/ilsvrc_2012_mean.npy')
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
        print("Loading file: %s" % input_file)
        inputs = [caffe.io.load_image(input_file)]

        #load labels
        labels_file = "/media/Kyou/FYP_DATA/flickr_dl/data/synset_words.txt"
        labels = np.loadtxt(labels_file, str, delimiter='\t')

        # Classify.
        start = time.time()
        predictions = classifier.predict(inputs, not center_only)
        print("Done in %.2f s." % (time.time() - start))

        #clasify output
        print ('prediction shape:', predictions[0].shape)
        print ('predicted class:', predictions[0].argmax())
        output = zip(labels, predictions[0])
        print(output)