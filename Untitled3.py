
# coding: utf-8

# In[1]:


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


# In[3]:


_PIL_INTERPOLATION_METHODS = {
      'nearest': pil_image.NEAREST,
      'bilinear': pil_image.BILINEAR,
      'bicubic': pil_image.BICUBIC,
  }
total_num = 1000
num_sample = 1
num_exp = 1


# In[29]:


def transform_img_fn_gen(path_list, box, size):
    out = []
    for img_path in path_list:
        temp = pil_image.open(img_path);
        cropped = temp.crop(box.tolist()[0]);
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
	 	 	box_list = cur_data['gt_box'];
            #get a random box 
            #save corresponding phrases here
	 	 	index = np.random.randint(len(box_list));
	 	 	box_map[img_name] = box_list[index];
	 return file_list, box_map;



#TODO: set # of boxes;
def sample(model, explainer, size, box_map, file_list):
    namelist = [];
    for i in range(num_exp):
        random_index = np.random.choice(total_num, num_sample, replace=False);
        for j in range(len(random_index)):
            img_name = './flickr30k_images/' + file_list[i] + '.jpg';
            namelist.append(file_list[i]);
            box = box_map[file_list[i]];
            img = transform_img_fn_gen([img_name], box[0], size);
            preds = model.predict(img)
            for x in decode_predictions(preds)[0]:
                print(x)
            explaination = explainer.explain_instance(img[0], model.predict, top_labels=1, hide_color=0, num_samples=1000)
            temp, mask = explaination.get_image_and_mask(explaination.top_labels[0], positive_only=False, num_features=10, hide_rest=False)
            result = mark_boundaries(temp / 2 + 0.5, mask);
            plt.imshow(result);
            plt.imsave(file_list[i] + model.name + '.jpg', result);


# In[25]:


explainer = lime_image.LimeImageExplainer()


# In[26]:


inet_model = inc_net.InceptionV3()
res_model = res50.ResNet50();
incep_res_model = incep_res_net.InceptionResNetV2();
vgg_model = vgg16.VGG16()


# In[27]:


file_list, box_map = load_box();


# In[30]:


sample(vgg_model, explainer, 224, box_map, file_list);


# In[23]:


sample(res_model, explainer, 224, box_map, file_list);


# In[ ]:


sample(inet_model, explainer, 299, box_map, file_list);  


# In[ ]:


get_ipython().system(u'jupyter nbconvert --to script Untitled3.ipynb')

