# [George's Blog](http://zhua0404.blogspot.com/)

[NS3 tutorial (1) - NS3 installation in Ubuntu 12.04](http://zhua0404.blogspot.com/2014/07/ns3-tutorial-1-ns3-installation-in.html)

[Documentation](https://www.nsnam.org/releases/ns-3-30/documentation/)

[API Ref](https://www.nsnam.org/doxygen/group__lr-wpan.html)

```./waf --run hello-simulator```

```./waf --run first```

```./waf --pyrun ./examples/tutorial/first.py```

> https://ixs.im/Note/NS3/
>
> 如果visualizer模块没有编译，需在http://code.nsnam.org/gjc/ns-3.9-pyviz/下载pyviz软件包，解压后放在/NS3_install/ns-allinone-3.28/ns-3.28/目录下，再需重新编译如下命令：
>
> $ ./waf clean
>
> $ ./waf –build-profile=optimized–enable-examples –enable-tests configure

把自己修改编写的代码放进scratch文件夹里，由于wscript执行文件搜索路径包含scratch，故用户编写的程序均应当放入其中方可正常运行

修改logging日志输出等级以及各函数调用情况以及各事件发生时间

```bash
export 'NS_LOG=UdpEchoClientApplication=level_function|prefix_func|prefix_time:UdpEchoServerApplication=level_all|prefix_func|prefix_time'
```

```
# 在myfirst.cc中添加自定义变量
uint32_t nPackets = 2;
cmd.AddValue("nPackets", "Number of PAckets to echo", nPackets);
# 在命令行中查看是否存在自定义变量
./waf --run "myfirst --PrintHelp"
# 在命令行中使用自定义变量
./waf --run "myfirst --nPackets=5"
```

运行PyViz ``` ./waf --run first --vis```



ZigBee Simulation in NS3: 

[API of the IEEE 802.15.4-related models.](https://www.nsnam.org/doxygen/group__lr-wpan.html)

[NS3 for WSN](http://ns3simulation.com/ns3-for-wsn/)

[工业级无线传感器网络源码](https://github.com/ggmessier/ns3-isa100.11a/tree/e2c05c7e5679d96864849284979ef1ee93acc97a)





---

NodeContainer : 节点类，负责创建计算机

PointToPointHelper： 创建网卡和信道，把网卡连接到节点，设置信道

NetdeviceContainer： 网络设备类，即带有网卡的计算机

InternetStackHelper： 给node安装安装协议

Ipv4AddressHelper： 分配IP地址

Ipv4InterfaceContainer：关联IP地址到设备

UdpEchoServerHelper： 设置端口号

ApplicationContainer： UdpEchoServerHelper安装UdpEchoServerApplication到Node上，返回的容器



Inns-3, nodes can have multiple WifiNetDevices on separate channels, and the WifiNetDevice can coexist with otherdevice types. With the use of theSpectrumWifiPhyframework, one can also build scenarios involving cross-channelinterference or multiple wireless technologies on a single channel.

