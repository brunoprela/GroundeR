import os

dir_name = './annotation/'
alreadyDoneFile = open('alreadyDone.txt', 'w')

for filename in os.listdir(dir_name):
    if filename.endswith(".pkl"):
	alreadyDoneFile.write(filename[:-4] + '\n')
       
alreadyDoneFile.close()
