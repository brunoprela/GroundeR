import numpy as np
#import pandas as pd
#import selectivesearch
import os
#import imageio
import scipy.io
import pickle

# Constants
# TODO: Bruno: should change these, perhaps put them in an environment vars files
ANNOTATION_TOKEN_PATH = '/Users/brunoprela/Documents/Projects/6.883/flickr30k_images/results_20130124.token'
FLICKR_IMAGE_PATH = '/Users/brunoprela/Documents/Projects/6.883/flickr30k_images/flickr30k_images'
FLICKR_ANNOTATIONS_PATH = '/Users/brunoprela/Documents/Projects/6.883/Flickr30kEntities/Annotations'
FLICKR_SENTENCES_PATH = '/Users/brunoprela/Documents/Projects/6.883/Flickr30kEntities/Sentences'


def read_mat(fn):
	mat = scipy.io.loadmat(fn);
	dictionary = {};
	size = 0;

	result = {};
	temp = mat['propList'];
	temp2 = [];
	for i in range(len(temp[0])):
		temp_list = temp[0][i][0].astype(int).tolist();
		if (len(temp_list) == 1) and (temp_list[0] == -2):
			temp_list = [];
		temp2.append(temp_list);
	result['gt_pos_all'] = temp2;
	temp = mat['propidList'];
	result['pos_id'] = [temp[0][i].astype(int)[0][0] for i in range(len(temp[0]))];
	#print(result['pos_id'])
	temp = mat['wordList'][0]
	temp2 = [];
	for i in range(len(temp)):
		temp_list = [temp[i][j][0].astype('str')[0] for j in range(len(temp[i]))];
		final_list = [];
		for w in temp_list:
			if w not in dictionary:
				dictionary[w] = size;
				final_list.append(size);
				size += 1;
			else:
				final_list.append(dictionary[w]);

	 	temp2.append(final_list);
	result['sens'] = temp2;
	temp = mat['boxList'][0]
	print(len(temp[0]))
	temp2 = [temp[i][0].astype(int) for i in range(len(temp))]
	result['gt_box'] = np.asmatrix(temp2);
	print(result);
	f = open('./annotation/6609688031.pkl', 'wb');
	pickle.dump(result, f, protocol=pickle.HIGHEST_PROTOCOL);
	f.close();
	

# Helper Functions

def get_Iou(b1, b2):
	xmin = np.max(b1[0], b2[0]);
	ymin = np.max(b1[1], b2[1]);
	xmax = np.min(b1[2], b2[2]);
	ymax = np.min(b1[3], b2[3]);

	intersection = get_area(xmax - xmin, ymax - ymin);
	union = get_area(b1[2] - b1[0], b1[3] - b1[1]) + get_area(b2[2] - b2[0], b2[3] - b2[1]) - intersection;
	return intersection / union

def get_area(w, h):
	return w * h

# Main Functions

#It is a list of length N. N represents the number of queries. The i-th element of this list is also a list, 
#recording the i-th query's positive proposals' IDs among the 100 proposals generated by Selective Search or Edge Box.
#The positive proposals are defined as the proposals with an Intersection of Union (IoU) larger than 0.5 for the 
#corresponding ground truth bounding box of the i-th query.
def get_gt_pos_all():
	annotations = pd.read_table(ANNOTATION_TOKEN_PATH, sep='\t', header=None, names=['image', 'caption'])
	annotations['image_num'] = annotations['image'].map(lambda x: x.split('#')[1])
	annotations['image'] = annotations['image'].map(lambda x: os.path.join(FLICKR_IMAGE_PATH, x.split('#')[0]))
	print annotations

	for img in annotations['image']:
		im = imageio.imread(img)
		print(im.shape)
		img_lbl, regions = selectivesearch.selective_search(im, scale=500, sigma=0.9, min_size=50)

		candidates = set()
		for r in regions:
			# excluding same rectangle (with different segments)
			if r['rect'] in candidates:
				continue
			# excluding regions smaller than 2000 pixels
			if r['size'] < 2000:
				continue
			# distorted rects
			x, y, w, h = r['rect']
			if w / h > 1.2 or h / w > 1.2:
				continue
			candidates.add(r['rect'])

		print "Candidate size: " + len(candidates)

		# for region in candidates:
		# 	for annotations in
	# regions[:10]
	return


#It is an N dimensional vector. The i-th element represent the proposal ID which covers most with ground truth bounding 
#box for the i-th query. If the most covered proposal's IoU is less than 0.5, we replace the proposal ID as -1.
def get_pos_id():
	return


#It is a list of length N. The i-th element of this list is also a list, which represents the word ID sequence of the i-th query.
def get_sens():
	return

#It is an N x 4 matrix. The i-th row represents the ground truth bounding box annotation for the i-th query. 
#The annotation is in the form of [xmin, ymin, xmax, ymax].
def get_gt_box(ann, dict):
	return

if __name__ == '__main__':
	# eng = matlab.engine.start_matlab();
	# fn = './Flickr30kEntities/Annotations/6609688031.xml'
	# #print type(eng.getAnnotations())
	# annotation = eng.getAnnotations(fn);
	# print annotation;
	#get_gt_pos_all()
	for f in os.listdir('./Flickr30kEntities/Annotations'):
		fn = './annotation/' + f[:-4] + '.mat';
		read_mat(fn);

		#read_mat('./6609688031.mat');
	




