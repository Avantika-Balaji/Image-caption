#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Sample code to generate caption using beam search
'''
import sys
import json
import os
# comment out the below if you want to do type check. Remeber this have to be done BEFORE import chainer
# os.environ["CHAINER_TYPE_CHECK"] = "0"
import chainer 

import argparse
import numpy as np
import math
from chainer import cuda
import chainer.functions as F
from chainer import cuda, Function, FunctionSet, gradient_check, Variable, optimizers
from chainer import serializers
import matplotlib 
from matplotlib import pyplot as plt
import matplotlib.image as mpimg

sys.path.append('./code')
from CaptionGenerator import CaptionGenerator

#Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-g", "--gpu",default=-1, type=int, help=u"GPU ID.CPU is -1")
parser.add_argument('--vocab',default='./data/MSCOCO/mscoco_caption_train2014_processed_dic.json', type=str,help='path to the vocaburary json')
parser.add_argument('--img',default='./sample_imgs', type=str,help='path to the image')
parser.add_argument('--cnn-model', type=str, default='./data/ResNet50.model',help='place of the ResNet model')
parser.add_argument('--rnn-model', type=str, default='./data/caption_model.model',help='place of the caption model')
parser.add_argument('--beam',default=3, type=int,help='beam size in beam search')
parser.add_argument('--depth',default=50, type=int,help='depth limit in beam search')
parser.add_argument('--lang',default="<sos>", type=str,help='special word to indicate the langauge or just <sos>')
args = parser.parse_args()

caption_generator=CaptionGenerator(
    rnn_model_place=args.rnn_model,
    cnn_model_place=args.cnn_model,
    dictonary_place=args.vocab,
    beamsize=args.beam,
    depth_limit=args.depth,
    gpu_id=args.gpu,
    first_word= args.lang,
    )

f = open("captions.txt", "w")

captions_list=""
for image_path in os.listdir(args.img):
	input_path = os.path.join(args.img, image_path)
	captions = caption_generator.generate(input_path)
	# img = mpimg.imread(input_path)
	# myimg=plt.imshow(img)
	# plt.show()

	#print(input_path)
	
	#print(captions)
	for caption in captions:
		temp1=(" ".join(caption["sentence"]))
		temp2=(caption["log_likelihood"])
	print(temp1)
	#print(temp1[6:-6])
	captions_list+=temp1[6:-6]+'\n'
f.write(captions_list)
f.close()

