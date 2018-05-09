from taeksoo.cnn_util import *
import pandas as pd
import numpy as np
import os
import scipy
import ipdb
import json
import cPickle
from sklearn.feature_extraction.text import CountVectorizer

# JUST REFERENCE CODE< DOES NOT DO ANYTHING
annotation_path = '/home/taeksoo/Study/show_attend_and_tell/data/flickr30k/results_20130124.token'
vgg_deploy_path = '/home/taeksoo/Package/caffe/models/vgg/VGG_ILSVRC_16_layers_deploy.prototxt'
vgg_model_path  = '/home/taeksoo/Package/caffe/models/vgg/VGG_ILSVRC_16_layers.caffemodel'
#flickr_image_path = '/home/taeksoo/Study/Multimodal/dataset/flickr30/flickr30k-images'
flickr_image_path = './images/flickr30k/'
feat_path='/home/taeksoo/Study/Multimodal/Show_Attend_Tell/feat/flickr30k'
#cnn = CNN(deploy=vgg_deploy_path,
#          model=vgg_model_path,
#          batch_size=20,
#          width=224,
#          height=224)

annotations = pd.read_table(annotation_path, sep='\t', header=None, names=['image', 'caption'])
annotations['image_num'] = annotations['image'].map(lambda x: x.split('#')[1])
annotations['image'] = annotations['image'].map(lambda x: os.path.join(flickr_image_path,x.split('#')[0]))

captions = annotations['caption'].values

vectorizer = CountVectorizer(max_features=10000).fit(captions)
dictionary = vectorizer.vocabulary_
dictionary_series = pd.Series(dictionary.values(), index=dictionary.keys()) + 2
dictionary = dictionary_series.to_dict()

with open('/home/taeksoo/Study/show_attend_and_tell/data/flickr30k/dictionary.pkl', 'wb') as f:
    cPickle.dump(dictionary, f)
with open('/home/taeksoo/Study/show_attend_and_tell/data/flickr30k/vectorizer.pkl', 'wb') as f:
    cPickle.dump(vectorizer, f)
