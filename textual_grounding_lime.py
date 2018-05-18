import os, sys
import numpy as np
import keras
from keras.applications import inception_v3 as inc_net
from keras.applications import resnet50 as res50
from keras.applications import inception_resnet_v2 as incep_res_net
from keras.applications import vgg16 as vgg16
from keras.preprocessing import image
from keras.applications.imagenet_utils import decode_predictions
from skimage.io import imread
import matplotlib.pyplot as plt
import lime
from lime import lime_image

print('Notebook run using keras:', keras.__version__)
inet_model = inc_net.InceptionV3()
res_model = res50.ResNet50()
incep_res_model = incep_res_net.InceptionResNetV2()
vgg_model = vgg16.VGG16()

def transform_img_fn(path_list):
    out = []
    for img_path in path_list:
        img = image.load_img(img_path, target_size=(299, 299))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = inc_net.preprocess_input(x)
        out.append(x)
    return np.vstack(out)

#images = transform_img_fn([os.path.join('data','cat_mouse.jpg')])
images = transform_img_fn(['65567.jpg'])
# I'm dividing by 2 and adding 0.5 because of how this Inception represents images
plt.imshow(images[0] / 2 + 0.5)
#preds = res_model.predict(images)
preds = inet_model.predict(images)
for x in decode_predictions(preds)[0]:
    print(x)
# preds = incep_res_model.predict(images)
# for x in decode_predictions(preds)[0]:
#     print(x)


explainer = lime_image.LimeImageExplainer()
explanation = explainer.explain_instance(images[0], inet_model.predict, top_labels=5, hide_color=0, num_samples=1000)
from skimage.segmentation import mark_boundaries
print(explanation.top_labels)
temp, mask = explanation.get_image_and_mask(627, positive_only=True, num_features=5, hide_rest=True)
plt.imshow(mark_boundaries(temp / 2 + 0.5, mask))

def transform_img_fn_vgg(path_list):
    out = []
    for img_path in path_list:
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = inc_net.preprocess_input(x)
        out.append(x)
    return np.vstack(out)

images_vgg = transform_img_fn_vgg(['65567.jpg'])
preds = vgg_model.predict(images)
for x in decode_predictions(preds)[0]:
    print(x)
explanation_vgg = explainer.explain_instance(images[0], vgg_model.predict, top_labels=5, hide_color=0, num_samples=1000)
print(explanation_vgg.top_labels)
temp_vgg, mask_vgg = explanation_vgg.get_image_and_mask(520, positive_only=True, num_features=5, hide_rest=True)
plt.imshow(mark_boundaries(temp_vgg / 2 + 0.5, mask_vgg));
