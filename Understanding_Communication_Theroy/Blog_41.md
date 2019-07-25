# 深入浅出通信原理Python代码版

> 深入浅出通信原理是陈爱军的心血之作，于[通信人家园](http://www.txrjy.com/thread-394879-1-4.html)连载，此处仅作python代码笔记训练所用
> 陈老师的连载从多项式乘法讲起，一步一步引出卷积、傅立叶级数展开、旋转向量、三维频谱、IQ调制、数字调制等一系列通信原理知识

[TOC]

## 码元(Symbol)详解

> 码元，对应英文Symbol，又称符号
>
> 维基百科：持续一段固定时间的通信信道有效状态就是码元
>
> 陈老师解释：在通信信道中持续固定时间，具有一定相位或者幅值的一段余弦载波
>
> 网友：在信道(空中或电缆中）码元或者符号就是持续一定（某个）时间，具有一定（某个）幅度和一定（某个）相位的正弦波。
>
> BPSK码元有2种(0,$\pi$)，QPSK码元有4种，16QAM有16种码元。
>
> 设某数字调制对应码元有N种，则每个码元承载的比特数有$log_2N$个
>
> 但调制效率愈高，抗干扰能力愈差，对信道质量要求愈高



## BPSK旋转向量理解

详见连载44-46

> 旋转向量在实轴上的投影就是BPSK调制后的信号，初始相位是0或者pi，但最后相位不一定落在相位0或者pi上

接收到的是个实信号，但可以分解成两者旋转向量之和：
$$
s(t)=\cos\omega_0t=Re\{e^{j\omega_0t} \}=\frac{1}{2}(e^{jw_0t}+e^{-jw_0t})
$$
此时乘上初始位置在实轴，顺时针旋转且旋转角速度是w0的单位旋转向量$e^{-jw_0t}$
$$
2s(t)e^{-jw_0t}=1+2e^{-jw_0t}
$$
通过低通滤波器或积分器便解调出1，即发送端发送的是-1

![BPSK积分解调](http://download.txrjy.com/forum/month_1006/20100601_5ec2be221143b7a8cb9asu6ES6mrlc7Q.jpg)

![复数运算实现BPSK](http://download.txrjy.com/forum/month_1008/20100828_26a169d237f2915fd3a6kIuFxZWV4G6M.jpg)

![实数运算实现BPSK](http://download.txrjy.com/forum/month_1008/20100828_38b1b96bffb46b39d951TAL2vS00Bxin.jpg)

## PSK=映射+调制

![常规PSK调制解调框图](http://download.txrjy.com/forum/month_1006/20100606_effbc769e7fc73ecd52eIyiYZ3uD9c7S.jpg)

