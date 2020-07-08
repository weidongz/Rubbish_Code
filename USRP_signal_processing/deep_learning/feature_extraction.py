import numpy as np
import matplotlib.mlab as mlab
import scipy.signal
import scipy.interpolate
import scipy.ndimage

def cal_mag(IQcomplex, fft_size=1024):
    #     fft_size = 1024
    IQcomplex_1024 = np.asarray(IQcomplex[0:fft_size])
    # 加窗，不然频谱现象不明显
    result, windowVal = mlab.apply_window(IQcomplex_1024, window=mlab.window_hanning, axis=0, return_window=True)
    # 进行fft
    result = np.fft.fft(result, n=fft_size)
    # 参数1：FFT点数，参数2：采样周期，即1/采样频率
    freqs = np.fft.fftfreq(fft_size, 1 / 25)

    # 以下代码的作用貌似是调整双边的位置
    freqcenter = fft_size // 2
    freqs = np.concatenate((freqs[freqcenter:], freqs[:freqcenter]))
    result = np.concatenate((result[freqcenter:], result[:freqcenter]), 0)

    # 貌似是归一化
    result = np.abs(result) / np.abs(windowVal).sum()
    # 加上中心频率
    Fc = 2433
    freqs += Fc
    # 取对数坐标
    spec = 20. * np.log10(result)
    return spec, freqs

def feature_cal(IQcomplex, n=1000, bins=1024):
    """
    find out whether it exists peak
    :param IQcomplex:
    :param n:
    :return: the center frequency of peaks and the indexs of the zigbee signal
    """
    center_freq = []
    bandwidth = []
    for index in range(n):
        IQcomplex_tmp = IQcomplex[index*bins:(index+1)*bins]
        mag, freqs = cal_mag(IQcomplex_tmp)
        mag_smooth = scipy.signal.savgol_filter(mag, 21, 3)
        indices = scipy.signal.find_peaks(mag_smooth, threshold=0.1, height=-60)[0]
        if len(indices) != 0:
            center_freq.extend([sum(freqs[indices]) / len(indices)])
            bandwidth.append(freqs[indices[-1]] - freqs[indices[0]])
        else:
            center_freq.extend([0])
            bandwidth.append(0)
    indexs = []
    for index, value in enumerate(center_freq):
        if value > 0:
            # if bandwidth[index] < 10:
                indexs.append(index)
    # print("索引："+ str(indexs))

    return center_freq, bandwidth, indexs

def find_continuous_indexs(result):
    """
    this function is used for find out the continuous num of indexs
    :param indexs: the continuous label list
    :return: the start and end element of each continuous list
    """
    indexs = []
    for index, value in enumerate(result):
        if value > 0:
            indexs.append(index)
    tnum = []
    tnum.append(indexs[0])
    for index in range(len(indexs) - 1):
        if indexs[index + 1] - indexs[index] == 1:
            continue
        else:
            tnum.append(indexs[index])
            tnum.append(0)
            tnum.append(indexs[index + 1])
    tnum.append(indexs[-1])
    data_index = map(lambda x,y: x-y, tnum[1::3], tnum[0::3])
    null_index = map(lambda x,y: x-y, tnum[3::3], tnum[1::3])
    # print('the original continuous index are ' + str(list(tnum)))
    # print('zigbee signal duration index is ' + str(list(data_index)))
    # print('the gap betwwen zigbee signal is ' + str(list(null_index)))

    def find_continuous_indexs_lessthan25(x,y):
        if(x - y < 25):
            return y,x
        else:
            return
    data_index_lessthan25 = map(find_continuous_indexs_lessthan25, tnum[1::3], tnum[0::3])

    data_index_lessthan25 = list(data_index_lessthan25)
    while None in data_index_lessthan25:
        data_index_lessthan25.remove(None)
    # print('zigbee signal duration index less then 25 is ' + str(data_index_lessthan25))

    return tnum