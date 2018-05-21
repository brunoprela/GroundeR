# GroundeR
This repository contains implementation for *Grounding of Textual Phrases in Images by Reconstruction* in [ECCV 2016](https://arxiv.org/pdf/1511.03745.pdf). We borrow an implementation from kanchen-usc. Please see [kanchen-usc/GroundeR](https://github.com/kanchen-usc/GroundeR) for the original repo.

## Setup

> Note: Please read the feature representation files in ```feature``` and ```annotation``` directories before using the code. Also please make sure to replace all path constants in the files with your own path constants!

**Platform:** matlab_R2016a for representation files, Python 2.7 for training, evaluation, explanations<br/>

To setup a virtual environment named 'env' type: ```virtualenv env -p python2``` or ```virtualenv env -p python``` if Python 2.7 is your default Python version. You can check which Python version you have by typing: ```python --version```.

To enter your virtual environment type: ```source env/bin/activate```. Then install dependencies by doing ```pip install -r requirements.txt```. Complete whatever Python actions you need within this environment and then deactivate it by typing ```deactivate``` when you are done.

**Visual features:** TODO We use [Faster-RCNN](https://github.com/endernewton/tf-faster-rcnn) pre-trained on PASCAL 2012 VOC for [Flickr30K Entities](http://web.engr.illinois.edu/~bplumme2/Flickr30kEntities/), and pre-trained on ImageNet for [Referit Game](http://tamaraberg.com/referitgame/). Please put visual features in the ```feature``` directory (More details can be seen in the [```README.md```](./feature/README.md) in this directory). (Fine-tuned features can achieve better performance, which are available in this [repository](https://github.com/kanchen-usc/QRC-Net)).<br/>
**Sentence features:** TODO We encode one-hot vector for each query, as well as the annotation for each query and image pair. Please put the encoded features in the ```annotation``` directory (More details are provided in the [```README.md```](./annotation/README.md) in this directory).<br/>
**File list:** TODO We generate a file list for each image in the Flickr30K Entities. If you would like to train and test on other dataset (e.g. [Referit Game](http://tamaraberg.com/referitgame/)), please follow the similar format in the ```flickr_train_val.lst``` and ```flickr_test.lst```.<br/>
**Hyper parameters:** TODO Please check the ```Config``` class in the ```train_supervise.py``` and ```train_unsupervise.py```.

## Training & Test

We implement GroundeR, GroundeR-ResNet and GroundeR-Inception.

### Supervised Models
For training, please enter the root folder of ```GroundeR```, then get the original GroundeR training by typing the following (pick descriptive model names based on the .py file being run):
```
$ python train_supervise.py -m [Model Name] -g [GPU ID]
```
In different instances of terminal (or tmux) each, also type the following for the GroundeR-ResNet and GroundeR-Inception training respectively
```
$ python train_supervise_res.py -m [Model Name] -g [GPU ID]


$ python train_supervise_inception.py -m [Model Name] -g [GPU ID]
```
For testing, please enter the root folder of ```GroundeR```, then type
```
$ python evaluate_supervise.py -m [Model Name] -g [GPU ID] --restore_id [Restore epoch ID]
```
Make sure the model name entered for evaluation is the same as the model name in training, and the epoch id exists.

## G-LIME Explanations

```
TODO
```