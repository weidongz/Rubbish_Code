
import _pickle as cPickle
import numpy as np
from time import time
import keras
from keras.models import Sequential
from keras.layers.core import Reshape, Dense, Dropout, Activation, Flatten
from keras.layers.noise import GaussianNoise
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.layers import Conv2D, MaxPooling2D
import sklearn.metrics as metrics
import matplotlib .pyplot as plt
import itertools

def load_dataset(datapath, labelpath):
    # Xd = cPickle.load(open("mixed_signal_n3186784_fft_size_64.pickle", 'rb'))
    # labels_zigbee = cPickle.load(open('mixed_signal_label_n3186784_fft_size_64.pickle','rb'))
    Xd = cPickle.load(open(datapath, 'rb'))
    labels_zigbee = cPickle.load(open(labelpath,'rb'))

    n_examples = Xd.shape[0]
    n_train = n_examples*0.5

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
    return X_train, X_test, Y_train, Y_test, in_shp, num_classes

def load_model(in_shp, num_classes):
    dr = 0.5
    model = Sequential()
    model.add(Reshape([1] + in_shp, input_shape=in_shp))
    model.add(ZeroPadding2D((0, 2)))
    model.add(Conv2D(256, 1, border_mode="valid", activation="relu", name="conv1", kernel_initializer="glorot_uniform",))
    model.add(Dropout(dr))
    model.add(ZeroPadding2D((0, 2)))
    model.add(Convolution2D(80, 1, border_mode="valid", activation="relu", name="conv2", kernel_initializer="glorot_uniform"))
    model.add(Dropout(dr))
    model.add(Flatten())
    model.add(Dense(256, activation='relu', init='he_normal', name="dense1"))
    model.add(Dropout(dr))
    model.add(Dense(num_classes, init='he_normal', name="dense2"))
    model.add(Activation('softmax'))
    model.add(Reshape([num_classes]))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=["accuracy"])
    model.summary()

    filepath = 'convmodrecnets_CNN2_0.5.wts.h5'
    model.load_weights(filepath)

    return model

def load_DNN_model(in_shp, num_classes, filepath):
    dr = 0.5
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
    model.summary()

    model.load_weights(filepath)
    return model


def calc_RunTime(model, X_test, Y_test):
    # Show simple version of performance
    begin_time = time()
    score = model.evaluate(X_test, Y_test, verbose=0, batch_size=1024)
    end_time = time()

    print(score)
    print ('该循环程序运行时间：', (end_time-begin_time)/(X_test.shape[0])) #该循环程序运行时间： 1.4201874732
    # 64: 0.00032315354346534723, 0.0003260678396332039
    # 128:  0.0005723794561611414, 0.0005817068924001852
    # 256: 0.0011669603961846212
    # 512:  0.0024203322601410327
    # 1024: 0.004590647122918083

def plot_confusion_matrix_fail(model, X_test, Y_test):
    m_fontsize = 20
    labels = ['Noise', 'ZigBee']
    # labels = ['Noise', 'ZigBee', 'WiFi']
    y_pred_ohe = model.predict(X_test)
    y_pred_labels = np.argmax(y_pred_ohe, axis=1)
    # pd.crosstab(true_label,y_pred_labels,rownames=['label'],colnames=['predict'])
    matrix = metrics.confusion_matrix(y_true=Y_test, y_pred=y_pred_labels)
    plt.matshow(matrix)
    plt.colorbar()
    plt.xlabel('Predicted label', fontsize=m_fontsize)
    plt.ylabel('True label', fontsize=m_fontsize)
    plt.xticks(np.arange(matrix.shape[1]),labels, fontsize=m_fontsize)
    plt.yticks(np.arange(matrix.shape[1]),labels, fontsize=m_fontsize)
    plt.show()

def plot_confusion_matrix(cm, classes,
                          title='Confusion matrix',
                          cmap=plt.cm.jet):
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, '{:.10f}'.format(cm[i, j]), horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "white", fontsize='large')
    plt.tight_layout()
    plt.ylabel('True label', fontsize='large')
    plt.xlabel('Predicted label', fontsize='large')
    plt.savefig("paper_images/conf_metrix.png",bbox_inches='tight')
    plt.show()
#
# 显示混淆矩阵
def plot_confuse(model, x_val, y_val):
    predictions = model.predict_classes(x_val)
    truelabel = y_val.argmax(axis=-1)   # 将one-hot转化为label
    conf_mat = metrics.confusion_matrix(y_true=truelabel, y_pred=predictions)
    print(conf_mat)
    conf_mat = np.array([[1453021, 272], [0, 138640]])
    plt.figure()
    plot_confusion_matrix(conf_mat, range(np.max(truelabel)+1))
#
# classes = ["Noise", "ZigBee"]
# plot_confusion_matrix(matrix, classes)

# print(y_pred_labels.shape)

if __name__=='__main__':
    # datapath = 'mixed_signal_n3186784_fft_size_64.pickle'
    # labelpath = 'mixed_signal_label_n3186784_fft_size_64.pickle'
    # filepath = 'Data/network_weights/deep_num3186784_size64.wts.h5'

    datapath = 'Data/pickle_file/same_samples_mixed_signal_n199094_fft_size_64.pickle'
    labelpath = 'Data/pickle_file/same_samples_mixed_signal_label_n199094_fft_size_64.pickle'
    filepath = 'Data/network_weights/zigbee_deep_size64.wts.h5'
    # filepath = 'Data/network_weights/deep_num199094_size1024.wts.h5'
    X_train, X_test, Y_train, Y_test, in_shp, num_classes = load_dataset(datapath, labelpath);
    model = load_DNN_model(in_shp, num_classes, filepath);
    calc_RunTime(model, X_test, Y_test)
    # plot_confusion_matrix_fail(model, X_test, Y_test)
    # y_pred_ohe = model.predict(X_test)
    # y_pred_labels = np.argmax(y_pred_ohe, axis=1)
    # matrix = metrics.confusion_matrix(y_true=Y_test, y_pred=y_pred_labels)
    # classes = ["Noise", "ZigBee"]
    plot_confuse(model, X_test, Y_test)