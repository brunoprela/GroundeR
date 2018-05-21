
# coding: utf-8




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
from PIL import Image as pil_image

# from dataprovider_supervise import dataprovider
# from model_supervise import ground_model

#to read pkl file
import pickle

import matplotlib.pyplot as plt
#matplotlib inline
import numpy as np

print('Notebook run using keras:', keras.__version__)





_PIL_INTERPOLATION_METHODS = {
      'nearest': pil_image.NEAREST,
      'bilinear': pil_image.BILINEAR,
      'bicubic': pil_image.BICUBIC,
  }
total_num = 1000
num_sample = 3
num_exp = 1
#random_index = np.random.choice(total_num, num_sample, replace=False);
random_index = [89, 587, 577]





explainer = lime_image.LimeImageExplainer()





#print(random_index)





inet_model = inc_net.InceptionV3()
res_model = res50.ResNet50()
#incep_res_model = incep_res_net.InceptionResNetV2();
vgg_model = vgg16.VGG16()




#crop then resize
def transform_img_fn_gen(path_list, box, size):
    out = []
    for img_path in path_list:
        temp = pil_image.open(img_path)
        cropped = temp.crop(box.tolist()[0])
        resample = _PIL_INTERPOLATION_METHODS['nearest']
        img = cropped.resize((size, size), resample)
        #img = image.load_img(img_path, target_size=(299, 299))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = inc_net.preprocess_input(x)
        out.append(x)
    return np.vstack(out)

#get box for each image
#box_map: dict map from image_name to the ground truth bounding box
def load_box():
    f = open('./flickr30k_test.lst')
    box_map = {}
    index_map = {}
    file_list = []
    for line in f:
        img_name = line.rstrip()
        file_list.append(img_name)
        with open('./annotation/' + img_name + '.pkl', 'rb') as ann:
            cur_data = pickle.load(ann)
            box_list = cur_data['gt_box']
            #get a random box 
            #save corresponding phrases here
            index = np.random.randint(len(box_list))
            box_map[img_name] = box_list[index]
            index_map[img_name] = index
    f2 = open('./flickr30k_train.lst')
    for line in f2:
        img_name = line.rstrip()
        file_list.append(img_name)
        with open('./annotation/' + img_name + '.pkl', 'rb') as ann:
            cur_data = pickle.load(ann)
            box_list = cur_data['gt_box']
            #get a random box 
            #save corresponding phrases here
            index = np.random.randint(len(box_list))
            box_map[img_name] = box_list[index]
            index_map[img_name] = index
    return file_list, box_map, index_map

#get a certain query for an image in the form of a list of string
def get_query(file_name, index):
    fn = './annotation/' + fileNameOnly + '.mat'
    mat = scipy.io.loadmat(fn)
    temp = mat['wordList'][0]
    phrase = [temp[index][j][0] for j in range(len(temp[index]))]
    return phrase
            

#Get LIME explinations for a list of cropped images        
#box_map: map from image name to box.
def sample(model, explainer, size, box_map, file_list, random_index):
    exp_list = [];
    #for i in range(num_exp):
    for j in range(len(random_index)):
        name = file_list[random_index[i]]
        img_name = './flickr30k_images/' + name + '.jpg'
        print(img_name)
        box = box_map[name]
        print(box)
        img = transform_img_fn_gen([img_name], box[0], size)
        plt.imshow(img[0] / 2 + 0.5)
        preds = model.predict(img)
        for x in decode_predictions(preds)[0]:
            print(x)
        explaination = explainer.explain_instance(img[0], model.predict, top_labels=1, hide_color=0, num_samples=1000)
        exp_list.append(explaination)
    return exp_list
  
# for one image, output superpixels  
def print_result(explaination, file_list, index, model):
    temp, mask = explaination.get_image_and_mask(explaination.top_labels[0], positive_only=False, num_features=10, hide_rest=False)
    result = mark_boundaries(temp / 2 + 0.5, mask)
    plt.imshow(result)
    plt.imsave(file_list[index] + model.name + '.jpg', result)


#functions for drawing boxes
import matplotlib.patches as patches

def draw_rect(file_name, box):
    img = np.array(pil_image.open(file_name + 'jpg', dtype=np.uint8))
    fig,ax = plt.subplots(1)
    ax.imshow(img)
    rect = patches.Rectangle((box[0],box[1]),box[2] - box[0],box[3] - box[1],linewidth=1,edgecolor='r',facecolor='none')
    ax.add_patch(rect)
    plt.show()

def get_img_with_box(file_list, random_index, box_map, index_map):
    for i in range(len(random_index)):
        file_name = file_list[random_index[i]]
        cur_q = get_query(file_name, index_map[file_name])
        print(cur_q)
        draw_rect(file_name, box_map[file_name])
        




file_list, box_map, index_map = load_box();




# for i in range(len(random_index)):
#     print file_list[random_index[i]];





# %store -r index_map





# %store -r box_map





explaination_vgg = sample(vgg_model, explainer, 224, box_map, file_list, random_index);
for i in range(len(explaination_vgg)):
    print_result(explaination_vgg[i], file_list, random_index[i], vgg_model);





explaination_res = sample(res_model, explainer, 224, box_map, file_list, random_index);
for i in range(len(explaination_res)):
    print_result(explaination_res[i], file_list, random_index[i], vgg_model);





explaination_inet = sample(inet_model, explainer, 299, box_map, file_list, random_index);
for i in range(len(explaination_res)):
    print_result(explaination_res[i], file_list, random_index[i], vgg_model);





#get_ipython().system(u'jupyter nbconvert --to script Untitled3-Copy3.ipynb')

