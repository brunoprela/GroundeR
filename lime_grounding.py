import os
import keras
from keras.applications import inception_v3 as inc_net
from keras.applications import resnet50 as res50
from keras.applications import inception_resnet_v2 as incep_res_net
from keras.applications import vgg16 as vgg16
from keras.preprocessing import image
from keras.applications.imagenet_utils import decode_predictions
from skimage.io import imread
from skimage.segmentation import mark_boundaries
import lime
from lime import lime_image
# from dataprovider_supervise import dataprovider
# from model_supervise import ground_model

#to read pkl file
import pickle

import matplotlib.pyplot as plt
#matplotlib inline
import numpy as np

print('Notebook run using keras:', keras.__version__)

from PIL import Image as pil_image
_PIL_INTERPOLATION_METHODS = {
      'nearest': pil_image.NEAREST,
      'bilinear': pil_image.BILINEAR,
      'bicubic': pil_image.BICUBIC,
  }
# model order: VGG, resnet, inception, inception_res

# img_name = '134206'
# print img_name
total_num = 1000
num_sample = 10
num_exp = 1


#todo: set in config


def transform_img_fn_gen(path_list, box, size):
    out = []
    for img_path in path_list:
        temp = Image.open(img_path)
        cropped = temp.crop(box);
        resample = _PIL_INTERPOLATION_METHODS['nearest']
        img = cropped.resize((size, size), resample)
        #img = image.load_img(img_path, target_size=(299, 299))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = inc_net.preprocess_input(x)
        out.append(x)
    return np.vstack(out)

def load_box():
	 f = open('./flickr30k_test.lst')
	 box_map = {};
	 file_list = []
	 for line in f:
	 	 img_name = line.rstrip();
	 	 file_list.append(img_name);
	 	 with open('./annotation4/' + img_name + '.pkl', 'rb') as ann:
	 	 	cur_data = pickle.load(ann);
	 	 	box = [0, 0, 0, 0]
	 	 	box_list = cur_data['pos_id']
	 	 	for i in range(len(box_list)):
	 	 		if box_list[i] != -1:
	 	 			box = cur_data['gt_pos_all'][i][box_list[i]];
	 	 	box_map[img_name] = box
	 return file_list, box_map;



#TODO: set # of boxes;
def sample(model, explainer, size, box_map, file_list):
    for i in range(num_exp):
        random_index = np.random.choice(total_num, num_sample, replace=False);
        for j in range(len(random_index)):
            img_name = file_list[i];
            box = box_map[img_name];
            img = transform_img_fn_gen([img_name], box, size);
            preds = model.predict(images_vgg)
            for x in decode_predictions(preds)[0]:
                print(x)
            explanation = explainer.explain_instance(img_name, model.predict, top_labels=1, hide_color=0, num_samples=1000)
            temp, mask = explanation.get_image_and_mask(explanation.top_labels[0], positive_only=True, num_features=5, hide_rest=True)
            result_vgg = mark_boundaries(temp / 2 + 0.5, mask);
            plt.imshow(result_vgg);
            plt.imsave(img_name + model.name + '.jpg', result_vgg);

def run_lime():
	explainer = lime_image.LimeImageExplainer()

	inet_model = inc_net.InceptionV3()
	res_model = res50.ResNet50();
	incep_res_model = incep_res_net.InceptionResNetV2();
	vgg_model = vgg16.VGG16()
	file_list, box_map = load_box();
	#VGG
	sample(vgg_model, explainer, 224, box_map, file_list);
	#resnet
	# sample(res_model, explainer, 224, box_map, file_list);
	# #inception
	# sample(inet_model, explainer, 299, box_map, file_list);  

if __name__ == '__main__':
	run_lime();




