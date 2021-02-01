import _pickle as cPickle
import os
import json
import numpy as np

from signal_seperator import load_indexs_snr


def add_indexfile():
    print(os.getcwd())
    os.chdir('1.13Exp_gain45')
    f = open("zigbee_snr.txt", 'r')
    jsonstr = f.read()
    indexdict_gain45 = json.loads(jsonstr)
    f.close()

    os.chdir('../1.13Exp_ch25')
    f = open("zigbee_snr.txt", 'r')
    jsonstr = f.read()
    indexdict_ch25 = json.loads(jsonstr)
    f.close()

    indexdict_gain45['ch25_pow3.dat'] = indexdict_ch25['telosb_only_ch25_gain45_pow3.dat']
    indexdict_gain45['ch25_pow13.dat'] = indexdict_ch25['telosb_only_ch25_gain45_pow13.dat']
    indexdict_gain45['ch25_pow23.dat'] = indexdict_ch25['telosb_only_ch25_gain45_pow23.dat']
    indexdict_gain45['ch25_pow8.dat'] = indexdict_ch25['telosb_only_ch25_gain45_pow8.dat']
    indexdict_gain45['ch25_pow18.dat'] = indexdict_ch25['telosb_only_ch25_gain45_pow18.dat']
    indexdict_gain45['ch25_pow28.dat'] = indexdict_ch25['telosb_only_ch25_gain45_pow28.dat']
    indexdict_gain45['ch25_pow31.dat'] = indexdict_ch25['telosb_only_ch25_gain45_pow31.dat']

    # 存到txt文件里
    os.chdir('../1.13Exp_gain45')
    file = open('zigbee_snr_full.txt', 'w')
    str = json.dumps(indexdict_gain45)
    file.write(str)

    return

def scan_pickles(filedir):
    os.chdir(filedir)
    mydir = os.getcwd()

    filelist = []
    for _, _, files in os.walk(mydir):
        #     print(files)
        for file in files:
            if os.path.splitext(file)[1] == '.pickle':
                filelist.append(file)
    return filelist;

def pickle_to_Xd(pickle_samples, fft_size, signal_num):
    if(len(pickle_samples)<signal_num):
        print('incompatible samples:'+ str(len(pickle_samples)))
        signal_num = len(pickle_samples)

    IQdata_sum = 0;
    for i in range(signal_num):
        IQdata_sum += len(pickle_samples[i])//fft_size
    signal = np.empty((IQdata_sum, 2, fft_size))

    IQdata_count = 0
    for i in range(signal_num):
        sample_count = len(pickle_samples[i])//fft_size
        for IQcount in range(sample_count):
            signal[IQdata_count][0] = pickle_samples[i].real[IQcount*fft_size:(IQcount+1)*fft_size]
            signal[IQdata_count][1] = pickle_samples[i].imag[IQcount*fft_size:(IQcount+1)*fft_size]
            IQdata_count += 1;
    return signal


def combine_pickle_data(filename):
    filelist = scan_pickles('./1.13Exp_gain45/pickle_file')
    # print(filelist)

    fft_size = 64;
    pickle_samples = cPickle.load(open('zigbeeonly_chch24__pow3_snr7.5597.pickle', 'rb'))
    # Xd = np.array(Xd)
    signals = pickle_to_Xd(pickle_samples, fft_size, 12)
    labels = np.ones(signals.shape[0]) * 2;

    #
    for file in filelist:
        # print(file[13:23].replace('__','_'))
        dictkey = file[13:23].replace('__','_')+'.dat'
        # indexs = load_indexs_snr('..',dictkey)
        # print(dictkey+': '+str(len(indexs)))
        if(dictkey=='ch24_pow3.dat' or dictkey=='ch26_pow3.dat'):
            continue                     #这俩dictkey的zigbee样本数只有13个与4个

        zigbee_num = 20; #所需的完整zigbee样本数量
        pickle_samples = cPickle.load(open(file, 'rb'))
        signal = pickle_to_Xd(pickle_samples, fft_size, zigbee_num)
        channel_num = int(dictkey[2:4])
        label = np.ones(signal.shape[0]) * (channel_num - 22)


        signals = np.append(signals,signal,axis=0)
        labels = np.append(labels,label, axis=0)

    print(signals.shape)
    print(labels.shape)
    file = open('mixed_signals.pickle', 'wb')
    cPickle.dump(signals, file)
    file.close()

    file = open('mixed_labels.pickle', 'wb')
    cPickle.dump(labels, file)
    file.close()

if __name__ == '__main__':
    # combine_pickle_data('')
    # add_indexfile()
    labels = cPickle.load(open('./1.13Exp_gain45/pickle_file/mixed_labels.pickle', 'rb'))

    print(labels)