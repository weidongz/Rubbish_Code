import numpy as np
import os
# import cPickle
# import _pickle as cPickle
# from plot_data import plot_IQ
# from feature_extraction import cal_mag,feature_cal

def load_data(size=1024, filename='1.13Exp_ch25/telosb_only_ch25_gain45_pow23.dat', n=10000):
    # load size*n IQdata
    IQdata = np.fromfile(filename, dtype="float32", count=size * 2 * n)
    # merge these data into complex form
    IQcomplex = map(complex, IQdata[0::2], IQdata[1::2])
    # change these data into complex type
    IQcomplex = np.array(list(IQcomplex), dtype=complex)

    #     IQdata =  IQcomplex.real,IQcomplex.imag
    return IQcomplex

def load_all_data(filename='1.13Exp_ch25/telosb_only_ch25_gain45_pow23.dat'):
    # load size*n IQdata
    IQdata = np.fromfile(filename, dtype="float32")
    # merge these data into complex form
    IQcomplex = map(complex, IQdata[0::2], IQdata[1::2])
    # change these data into complex type
    IQcomplex = np.array(list(IQcomplex), dtype=complex)

    #     IQdata =  IQcomplex.real,IQcomplex.imag
    return IQcomplex

def scanFile(filedir, filesuffix='.dat'):
    '''
    # Get all the data file from filedir to filelist
    遍历 filedir 获取所有后缀是.dat文件并存于filelist数组里
    :param filedir:文件名
    :return:
    '''
    os.chdir(filedir)
    mydir = os.getcwd()

    filelist = []
    for _,_,files in os.walk(mydir):
    #     print(files)
        for file in files:
            if os.path.splitext(file)[1] == filesuffix:
                filelist.append(file)

    return filelist