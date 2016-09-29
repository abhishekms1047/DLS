#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ar'

import os
import glob
import json

import skimage.io as io
import matplotlib.pyplot as plt

from pprint import pprint

import keras
from keras.utils.visualize_util import plot as kplot

from app.backend.core.models.convertors.caffe import convert as caffeConvert
from app.backend.core.models.convertors.caffe.extra_layers import dictExtraLayers

pathWithDatasets='../../../data-test/test_caffe_models'

if __name__ == '__main__':
    lstModelsPaths=[{
        'proto':    os.path.abspath(os.path.join(pathWithDatasets, '%s.prototxt'   % os.path.basename(os.path.splitext(xx)[0]) )),
        'weights':  os.path.abspath(os.path.join(pathWithDatasets, '%s.caffemodel' % os.path.basename(os.path.splitext(xx)[0]) ))
    } for xx in glob.glob('%s/bvlc_*.prototxt' % pathWithDatasets)]
    pprint(lstModelsPaths)
    for ii,pp in enumerate(lstModelsPaths):
        pathProto   = pp['proto']
        pathWeights = pp['weights']
        # (1) convert Caffe->Keras
        model = caffeConvert.caffe_to_keras(pathProto, caffemodelPath=None, debug=False)
        pathKerasModelOutput='%s-kerasmodel.json' % os.path.splitext(pathProto)[0]
        with open(pathKerasModelOutput, 'w') as f:
            f.write(model.to_json(indent=4))
        print ('[%d/%d] %s --> %s' % (ii, len(lstModelsPaths), pathProto, pathKerasModelOutput))
        # (2) try to load and plot Keras model
        with open(pathKerasModelOutput, 'r') as f:
            jsonData = f.read()
        kerasModel = keras.models.model_from_json(jsonData, custom_objects=dictExtraLayers)
        pathKerasModelImage = '%s-kerasmodel.jpg' % os.path.splitext(pathProto)[0]
        kplot(kerasModel, to_file=pathKerasModelImage, show_shapes=True)
        img = io.imread(pathKerasModelImage)
        plt.imshow(img)
        plt.show()
