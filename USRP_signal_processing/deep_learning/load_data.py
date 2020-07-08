import numpy as np
# import cPickle
# import _pickle as cPickle
# from plot_data import plot_IQ
from feature_extraction import cal_mag,feature_cal

def load_zigbee_25M_data(size=1024, n=1000):
    # load size*n IQdata
    IQdata = np.fromfile('Data/usrp_25M_data_with_telosb.dat',dtype="float32",count=size*2*n)
    # merge these data into complex form
    IQcomplex = map(complex,IQdata[0::2],IQdata[1::2])
    # change these data into complex type
    IQcomplex = np.array(list(IQcomplex),dtype=complex)
    # save data
#     IQdata[index*1024*2:(index+1)*1024*2].tofile("./usrp_81us.dat")
    return IQcomplex

def load_wifi_25M_data(n=100):
    # load 1024*n IQdata
    IQdata = np.fromfile('Data/usrp_wifi_cf2433M_sr25M.dat',dtype="float32",count=1024*2*n)
    # merge these data into complex form
    IQcomplex = map(complex,IQdata[0::2],IQdata[1::2])
    # change these data into complex type
    IQcomplex = np.array(list(IQcomplex),dtype=complex)
    return IQcomplex


def load_data(size=1024, filename='9.11usrp_zigbeeonwifi_rxgain10.dat', n=10000):
    # load size*n IQdata
    IQdata = np.fromfile(filename, dtype="float32", count=size * 2 * n)
    # merge these data into complex form
    IQcomplex = map(complex, IQdata[0::2], IQdata[1::2])
    # change these data into complex type
    IQcomplex = np.array(list(IQcomplex), dtype=complex)

    #     IQdata =  IQcomplex.real,IQcomplex.imag
    return IQcomplex

