import numpy as np
import _pickle as cPickle

from plot_data import plot_IQ
from feature_extraction import cal_mag,feature_cal,find_continuous_indexs
from load_data import load_data

if __name__ == '__main__':
    fft_size = 1024
    signal_num = 100000

    ## IQcomplex_zigbee是个复数信号，有real和imag部分
    IQcomplex_zigbee = load_data(size=fft_size, filename='Data/usrp_25M_data_with_telosb.dat', n=signal_num )
    # plot_IQ(IQcomplex_zigbee, IQIndex=120, bins=fft_size)

    center_freqs_zigbee, bandwidths_zigbee, indexs_zigbee = feature_cal(IQcomplex_zigbee, n=signal_num, bins=fft_size)
    labels_zigbee = np.zeros(len(center_freqs_zigbee))

    for index in indexs_zigbee:
        labels_zigbee[index] = 1
    labels_zigbee = np.array(labels_zigbee)

    ## deal with wrong labels and miss labels
    find_continuous_indexs(labels_zigbee)
    unordinary_index = [8073, 9827, 12363, 14787, 16857 , 20747, 27483, 30407, 39810, 42346, 43957, 44770, 52303, 54839, 68126, 72329, 77289, 82286, 84822, 87246, ]
    missed_index  = [14033, 14034]
    for i in unordinary_index:
        labels_zigbee[i] = 0
    for i in missed_index:
        labels_zigbee[i] = 1


    IQcomplex_wifi = load_data(size=fft_size, filename='Data/usrp_wifi_cf2433M_sr25M.dat', n=signal_num)
    center_freqs_wifi, bandwidths_wifi, indexs_wifi = feature_cal(IQcomplex_wifi, n=signal_num, bins=fft_size)
    labels_wifi = np.zeros(len(center_freqs_wifi))
    # for index in indexs_wifi:
    #     labels_wifi[index] = 2
    # labels_wifi = np.array(labels_wifi)

    signals = np.empty((signal_num*2, 2, fft_size)) #complex is 2 parrt(real&imag)
    for i in range(signal_num):
        if (i + 1) % 1000 == 0:
            print('已解析 %d' % (i + 1) + '个')
        # signals[i] = np.array(struct.unpack_from(fmt_image, bin_data, offset)).reshape((num_rows, num_cols))
        if i < signal_num:
            signals[i][0] = IQcomplex_zigbee.real[i*1024:(i+1)*1024]
            signals[i][1] = IQcomplex_zigbee.imag[i*1024:(i+1)*1024]
        else:
            signals[i][0] = IQcomplex_wifi.real[i*1024:(i+1)*1024]
            signals[i][1] = IQcomplex_wifi.imag[i * 1024:(i + 1) * 1024]

    # signals = np.vstack(IQcomplex_zigbee,IQcomplex_wifi)

    labels = np.concatenate((labels_zigbee, labels_wifi))

    print(signals.shape)
    print(labels.shape)

    #remove bounary
    boundary = find_continuous_indexs((labels)) #this is the atart and end index of each zigbee tag
    while 0 in boundary:
        boundary.remove(0)
    signals = np.delete(signals, boundary, axis=0)
    labels = np.delete(labels, boundary, axis=0)
    # print(signals.shape)
    # print(labels.shape)

    file = open('Data/pickle_file/same_samples_mixed_signal_n'+ str(signals.shape[0]) + '_fft_size_' + str(fft_size) + '.pickle', 'wb')
    cPickle.dump(signals, file)
    file.close()

    file = open("Data/pickle_file/same_samples_mixed_signal_label_n"+str(labels.shape[0]) + '_fft_size_' + str(fft_size) +".pickle",'wb')
    cPickle.dump(labels,file)
    file.close()