import numpy as np
import matplotlib.pyplot as plt
import json

import _pickle as cPickle
# try:
#     import cPickle as pickle
# except ImportError:
#     import pickle

import os
from load_data import load_all_data, scanFile, load_data
from calc_snr import calc_snr
from plot_data import plot_IQ,plot_IQ_timeseries

def signal_separation(IQSamples):
    # print(IQSamples.dtype)
    # 计算幅值
    mag = np.sqrt(IQSamples.real ** 2 + IQSamples.imag ** 2)

    # # 循环方式
    # n = IQSamples.size
    # n = n//10
    # mags = []
    # for i in range(n):
    #     mag_avg = np.average(mag[i*10:i*10+10])
    #     mags.append(mag_avg)
    #     mags
    # print(len(mags))
    # print(mag[0:20])

    # 使用numpy，每bins个点求一次均值
    bins = 10; #分辨率，若干个点求一次均值

    mag = np.resize(mag, (mag.size//bins, bins))
    # mag = mag.reshape(mag.size // bins, bins)
    mag = np.average(mag,axis=1)
    # print(len(mag))

    indexs = detect_by_threshold(mag);

    snr = get_snr(mag, indexs);

    # plt.plot(np.arange(0, len(mag)), mag)
    # plt.plot(range(0,len(mag)),mag)
    # plt.show()

    return indexs, snr

def detect_by_threshold(mag):
    # 每十个点求一个mag，根据mag的值，找出幅值的起始点与终点
    indexs = []
    flag = False #用于判断是否起始点
    for index, value in enumerate(mag):
        # threshold_dict = {'w3':0.01, 'w4':0.015, 'w5':0.011, 'w6':0.012}
        if value > 0.012:  #magnitude threshold:0.012
            if flag == False:
                flag = True
                if(len(indexs)>=1 and index-indexs[-1]<=10):
                    indexs.pop() #防止部分值不符合阈值
                else:
                    indexs.append(index)

        else:
            if flag == True:
                indexs.append(index)
                flag = False

    return indexs

def get_snr(mag, indexs):
    if len(indexs)==0:
        return -1
    zigbee_magnitude = (np.sum(mag[indexs[2]:indexs[3]]) / (indexs[3] - indexs[2]))
    noise_magnitude = (np.sum(mag[indexs[1]+10:indexs[2]-10]) / (indexs[2] - indexs[1]-20))
    snr = calc_snr(zigbee_magnitude,noise_magnitude);

    return snr

def zigbee_signal_extraction(IQSamples, indexs):
    # 列表形式存储，每个单元都是一整段ZigBee信号，如ZigBeeSamples[0]是一整段ZigBee信号包含30130个IQ点
    ZigBeeSamples = []

    for i in range(len(indexs)//2):
        ZigBeeSamples.append(IQSamples[indexs[i*2]*10 : indexs[i*2+1]*10])

    return ZigBeeSamples

def noise_extraction(IQSamples, indexs):

    IQSamples2 = IQSamples[(indexs[1]+5)*10: (indexs[2]-5)*10]

    return IQSamples2

def save_to_pickle():
    filelist = scanFile('./1.13Exp_gain45')
    for file in filelist:
        IQSamples = load_all_data(file)
        indexs, snr = signal_separation(IQSamples)
        if snr == -1:
            continue

        # 存到pickle文件里
        os.chdir('./pickle_file')
        # pathname = os.path.join(os.path.abspath('./pickle_file'), 'zigbeeonly_ch25_' + file[-9:-4] + '_snr' + str(
        #     snr)[0:6] + '.pickle')
        # print(os.getcwd())
        file = open('zigbeeonly_ch'+file[0:4]+'_' + file[-9:-4] + '_snr' + str(snr)[0:6] + '.pickle', 'wb')

        IQSamples = zigbee_signal_extraction(IQSamples, indexs)
        cPickle.dump(IQSamples, file)
        file.close()
        os.chdir('..')

    return;

def save_indexs(filedir):
    filelist = scanFile(filedir)
    snrdict = {}
    indexdict = {}

    for file in filelist:
        IQSamples = load_all_data(file)
        indexs, snr = signal_separation(IQSamples)
        indexdict[file] = indexs
        snrdict[file] = snr
        # if snr == -1:
        #     continue

    # 存到txt文件里
    file = open('zigbee_indexs.txt', 'w')
    str = json.dumps(indexdict)
    file.write(str)

    file = open('zigbee_snr.txt', 'w')
    str = json.dumps(snrdict)
    file.write(str)
    file.close()

    return;

def load_indexs_snr(filedir, filename):
    # os.chdir('./1.13Exp_ch25')
    os.chdir(filedir)
    try:
        f = open('zigbee_snr.txt', 'r')
        jsonstr = f.read()
        snrdict = json.loads(jsonstr)
        print('snr:',snrdict[filename])

        # jsonstr = jsonstr[1:-1]  # 去除括号
        # strs = jsonstr.split(',')

        f = open("zigbee_indexs.txt",'r')
        jsonstr = f.read()
        indexdict = json.loads(jsonstr)
        print('indexs:', indexdict[filename])
        return indexdict[filename]

    finally:
        if f:
            f.close()

if __name__ == '__main__':
    # IQSamples = load_all_data('./1.13Exp_ch25/telosb_only_ch25_gain45_pow31.dat')
    IQSamples = load_data(1024, './1.13Exp_ch25/telosb_only_ch25_gain45_pow6.dat', 1000)
    print(len(IQSamples))

    # save_to_pickle()

    # save_indexs('./1.13Exp_gain45')
    load_indexs_snr('./1.13Exp_ch25', 'telosb_only_ch25_gain45_pow6.dat')


    pass

