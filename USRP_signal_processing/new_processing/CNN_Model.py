import os
import numpy as np
import keras

os.environ["KERAS_BACKEND"] = "theano"

from keras.models import Sequential
from keras.layers.core import Reshape, Dense, Dropout, Activation, Flatten
from keras.layers.noise import GaussianNoise
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.layers import Conv2D, MaxPooling2D

import _pickle as cPickle
# from signal_seperator import load_indexs_snr
# from load_data import load_all_data
#
# fft_size = 1024
# signal_samples = load_all_data('./1.13Exp_ch25/telosb_only_ch25_gain45_pow21.dat');
# label_ten_index = load_indexs_snr('telosb_only_ch25_gain45_pow21.dat')
#
# labels_zigbee = np.zeros(len(signal_samples))
# for index in range(len(label_ten_index)//2) :
#     labels_zigbee[label_ten_index[index*2]*10:label_ten_index[index*2+1]*10] = 1;
# if(len(label_ten_index)%2)!=0:
#     labels_zigbee[label_ten_index[-1]*10:] = 1;
#
# signal_num = len(signal_samples)//fft_size;
# signals = np.empty((signal_num * 2, 2, fft_size))  # complex is 2 parrt(real&imag)
# labels = np.zeros(signal_num)
# for i in range(signal_num):
#     if (i + 1) % 1000 == 0:
#         print('已解析 %d' % (i + 1) + '个')
#     # signals[i] = np.array(struct.unpack_from(fmt_image, bin_data, offset)).reshape((num_rows, num_cols))
#
#     signals[i][0] = signal_samples.real[i * fft_size:(i + 1) * fft_size]
#     signals[i][1] = signal_samples.imag[i * fft_size: (i + 1) * fft_size]
#
#     if (np.sum( labels_zigbee[i * fft_size//10:(i + 1) * fft_size//10]) > fft_size//40 ):
#         labels[i] = 1;

labels_zigbee = cPickle.load(open('./1.13Exp_gain45/pickle_file/mixed_labels.pickle', 'rb'))
signals = cPickle.load(open('./1.13Exp_gain45/pickle_file/mixed_signals.pickle', 'rb'))

Xd = signals
np.random.seed(2020)
n_examples = Xd.shape[0]
n_train = n_examples * 0.7

train_idx = np.random.choice(range(0, n_examples), size=int(n_train), replace=False)
test_idx = list(set(range(0, n_examples)) - set(train_idx))
X_train = Xd[train_idx]
X_test = Xd[test_idx]

Y_train = labels_zigbee[train_idx]
Y_test = labels_zigbee[test_idx]

print(Y_train)
num_classes = 5
Y_train = keras.utils.to_categorical(Y_train, num_classes)
Y_test = keras.utils.to_categorical(Y_test, num_classes)

in_shp = list(X_train.shape[1:])
print(X_train.shape, in_shp)

dr = 0.5  # dropout rate (%)

model = Sequential()
model.add(Reshape( in_shp + [1], input_shape=in_shp))
model.add(ZeroPadding2D((0, 2)))
model.add(Conv2D(128, (1,3), border_mode="valid", activation="relu", name="conv1", kernel_initializer="glorot_uniform",))
model.add(Dropout(dr))
model.add(ZeroPadding2D((0, 2)))
model.add(Convolution2D(64, (1,3), border_mode="valid", activation="relu", name="conv2", kernel_initializer="glorot_uniform"))
# model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(dr))
model.add(Flatten())
model.add(Dense(256, activation='relu', init='he_normal', name="dense1"))
model.add(Dropout(dr))
model.add(Dense(num_classes, init='he_normal', name="dense2"))
model.add(Activation('softmax'))
model.add(Reshape([num_classes]))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=["accuracy"])
# from keras.metrics import categorical_accuracy
# model.compile(loss='binary_crossentropy',
#  optimizer='adam', metrics=[categorical_accuracy])
model.summary()

# Set up some params
nb_epoch = 20  # number of epochs to train on
batch_size = 1024  # training batch size

# perform training ...
#   - call the main training loop in keras for our network+dataset
filepath = 'network_weights.wts.h5'
history = model.fit(X_train,
                    Y_train,
                    batch_size=batch_size,
                    epochs=nb_epoch,
                    # show_accuracy=False,
                    verbose=2,
                    validation_data=(X_test, Y_test),
                    callbacks=[
                        keras.callbacks.ModelCheckpoint(filepath, monitor='val_loss', verbose=0, save_best_only=True,
                                                        mode='auto'),
                        keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, verbose=0, mode='auto')
                    ])

# we re-load the best weights once training is finished
model.load_weights(filepath)

# Show simple version of performance
score = model.evaluate(X_test, Y_test, verbose=0, batch_size=batch_size)
print(score)