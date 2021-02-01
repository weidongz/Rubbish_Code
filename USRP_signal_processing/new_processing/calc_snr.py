import numpy as np

def calc_snr(sig_amp, noise_amp):
    '''
    SNR = 10log_10(P_signal/P_noise) = 20lg(A_sig/A_noise)
    :param sig_amp: 信号功率
    :param noise_amp: 噪声功率
    :return: SNR（dB），单位是分贝
    '''
    snr = 20 * np.log10(sig_amp/noise_amp)
    return snr

def calc_rssi(IQcomplex, index1, index2):
    '''
    该函数用于计算rssi
    :param IQcomplex: 样本集
    :param index1: 1024个样本点中噪声信号索引
    :param index2: zigbee信号索引, 1024个样本点
    :return: rssi值
    '''
    bins = 1024
    IQcomplex_noise = IQcomplex[(index1) * bins:(index1 + 1) * bins]
    IQcomplex_zigbee = IQcomplex[(index2) * bins:(index2 + 1) * bins]

    mag_noise = np.sqrt(IQcomplex_noise.real ** 2 + IQcomplex_noise.imag ** 2)      #根号（I²+Q²）代表载波IQ信号的振幅
    mag_zigbee = np.sqrt(IQcomplex_zigbee.real ** 2 + IQcomplex_zigbee.imag ** 2)
    mag_avg_noise = np.average(mag_noise)
    mag_avg_zigbee = np.average(mag_zigbee)
    print('noise mag: %f, zigbee mag:%f' %(mag_avg_noise, mag_avg_zigbee))

    snr = calc_snr(mag_avg_zigbee,mag_avg_noise)
    # rssi = mag_avg_zigbee/mag_avg_noise;
    print('zigbee magnitude:',mag_avg_zigbee,',noise mag:',mag_avg_noise,',snr',snr)
    return snr

def mW2dBm(mW):
    '''
    mW至dBm的转换函数 P(dBm) = 10 ⋅ log10( P(mW) / 1mW)
    :param mW: 毫瓦
    :return: dBm
    '''
    dBm = 10*np.log10(mW);
    return dBm

def dBm2mW(dBm):
    '''
    dBm至mW的转换函数 P(mW) = 1mW ⋅ 10(P(dBm)/ 10)
    :param dBm:
    :return:
    '''

    mW = pow(10,dBm/10)
    return mW



if __name__ == "__main__":
    print(mW2dBm(9))
    print(dBm2mW(0))
