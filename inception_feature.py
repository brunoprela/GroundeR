import os
import torch
import torchvision.models as models
import torchvision.transforms as transforms
import torch.nn.functional as functional
from torch.autograd import Variable
from scipy.io import loadmat
from PIL import Image
import numpy as np

model = models.inception_v3(pretrained=True)

layer = model._modules.get('Mixed_7c')
model.eval()
scaler = transforms.Resize((299, 299))
normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                         std=[0.229, 0.224, 0.225])
to_tensor = transforms.ToTensor()

def get_vector(img):
    # 1. Load the image with Pillow library
    # img = Image.open(image_name)
    # 2. Create a PyTorch Variable with the transformed image
    t_img = Variable(normalize(to_tensor(scaler(img))).unsqueeze(0))
    # 3. Create a vector of zeros that will hold our feature vector
    #    The 'avgpool' layer has an output size of 512
    my_embedding = torch.zeros(1, 2048, 8, 8)
    # 4. Define a function that will copy the output of a layer
    def copy_data(m, i, o):
        my_embedding.copy_(o.data)
    # 5. Attach that function to our selected layer
    h = layer.register_forward_hook(copy_data)
    # 6. Run the model on our transformed image
    model(t_img)
    # 7. Detach our copy function from the layer
    h.remove()
    # 8. Return the feature vector
    return functional.avg_pool2d(my_embedding, kernel_size=8)

if __name__ == "__main__":


    FLICKR30K_IMAGE_DIR = '/home/brunoprela/6.883/flickr30k_images'
    FLICKR30K_IMAGE_BBX_SS_DIR = '/home/brunoprela/6.883/flickr30k_img_bbx_ss'
    FLICKR30K_INCEPTION_DIR = '/home/brunoprela/6.883/flickr30k_inception'
    # loop through images
    count = 0
    for filename in os.listdir(FLICKR30K_IMAGE_DIR):
        # initialize output
        result = []
        # open the image
        img = Image.open(FLICKR30K_IMAGE_DIR + '/' + filename)
        image_name = filename[:-4]
        # load the box matrix, boxes in 'cur_bbxes'
        data = loadmat(FLICKR30K_IMAGE_BBX_SS_DIR + '/' + image_name + '.mat')
        # loop through the box matrix
        for area in data['cur_bbxes']:
            cropped_img = img.crop(area)
            feat_vector = get_vector(cropped_img)
            result.append([feat_vector[0][i][0][0].numpy() for i in range(feat_vector.shape[1])])
        np.save(FLICKR30K_INCEPTION_DIR + '/' + image_name + '.npy', result)
        count += 1
        print 'count: ' + str(count)
