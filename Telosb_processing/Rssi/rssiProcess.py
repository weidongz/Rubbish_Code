#!usr/bin/python

import os
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

def scanFile():
    # Get all the data file in filelist
    os.chdir('.')
    mydir = os.getcwd()

    filelist = []
    for _,_,files in os.walk(mydir):
    #     print(files)
        for file in files:
            if os.path.splitext(file)[1] == '.dat':
                filelist.append(file)

    return filelist

def count_rssi(filename):
    # open file
    with open(filename) as fr:
        # read file
        arrayOlines = fr.readlines()
        # data num
        numberOfLines = len(arrayOlines)

    # most common word list and appearence
    commonword_num = []
    RssiList = []
    # read every line
    for line in arrayOlines:
        line = line.strip()
        listFromLine = line.split(' ')
        # get the most common Rssi Value in each packet
        temp_commonword = Counter(listFromLine).most_common()[0]
        commonword_num.append(temp_commonword)
        # compute Rssi Value and add it to list
        intRssi = int(temp_commonword[0], 16)
        Rssi = intRssi - 255 - 45 if intRssi > 127 else intRssi - 45
        RssiList.append(Rssi)

    print('{0}:{1}'.format(filename, RssiList));
    print('{0}: Rssi Value,total number: {1}'.format(filename, Counter(RssiList).most_common()))

    # print('{0}:'.format(filename));
    return RssiList

# count_rssi('with_telosb_outside_right_20m_7.31.dat')

def calAvgRssi(filename):
#     RssiList = count_rssi('with_telosb_chamber_0.1m.dat')
    RssiList = count_rssi(filename)
    RssiCounter = Counter(RssiList).most_common()
    RssiCounter[0][0]
    len(RssiCounter)
    RssiTotalValue = 0
    RssiTotalNum = 0
    for index in range(3):
        RssiTotalValue += RssiCounter[index][0]*RssiCounter[index][1]
        RssiTotalNum += RssiCounter[index][1]
    RssiAvgValue = RssiTotalValue/RssiTotalNum
#     print(RssiAvgValue)#np.floor(RssiAvgValue)
    print(np.rint(RssiAvgValue))

def plot_rssi(filename):
    # open file
    with open(filename) as fr:
        # read file
        arrayOlines = fr.readlines()
        # data num
        numberOfLines = len(arrayOlines)

    # most common word list and appearence
    commonword_num = []
    RssiList = []
    # read every line
    for line in arrayOlines:
        line = line.strip()
        listFromLine = line.split(' ')
        # get the most common Rssi Value in each packet
        temp_commonword = Counter(listFromLine).most_common()[0]
        commonword_num.append(temp_commonword)
        # compute Rssi Value and add it to list
        intRssi = int(temp_commonword[0], 16)
        Rssi = intRssi - 255 - 45 if intRssi > 127 else intRssi - 45
        RssiList.append(Rssi)

    # print('{0}: Rssi Value,total number: {1}'.format(filename, Counter(RssiList).most_common()))
    plt.plot(range(numberOfLines),RssiList)
    plt.title(filename)
    plt.show()

    # return RssiList


if __name__ == '__main__':
    filelist = scanFile();
    for file in filelist:
        calAvgRssi(file)
        plot_rssi(file)

    # plot_rssi("withtelosb.dat")
