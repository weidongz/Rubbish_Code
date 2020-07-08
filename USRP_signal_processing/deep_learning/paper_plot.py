import matplotlib.pyplot as plt
import numpy as np
from plot_data import plot_one_image_spectrum
from load_data import load_data
from matplotlib.ticker import FuncFormatter

def plot_acc_diff_length():
    fft_size = [1024, 512, 256, 128, 64]
    acc = [0.99917, 0.9994175946659705, 0.9995079679074578, 0.999892054183779, 0.9999353580286584]
    acc  = [ i*100 for i in acc]

    acc_same_length = [0.999949772721565, 0.9999748863607826 , 0.9999372159019564, 0.9998869886235214, 0.9996986363293905]
    acc_same_length = [ i*100 for i in acc_same_length]

    # extracts the first element of the list into l1 using tuple
    # unpacking.  So l1 is a Line2D instance, not a sequence of lines
    f = plt.figure(figsize=(11,6.8))
    # fig, ax = plt.subplots()
    ax = f.add_subplot(111)
    l1, = ax.plot(fft_size, acc,  'bs')
    l2, = ax.plot(fft_size, acc_same_length, 'ro')
    l3 = ax.plot(fft_size, acc, fft_size, acc_same_length)

    m_fontsize = 20
    ax.legend((l1, l2), ('same samples', 'different samples'), loc='lower left', shadow=True, fontsize=m_fontsize)
    ax.set_xlabel("Sample length ", fontsize=m_fontsize)
    ax.set_ylabel("Accuracy %", fontsize=m_fontsize)
    # new_ticks = np.linspace(-1, 2, 5)
    plt.xticks(fft_size, fontsize=m_fontsize)
    plt.yticks(fontsize=m_fontsize)

    # plt.savefig("pgf_fonts.pdf")
    plt.savefig("paper_images/plot_acc_diff_length.png")
    plt.show()

def plot_timeresponse():
    # fft_size = 64;
    fft_size = 1024;
    IQcomplex_zigbee = load_data(size=fft_size, filename='Data/usrp_25M_data_with_telosb.dat', n=10000)
    Index = 100
    # plot_one_image_time(IQcomplex_zigbee, IQIndex=Index, bins=fft_size)
    plot_one_image_spectrum(IQcomplex_zigbee, IQIndex=Index, bins=fft_size)

def plot_time_box():
    # from matplotlib.patches import Polygon
    m_fontsize = 20

    fft_size = [1024, 512, 256, 128, 64]
    fft_size = fft_size[-1::-1] #转置

    # 64: 0.00032315354346534723, 0.0003260678396332039
    # 128:  0.0005723794561611414, 0.0005817068924001852
    # 256: 0.0011669603961846212
    # 512:  0.0024203322601410327
    # 1024: 0.004590647122918083
    time64 = np.array([70.2633906950527, 66.0730996763345, 66.34821899328992, 66.59867855188803, 67.26250116444116, 69.91776167686277, 67.09960365664244, 65.93476911974132 , 67.81385647795226, 69.88021669330575, 67.33789350324317, 65.7752744091286])
    time128 = np.array([133.3230000245894, 137.59388635403968, 136.9802275039043, 129.86699042541431,  132.94741546896034 , 137.25577493126949, 130.07946192115025, 144.581905628347, 136.17845454470233, 143.0790315193738])
    time256 = np.array([264.3420565190896, 273.7348887223368, 258.86989537366514, 255.5633951022021, 258.45619701645217, 267.04899863992716, 282.4256318287134 , 269.79024048778916, 267.2975361923501, 294.66128779809634])
    time512 = np.array([512.3421926639, 531.6030476500986, 512.2541785524583, 552.3163046236061,539.5804809755783,514.734147311652,542.2301281522078, 536.098554230828,  545.0907439474704, 526.9945378838695])
    time1024 = np.array([ 950.7592078440067, 957.4974321786736, 941.8932418413215, 947.6666130884632,  940.4524766733317, 935.7687302448135])
    # Making a 2-D array only works if all the columns are the
    # same length.  If they are not, then use a list instead.
    # This is actually more efficient because boxplot converts
    # a 2-D array into a list of vectors internally anyway.

    # Multiple box plots on one Axes
    fig, ax = plt.subplots()
    time_spread = [time64, time128, time256, time512, time1024]
    ax.boxplot(time_spread,vert=True, labels=fft_size)

    ax.set_xlabel("Sample length ", fontsize=m_fontsize)
    ax.set_ylabel("Time("+r"$\mu$"+"s)", fontsize=m_fontsize)
    plt.xticks(fontsize=m_fontsize) #坐标轴刻度
    plt.yticks(fontsize=m_fontsize)

    plt.savefig("paper_images/plot_timeresponse.png" ,bbox_inches='tight')
    plt.show()

def to_percent(temp, position):
    return '%1.0f'%(100*temp) + '%'

def plot_ns3_packetlength():
    # % PPR
    m_fontsize = 20
    x = np.arange(1500, 500, -100)
    Throughput_before = np.array(
        [9.47261, 8.95422, 8.63332, 8.35027, 7.81274, 7.42764, 6.94112, 6.40204, 5.81253, 5.19193])
    THroughput_after = np.array(
        [9.72462, 9.06398, 8.65367, 8.38214, 7.75956, 7.42764, 6.93693, 6.31558, 5.76952, 5.15441])
    PPR_before = np.array([378, 335, 338, 352, 406, 414, 411, 491, 513, 532]) / 1754
    PPR_after = np.array([746, 719, 753, 832, 760, 814, 856, 813, 877, 901]) / 1754
    fig, ax1 = plt.subplots()
    plt.xticks(fontsize=m_fontsize)
    plt.yticks(fontsize=m_fontsize)
    ax2 = ax1.twinx()
    ax1.plot(x, Throughput_before, 'r', linestyle='--', label="WiFi Throughput")
    ax1.plot(x, THroughput_after, 'rs-', label="After design")
    ax2.plot(x, PPR_before, 'b', linestyle='--', label="ZigBee PRR")
    ax2.plot(x, PPR_after, 'bo-',  label="After design")
    ax1.set_xlabel('WiFi Packet Length(byte)', fontsize=m_fontsize)
    ax1.set_ylabel('WiFi Throughput(Mbps)', color='r', fontsize=m_fontsize)
    ax2.set_ylabel('ZigBee PRR', color='b', fontsize=m_fontsize)
    # ax2.set_xlabel(fontsize=m_fontsize)
    ax2.yaxis.set_major_formatter(FuncFormatter(to_percent))
    ax1.legend(loc='center left', fontsize=14)
    ax2.legend(loc='center right', fontsize=14)
    # ax1.set_xticks(fontsize=m_fontsize)
    # plt.tick_params(labelsize=20)
    plt.yticks(fontsize=m_fontsize)
    plt.savefig('paper_images/Packet_Length_Performance.png', bbox_inches='tight')
    plt.show()

def plot_ns3_wifipower():
    # Power
    m_fontsize = 20
    power = np.arange(20, 11, -2)
    Throughput_before = np.array([20.144, 20.144, 20.144, 20.1393, 18.2198])
    THroughput_after = np.array([12.2941, 12.2941, 12.2941, 12.2941, 11.9785])
    PPR_before = np.array([367, 369, 378, 388, 400]) / 1754
    PPR_after = np.array([709, 709, 709, 709, 709]) / 1754
    fig, ax1 = plt.subplots()
    plt.xticks(fontsize=m_fontsize)
    plt.yticks(fontsize=m_fontsize)
    ax2 = ax1.twinx()
    ax1.plot(power, Throughput_before, 'rs', linestyle='--',label="WiFi Throughput")
    ax1.plot(power, THroughput_after, 'rs-',  label="After design")
    ax2.plot(power, PPR_before, 'bo', linestyle='--', label="ZigBee PRR")
    ax2.plot(power, PPR_after, 'bo-',  label="After design")
    ax1.set_xlabel('WiFi transmit Power (dBm)',fontsize=m_fontsize)
    ax1.set_ylabel('WiFi Throughput(Mbps)', color='r',fontsize=m_fontsize)
    ax2.set_ylabel('ZigBee PRR', color='b',fontsize=m_fontsize)
    ax2.set_ylim((0.15, 0.45))
    ax2.yaxis.set_major_formatter(FuncFormatter(to_percent))
    ax1.legend(loc='center left')
    ax2.legend(loc='center right')
    plt.yticks(fontsize=m_fontsize)
    plt.savefig('paper_images/Power_Performance.png', bbox_inches='tight')
    plt.show()

def plot_ns3_datarate():
    m_fontsize = 20
    data_rate = np.array([12, 18, 24, 36, 48, 54])
    Throughput_before = np.array([8.533505, 11.1189, 13.3882, 12.6757, 8.91679, 9.47261])
    THroughput_after = np.array([6.04109, 7.46834, 8.59177, 9.39725, 9.39725, 9.72462])
    PPR_before = np.array([150, 137, 48, 341, 385, 378]) / 1754
    PPR_after = np.array([262, 351, 508, 612, 647, 746]) / 1754
    fig, ax1 = plt.subplots()
    plt.xticks([12, 18, 24, 36, 48, 54], fontsize=m_fontsize)
    plt.yticks(fontsize=m_fontsize)
    ax2 = ax1.twinx()
    ax1.plot(data_rate, Throughput_before, 'r', linestyle='--', label="WiFi Throughput")
    ax1.plot(data_rate, THroughput_after, 'rs-', label="After design")
    ax2.plot(data_rate, PPR_before, 'b', linestyle='--', label="ZigBee PRR")
    ax2.plot(data_rate, PPR_after, 'bo-', label="After design")
    ax1.set_xlabel('WiFi data rate (Mbps)', fontsize=m_fontsize)
    ax1.set_ylabel('WiFi Throughput(Mbps)', color='r', fontsize=m_fontsize)
    ax2.set_ylabel('ZigBee PRR', color='b',fontsize=m_fontsize)
    # ax2.set_ylim((0.15,0.45))
    ax2.yaxis.set_major_formatter(FuncFormatter(to_percent))
    ax1.legend(loc='upper left')
    ax2.legend(loc='lower right')
    plt.yticks(fontsize=m_fontsize)
    plt.savefig('paper_images/Data_Rate_Performance.png', bbox_inches='tight')
    plt.show()

def sim_zigbeeDistance():
    m_fontsize = 20
    distance_z = np.array([2,3,4,5,6])
    PRR_before = np.array([1754, 1511, 526, 378, 378]) / 1754
    PPR_after = np.array([1754, 1741, 795, 746, 684]) / 1754
    plt.plot(distance_z, PRR_before,  'bs:', label = "Original PRR")
    plt.plot(distance_z, PPR_after, 'ro-', label = "After design")
    # plt.legend((l1, l2), ('same samples', 'different samples'), loc='lower left', shadow=True, fontsize=m_fontsize)
    plt.xlabel("distance (m) ", fontsize=m_fontsize)
    plt.ylabel("ZigBee PPR", fontsize=m_fontsize)
    # new_ticks = np.linspace(-1, 2, 5)
    plt.xticks(distance_z, fontsize=m_fontsize)
    plt.yticks(fontsize=m_fontsize)
    plt.legend(fontsize=m_fontsize)
    # plt.savefig("pgf_fonts.pdf")
    plt.savefig('paper_images/zigbeedistance_performance.png', bbox_inches='tight')
    plt.show()

def sim_wifizigbeeDistance():
    m_fontsize = 20
    distance_wz = np.array([2,3,4,5,6])
    Throughput_before = np.array([9.06045, 9.14995, 9.19235, 9.1476, 9.1476])
    THroughput_after = np.array([0.0070656,9.31482,9.29126, 9.29126, 9.29126 ])
    PPR_before = np.array([686, 347, 361, 378, 378]) / 1754
    PPR_after = np.array([1719, 704, 684, 746, 793]) / 1754
    fig, ax1 = plt.subplots()
    plt.xticks(distance_wz, fontsize=m_fontsize)
    plt.yticks(fontsize=m_fontsize)
    ax2 = ax1.twinx()
    ax1.plot(distance_wz, Throughput_before, 'r', linestyle='--', label="WiFi Throughput")
    ax1.plot(distance_wz, THroughput_after, 'rs-', label="After design")
    ax2.plot(distance_wz, PPR_before, 'b', linestyle='--', label="ZigBee PRR")
    ax2.plot(distance_wz, PPR_after, 'bo-', label="After design")
    ax1.set_xlabel('Distance between WiFi&ZigBee (m)', fontsize=m_fontsize)
    ax1.set_ylabel('WiFi Throughput(Mbps)', color='r', fontsize=m_fontsize)
    ax2.set_ylabel('ZigBee PRR', color='b',fontsize=m_fontsize)
    # ax2.set_ylim((0.15,0.45))
    ax2.yaxis.set_major_formatter(FuncFormatter(to_percent))
    ax1.legend(loc='center left')
    ax2.legend(loc='center right')
    plt.yticks(fontsize=m_fontsize)
    plt.savefig('paper_images/wifi_zigbeedistance_performance.png', bbox_inches='tight')
    plt.show()


if __name__=='__main__':
    # plot_acc_diff_length();
    # plot_time_box()
    plot_ns3_packetlength()
    # plot_ns3_wifipower()
    # plot_ns3_datarate()
    # sim_zigbeeDistance()
    # sim_wifizigbeeDistance()