import os

dir_name = './flickr30k_resnet/'
alreadyDoneFile = open('alreadyDone_resnet.txt', 'w')

for filename in os.listdir(dir_name):
    if filename.endswith(".npy"):
	alreadyDoneFile.write(filename[:-4] + '\n')
       
alreadyDoneFile.close()
