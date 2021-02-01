import matplotlib.pyplot as plt

from load_data import load_data, scanFile
import numpy as np
from feature_extraction import cal_mag, feature_cal
from feature_extraction import find_continuous_indexs
from calc_snr import calc_rssi

def plot_IQ(IQcomplex, IQIndex=0, bins=1024):
    """
    This function plot 10 figures, use IQIndex*100 us IQdata， 绘制频谱图
    :param IQcomplex:
    :param IQIndex: the index num of IQcomplex
    :return:
    """
    plt.figure(figsize=(6, 10))
    num = IQIndex
    for n in range(10):
        plt.subplot(5, 2, n + 1)
        IQcomplex_tmp = IQcomplex[(n + num) * bins:(n + 1 + num) * bins]
        mag, freqs = cal_mag(IQcomplex_tmp)
        plt.plot(freqs, mag)
    plt.show()
    return

def plot_one_image_spectrum(IQcomplex, IQIndex=0, bins=1024):
    '''
    绘制特定Index的频谱图
    :param IQcomplex:  样本集
    :param IQIndex:  所需绘制的图形样本点的index
    :param bins:  size
    :return:
    '''
    # plt.figure(figsize=(6, 10))
    num = IQIndex
    m_fontsize = 20

    IQcomplex_tmp = IQcomplex[(num) * bins:(1 + num) * bins]
    mag, freqs = cal_mag(IQcomplex_tmp)
    plt.plot(freqs, mag)
    plt.xlabel('Frequency(MHz)', fontsize=m_fontsize)
    plt.ylabel('Amplitude(dB)', fontsize=m_fontsize)
    plt.xticks(fontsize=m_fontsize)
    plt.yticks(fontsize=m_fontsize)
    plt.savefig("paper_images/plot_spectrum64.png", bbox_inches='tight')
    plt.show()
    return

def plot_one_image_time(IQcomplex, IQIndex=0, bins=64):
    '''
    绘制单张时域图
    :param IQcomplex:  样本集
    :param IQIndex:  index序号
    :param bins:
    :return:
    '''
    plt.figure(figsize=(6, 10))
    num = IQIndex

    Qcomplex_tmp_time = np.linspace(0, bins , bins)
    IQcomplex_tmp = IQcomplex[(num) * bins:(1 + num) * bins]
    mag = np.sqrt(IQcomplex_tmp.real ** 2 + IQcomplex_tmp.imag ** 2) #根号（I²+Q²）代表载波IQ信号的振幅
    plt.plot(Qcomplex_tmp_time, mag)
    plt.show()
    return

def plot_IQ_timeseries(IQcomplex, IQIndex=0, bins = 1024):
    '''
    绘制10张时域图
    :param IQcomplex:
    :param IQIndex:
    :param bins:
    :return:
    '''
    plt.figure(figsize=(6, 10))
    num = IQIndex
    for n in range(10):
        plt.subplot(5, 2, n + 1)
        # for time analysis

        IQcomplex_tmp_time = np.linspace(0, bins / 25, bins) #横坐标是时间
        IQcomplex_tmp = IQcomplex[(n + num) * bins:(n + 1 + num) * bins]
        # plot time IQ seperate
        #         plt.plot(IQcomplex_tmp_time,IQcomplex_tmp.real)
        #         plt.plot(IQcomplex_tmp_time,IQcomplex_tmp.imag)

        # plot energy
        #         IQcomplex_tmp_time = np.linspace(0, bins*2/25, bins)
        mag = np.sqrt(IQcomplex_tmp.real ** 2 + IQcomplex_tmp.imag ** 2)
        plt.plot(IQcomplex_tmp_time, mag)
        plt.xlabel('Time(us)')
    plt.show()
    return

def plot_IQ_timeseries2(IQcomplex, IQIndex=0, bins = 1024):
    plt.figure(figsize=(20, 20))
    num = IQIndex

        # for time analysis

    IQcomplex_tmp_time = np.linspace(0, bins / 25 *10, bins*10) #横坐标是时间
    IQcomplex_tmp = IQcomplex[(num) * bins:(10 + num) * bins]
    # plot time IQ seperate
    #         plt.plot(IQcomplex_tmp_time,IQcomplex_tmp.real)
    #         plt.plot(IQcomplex_tmp_time,IQcomplex_tmp.imag)

    # plot energy
    #         IQcomplex_tmp_time = np.linspace(0, bins*2/25, bins)
    mag = np.sqrt(IQcomplex_tmp.real ** 2 + IQcomplex_tmp.imag ** 2)
    plt.plot(IQcomplex_tmp_time, mag)
    plt.xlabel('Time(us)')
    plt.show()
    return

def plot_IQ_timeseries3(IQcomplex, filename='', IQIndex=0, bins = 1024):
    '''
    绘制长达10ms的时域图
    :param IQcomplex:
    :param IQIndex:
    :param bins:
    :return:
    '''
    plt.figure(figsize=(20, 20))
    num = IQIndex
    factor = 100

        # for time analysis

    IQcomplex_tmp_time = np.linspace(0, bins / 20 * factor*10, bins * factor*10) #横坐标是时间
    IQcomplex_tmp = IQcomplex[(num) * bins:(10*factor + num) * bins]
    # plot time IQ seperate
    #         plt.plot(IQcomplex_tmp_time,IQcomplex_tmp.real)
    #         plt.plot(IQcomplex_tmp_time,IQcomplex_tmp.imag)

    # plot energy
    #         IQcomplex_tmp_time = np.linspace(0, bins*2/25, bins)
    mag = np.sqrt(IQcomplex_tmp.real ** 2 + IQcomplex_tmp.imag ** 2)
    plt.plot(IQcomplex_tmp_time, mag)
    plt.xlabel('Time(us)')
    plt.title(filename)
    plt.show()
    return

def plot_file_timeseries(filelist, startIndex=0, endIndex = 10):
    '''
    绘制filelist的10张时域图
    :param IQcomplex:
    :param IQIndex:
    :param bins:
    :return:
    '''
    # plt.figure(figsize=(6, 10))
    num = 0
    bins = 1024
    filelist = filelist[startIndex: endIndex]
    for n in range(10):
    # for thisfile in filelist:
        plt.subplot(5, 2, num + 1)
        # for time analysis
        thisfile = "telosb_only_ch25_gain45_pow"+ str(num+21) +".dat"
        factor = 100
        IQcomplex_tmp_time = np.linspace(0, bins / 20 * factor * 10, bins * factor * 10)  # 横坐标是时间
        IQcomplex= load_data(size=bins, filename=thisfile,
                                          n=1000)
        IQcomplex_tmp = IQcomplex[(0) * bins:(10 * factor + 0) * bins]
        # plot time IQ seperate
        #         plt.plot(IQcomplex_tmp_time,IQcomplex_tmp.real)
        #         plt.plot(IQcomplex_tmp_time,IQcomplex_tmp.imag)

        # plot energy
        #         IQcomplex_tmp_time = np.linspace(0, bins*2/25, bins)
        mag = np.sqrt(IQcomplex_tmp.real ** 2 + IQcomplex_tmp.imag ** 2)

        plt.title(thisfile[-9:-4])
        plt.plot(IQcomplex_tmp_time, mag)
        # plt.xlabel('Time(us)')

        num = num+1

    plt.show()
    return

def plot_IQ_time_spectrum(IQcomplex, SpecificIndex, bins):
    '''
    绘制单张特定Index时频图
    :param IQcomplex: 样本集
    :param SpecificIndex:  指定Index
    :param bins:
    :return:
    '''
    n = SpecificIndex
    plt.subplot(121)
    # bins = 1024
    IQcomplex_tmp = IQcomplex[(n) * bins:(n + 1) * bins]
    mag, freqs = cal_mag(IQcomplex_tmp)
    plt.plot(freqs, mag)
    plt.xlabel('Freq(MHz)')

    plt.subplot(122)

    IQcomplex_tmp_time = np.linspace(0, bins / 20, bins)
    mag = np.sqrt(IQcomplex_tmp.real ** 2 + IQcomplex_tmp.imag ** 2)
    plt.plot(IQcomplex_tmp_time, mag)
    plt.xlabel('Time(us)')
    plt.tight_layout()

    plt.show()
    return

def plot_file_time(filelist, startIndex=0, endIndex = 10):
    '''
    绘制filelist的10张时域图
    :param IQcomplex:
    :param IQIndex:
    :param bins:
    :return:
    '''
    # plt.figure(figsize=(6, 10))
    num = 0
    bins = 1024
    filelist = filelist[startIndex: endIndex]
    # for n in range(10):
    for thisfile in filelist:
        plt.subplot(5, 2, num + 1)
        # for time analysis
        # thisfile = "telosb_only_ch25_gain45_pow"+ str(num+21) +".dat"
        factor = 100
        IQcomplex_tmp_time = np.linspace(0, bins / 20 * factor * 10, bins * factor * 10)  # 横坐标是时间
        IQcomplex= load_data(size=bins, filename=thisfile,
                                          n=1000)
        IQcomplex_tmp = IQcomplex[(0) * bins:(10 * factor + 0) * bins]

        mag = np.sqrt(IQcomplex_tmp.real ** 2 + IQcomplex_tmp.imag ** 2)

        plt.title(thisfile[:-4])
        plt.plot(IQcomplex_tmp_time, mag)
        # plt.xlabel('Time(us)')

        num = num+1

    plt.show()
    return

def print_file_snr(filelist):
    '''
    打印指定文件夹的
    :param filelist:
    :return:
    '''
    fft_size = 1024;

    for file in filelist:
        IQcomplex_only_zigbee = load_data(size=fft_size, filename=file,
                                          n=1000)
        center_freqs_only_zigbee, bandwidths_only_zigbee, indexs_only_zigbee = feature_cal(
            IQcomplex_only_zigbee, n=1000, bins=fft_size)

        print('\n',file,':')
        if(len(indexs_only_zigbee) and indexs_only_zigbee[0]>5):
            calc_rssi(IQcomplex_only_zigbee, indexs_only_zigbee[0] - 5, indexs_only_zigbee[2])
            # plot_IQ_timeseries3(IQcomplex_only_zigbee,file)
        elif(len(indexs_only_zigbee)):
            calc_rssi(IQcomplex_only_zigbee, 30, indexs_only_zigbee[2])
        else:
            print(indexs_only_zigbee)

def analysis_one_file(filename):
    fft_size = 1024;
    IQcomplex_only_zigbee = load_data(size=fft_size, filename=filename, n=1000)

    Index = 10;

    plot_IQ(IQcomplex_only_zigbee, IQIndex=Index, bins=fft_size)
    plot_IQ_timeseries(IQcomplex_only_zigbee, Index, fft_size)
    # plot_IQ_time_spectrum(IQcomplex=IQcomplex_wifi_with_zigbee, SpecificIndex=Index, bins=fft_size)

    center_freqs_only_zigbee, bandwidths_only_zigbee, indexs_only_zigbee = feature_cal(
        IQcomplex_only_zigbee, n=1000, bins=fft_size)

    feature_only_zigbee = np.array([center_freqs_only_zigbee, bandwidths_only_zigbee])

    print(indexs_only_zigbee)
    # print(center_freqs_wifi_with_zigbee)
    print('信号带宽',bandwidths_only_zigbee[indexs_only_zigbee[1]])

    calc_rssi(IQcomplex_only_zigbee, indexs_only_zigbee[0]-5, indexs_only_zigbee[2])

    plot_IQ_timeseries3(IQcomplex_only_zigbee)


if __name__=='__main__':
    # filelist = scanFile('./1.13Exp_ch25')
    # filelist = scanFile("./1.13Exp_gain45")

    # plot_file_timeseries(filelist,0,10)

    # print_file_snr(filelist)

    # plot_file_time(filelist,20,30)

    # analysis_one_file('./1.13Exp_ch25/telosb_only_ch25_gain45_pow31.dat')
    analysis_one_file('./1.13Exp_gain45/ch23_pow3.dat')








