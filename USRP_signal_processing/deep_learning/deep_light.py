import sys
import _pickle as cPickle

print(sys.path)
import os, random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random, sys, keras
from time import time

os.environ["KERAS_BACKEND"] = "theano"
# os.environ["KERAS_BACKEND"] = "tensorflow"
# os.environ["THEANO_FLAGS"] = "device=gpu%d" % (1)  # 报错，该代码表示使用GPU1运行theano
# os.environ["THEANO_FLAGS"] = "device=gpu0"

import theano as th
import theano.tensor as T
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Reshape, Dense, Dropout, Activation, Flatten
from keras.layers.noise import GaussianNoise
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.layers import Conv2D, MaxPooling2D
from keras.regularizers import *
from keras.optimizers import adam

from feature_extraction import cal_mag,feature_cal,find_continuous_indexs

# Load the dataset ...
#  You will need to seperately download or generate this file
# Xd = cPickle.load(open("zigbee_signal_n10000_fft_size_1024.pickle", 'rb'))
# labels_zigbee = cPickle.load(open('signal_label.pikle','rb'))
## mixed ZigBee & WiFi with size 1024
# Xd = cPickle.load(open("mixed_signal_n200000_fft_size_1024.pickle", 'rb'))
# labels_zigbee = cPickle.load(open('mixed_signal_three_label_n200000.pickle','rb'))
## for size 256
# Xd = cPickle.load(open("mixed_signal_n400000_fft_size_256.pickle", 'rb'))
# labels_zigbee = cPickle.load(open('mixed_signal_label_n400000_fft_size_256.pickle','rb'))
# Xd = cPickle.load(open("mixed_signal_n3186784_fft_size_64.pickle", 'rb'))
# labels_zigbee = cPickle.load(open('mixed_signal_label_n3186784_fft_size_64.pickle','rb'))
## for same samples
fft_size = 1024
Xd = cPickle.load(open("Data/pickle_file/same_samples_mixed_signal_n199094_fft_size_1024.pickle", 'rb'))
labels_zigbee = cPickle.load(open('Data/pickle_file/same_samples_mixed_signal_label_n199094_fft_size_1024.pickle','rb'))

# Partition the data
#  into training and test sets of the form we can train/test on
#  while keeping SNR and Mod labels handy for each
np.random.seed(2020)
n_examples = Xd.shape[0]
n_train = n_examples * 0.6

train_idx = np.random.choice(range(0, n_examples), size=int(n_train), replace=False)
test_idx = list(set(range(0, n_examples)) - set(train_idx))
X_train = Xd[train_idx]
X_test = Xd[test_idx]

Y_train = labels_zigbee[train_idx]
Y_test = labels_zigbee[test_idx]

num_classes = 2
Y_train = keras.utils.to_categorical(Y_train, num_classes)
Y_test = keras.utils.to_categorical(Y_test, num_classes)

in_shp = list(X_train.shape[1:])
print(X_train.shape, in_shp)


dr = 0.5  # dropout rate (%)
# model = Sequential()
# # model.add(Reshape([1] + in_shp, input_shape=in_shp))
# model.add(ZeroPadding2D((0, 2)))
# # model.add(Convolution2D(256, 1, 3, border_mode='valid', activation="relu", name="conv1", init='glorot_uniform'))
# model.add(Convolution2D(256, 1, 3, border_mode='valid', activation="relu", name="conv1", kernel_initializer="glorot_uniform", padding="valid"))
# model.add(Dropout(dr))
# model.add(ZeroPadding2D((0, 2)))
# model.add(Convolution2D(80, 2, 3, border_mode="valid", activation="relu", name="conv2", kernel_initializer="glorot_uniform", padding="valid"))
# model.add(Dropout(dr))
# model.add(Flatten())
# model.add(Dense(256, activation='relu', init='he_normal', name="dense1"))
# model.add(Dropout(dr))
# model.add(Dense(len(classes), init='he_normal', name="dense2"))
# model.add(Activation('softmax'))
# model.add(Reshape([len(classes)]))
# model.compile(loss='categorical_crossentropy', optimizer='adam')
# model.summary()

# model type:
# - Reshape [N,2,fft_size] to [N,1,2,fft_size] on input
# - Pass through 2 2DConv/ReLu layers
#  - Perform categorical cross entropy optimization

model = Sequential()
model.add(Reshape( in_shp + [1], input_shape=in_shp))
model.add(ZeroPadding2D((0, 2)))
model.add(Conv2D(128, (1,3), border_mode="valid", activation="relu", name="conv1", kernel_initializer="glorot_uniform",))
model.add(Dropout(dr))
# model.add(ZeroPadding2D((0, 2)))
# model.add(Convolution2D(64, (1,3), border_mode="valid", activation="relu", name="conv2", kernel_initializer="glorot_uniform"))
# model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(dr))
model.add(Flatten())
# model.add(Dense(256, activation='relu', init='he_normal', name="dense1"))
# model.add(Dropout(dr))
model.add(Dense(num_classes, init='he_normal', name="dense2"))
model.add(Activation('softmax'))
model.add(Reshape([num_classes]))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=["accuracy"])
model.summary()

# Set up some params
nb_epoch = 2  # number of epochs to train on
batch_size = 1024  # training batch size

# perform training ...
#   - call the main training loop in keras for our network+dataset
filepath = 'Data/network_weights/lightdeep_num'+str(n_examples)+'_size'+str(fft_size)+'.wts.h5'
# filepath = 'Data/network_weights/lightdeep_num'+'199094'+'_size'+str(fft_size)+'.wts.h5'

# history = model.fit(X_train,
#                     Y_train,
#                     batch_size=batch_size,
#                     epochs=nb_epoch,
#                     # show_accuracy=False,
#                     verbose=2,
#                     validation_data=(X_test, Y_test),
#                     callbacks=[
#                         keras.callbacks.ModelCheckpoint(filepath, monitor='val_loss', verbose=0, save_best_only=True,
#                                                         mode='auto'),
#                         keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, verbose=0, mode='auto')
#                     ])

# we re-load the best weights once training is finished
model.load_weights(filepath)

# Show simple version of performance

begin_time = time()
score = model.evaluate(X_test, Y_test, verbose=0, batch_size=batch_size)
end_time = time()

print(score)
print('该循环程序运行时间：', (end_time - begin_time) / (X_test.shape[0])*1000000, ' us')