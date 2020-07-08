import numpy as np
import _pickle as cPickle

# from plot_data import plot_IQ
from feature_extraction import cal_mag,feature_cal,find_continuous_indexs
# from load_data import load_data

if __name__ == '__main__':
    fft_size = 64
    signal_num = 199094

    IQcommplex = cPickle.load(open("Data/pickle_file/same_samples_mixed_signal_n199094_fft_size_1024.pickle", 'rb'))
    labels = cPickle.load(open('Data/pickle_file/same_samples_mixed_signal_label_n199094.pickle', 'rb'))

    # find_continuous_indexs(labels)
    print("oringal data shape: "+ str(IQcommplex.shape))
    # print("original label num: " + sum(np.array(labels)==1))

    multiple = int(1024/fft_size)
    # labels = labels.repeat(multiple)

    IQcommplex_cut = np.empty((len(IQcommplex), 2, fft_size))
    ## len(IQcommplex)：样本数量
    for i in range(len(IQcommplex)):
            # IQcommplex_256_real = np.split(IQcommplex[i][0], multiple) #分成multiple份，每份fft_size个点
            # IQcommplex_256_imag = np.split(IQcommplex[i][1], multiple)
            # IQcommplex_cut[i][0] = IQcommplex_256_real[1] #multiple份只取第二段
            # IQcommplex_cut[i][1] = IQcommplex_256_imag[1]
        IQcommplex_cut[i][0] = np.split(IQcommplex[i][0], multiple)[1]  # multiple份只取第二段
        IQcommplex_cut[i][1] = np.split(IQcommplex[i][1], multiple)[1]

    print(IQcommplex_cut.shape)

    # np.split(IQcommplex, len(IQcommplex)*4)

    #IQcomplex_zigbee是个复数信号，有real和imag部分



    file = open('Data/pickle_file/same_samples_mixed_signal_n' + str(len(IQcommplex_cut)) + '_fft_size_' + str(fft_size) + '.pickle', 'wb')
    cPickle.dump(IQcommplex_cut, file)
    file.close()

    file = open('Data/pickle_file/same_samples_mixed_signal_label_n' + str(len(labels)) + '_fft_size_' + str(fft_size) +'.pickle','wb')
    cPickle.dump(labels,file)
    file.close()