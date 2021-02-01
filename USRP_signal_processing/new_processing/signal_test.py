import numpy as np
import os
import _pickle as cPickle

import keras.utils
from keras.models import Sequential
from keras.layers.core import Reshape, Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.layers import Conv2D, MaxPooling2D

from load_data import scanFile

def pickle_to_Xd(pickle_samples, fft_size, skip_num, signal_num):
    if(len(pickle_samples)<signal_num+skip_num):
        print('incompatible samples:'+ str(len(pickle_samples)))
        signal_num = len(pickle_samples)

    IQdata_sum = 0;
    for i in range(signal_num):
        IQdata_sum += len(pickle_samples[i+skip_num])//fft_size
    signal = np.empty((IQdata_sum, 2, fft_size))

    IQdata_count = 0
    for i in range(signal_num):
        i += skip_num;
        sample_count = len(pickle_samples[i])//fft_size
        for IQcount in range(sample_count):
            signal[IQdata_count][0] = pickle_samples[i].real[IQcount*fft_size:(IQcount+1)*fft_size]
            signal[IQdata_count][1] = pickle_samples[i].imag[IQcount*fft_size:(IQcount+1)*fft_size]
            IQdata_count += 1;
    return signal

def load_pickle(filename):
    pickle_samples = cPickle.load(open(filename, 'rb'))

    fft_size = 64
    signal = pickle_to_Xd(pickle_samples, fft_size, 20, 10)

    filedir, filename = os.path.split(filename)
    fileinfo = filename[11:21]+filename[21:31]
    channel_num = int(fileinfo[2:4])
    label = np.ones(signal.shape[0]) * (channel_num - 22)

    return signal,label,fileinfo

def model_build(signal, label):
    np.random.seed(2020)

    num_classes = 5
    X_test = signal
    Y_test = keras.utils.to_categorical(label, num_classes)

    print(Y_test)

    in_shp = list(X_test.shape[1:])
    dr = 0.5  # dropout rate (%)

    model = Sequential()
    model.add(Reshape(in_shp + [1], input_shape=in_shp))
    model.add(ZeroPadding2D((0, 2)))
    model.add(Conv2D(128, (1, 3), border_mode="valid", activation="relu", name="conv1",
                     kernel_initializer="glorot_uniform", ))
    model.add(Dropout(dr))
    model.add(ZeroPadding2D((0, 2)))
    model.add(Convolution2D(64, (1, 3), border_mode="valid", activation="relu", name="conv2",
                            kernel_initializer="glorot_uniform"))
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
    # model.summary()

    # Set up some params
    nb_epoch = 2  # number of epochs to train on
    batch_size = 1024  # training batch size

    filepath = 'network_weights.wts.h5'
    model.load_weights(filepath)

    score = model.evaluate(X_test, Y_test, verbose=0, batch_size=batch_size)
    print(score)

    return

if __name__ == '__main__':
    # IQSamples = load_all_data('./1.13Exp_ch25/telosb_only_ch25_gain45_pow31.dat')
    filelist = scanFile('./1.13Exp_ch25/pickle_file','.pickle')
    print(filelist)
    os.chdir('../..')
    for filename in filelist:
        if (filename[13:23] == 'ch24__pow3' or filename[13:23] == 'ch26__pow3' or filename=='mixed_labels.pickle' or filename=='mixed_signals.pickle' or filename[13:23]=='ch23__pow3'):
            continue
        signal,label,fileinfo = load_pickle('./1.13Exp_ch25/pickle_file/'+filename)
        # print(signal.shape, label.shape)
        print(fileinfo)
        model_build(signal,label)


    pass




