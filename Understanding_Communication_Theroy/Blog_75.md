# 深入浅出通信原理Python代码版

> 深入浅出通信原理（http://www.txrjy.com/thread-394879-1-4.html）从2010年4月8日开始在C114通信人家园上线连载，从多项式乘法讲起，一步一步引出卷积、傅立叶级数展开、旋转向量、三维频谱、IQ调制、数字调制等一系列通信原理知识

[TOC]

## 傅里叶变换与反变换

Fourier Transform:
$$
X(f) = \int_{-\infty}^{+\infty}x(t)e^{-j2\pi ft}dt \\
X(\omega)= \int_{-\infty}^{+\infty}x(t)e^{-j\omega t}dt
$$
Fourier inverse Transform:
$$
x(t)=\int_{-\infty}^{+\infty}X(f)e^{j2\pi ft}df
$$

## 傅里叶变换性质

| 时域                  | 频域                 |
| --------------------- | -------------------- |
| $x(t)$                | $X(\omega)$          |
| $x(t)e^{j\omega_0t}$  | $X(\omega-\omega_0)$ |
| $x(t)e^{-j\omega_0t}$ | $X(\omega+\omega_0)$ |

> 信号x(t)在时域乘上$e^{j\omega_0t}$, 相当于频谱X(w)右移$\omega_0$;信号在时域乘上$e^{-j\omega_0t}$, 相当于频谱左移$\omega_0$;
>
> 信号x(t)调制载波$cos\omega_0t$, 相当于频谱X(w)一分为二并分别左移右移$w_0$
>
> ```python
> # coswt频谱搬移作用
> x = np.arange(-np.pi/2,np.pi/2,0.01)
> y = np.cos(x)
> 
> plt.plot(x,y,':')
> # y1 = np.cos(x-np.pi)/2
> plt.plot(x-3*np.pi,y/2,color='b')
> plt.plot(x+3*np.pi,y/2,color='b')
> plt.xticks([-3*np.pi,0,3*np.pi],['$-\omega_0$','0','$-omega_0$'])
> plt.yticks([1],['$X(\omega)$'])
> plt.show()
> ```
>
> ![coswt频谱搬移作用](http://ww1.sinaimg.cn/large/70815d51ly1g5i5i6nkfoj20ak06ymx5.jpg)
>
> ```python
> # 矩形脉冲调制余弦载波
> # 矩形脉冲
> # x = np.arange(-1.5,1.5,0.1)
> # y = [0 for x in x if x <= -0.5]
> # y.extend([1 for x in x  if x>-0.5 and x<=0.5])
> # y.extend([0 for x in x  if x>0.5])
> # plt.plot(x,y)
> plt.subplot(3,2,1)
> x = [-1.5,-0.5,0.5,1.5]
> y = [0,1,0,0]
> plt.plot(x,y,drawstyle='steps-post')
> 
> # cos(2\pi*5t),5Hz
> plt.subplot(3,2,3)
> x = np.arange(-1.5,1.6,0.1)
> y = np.cos(2*np.pi*5*x)
> plt.plot(x,y)
> 
> # time zone modulation
> plt.subplot(3,2,5)
> y = [0 for x in x if x <= -0.4]
> y.extend([ np.cos(2*np.pi*5*x) for x in x  if x>=-0.5 and x<=0.6])
> y.extend([0 for x in x  if x>=0.5])
> x = np.sort(np.append(x,[0.5,-0.5]))
> plt.plot(x,y)
> plt.plot()
> 
> # 矩形脉冲 Spectrum
> plt.subplot(3,2,2)
> f = np.arange(-4,4,0.1)
> y = np.sinc(f)
> plt.plot(f,y)
> 
> # cos wave spectrum
> plt.subplot(3,2,4)
> f = [-5,5]
> y = [0.5,0.5]
> plt.stem(f,y)
> 
> # modulation Spectrum
> plt.subplot(3,2,6)
> f = np.arange(-10,10,0.1)
> X = 0.5*np.sinc(f-5)+0.5*np.sinc(f+5)
> plt.plot(f,X)
> 
> plt.tight_layout()
> plt.show()
> ```
>
> ![矩形脉冲调制余弦载波](http://ww1.sinaimg.cn/large/70815d51ly1g5i5jcxf1bj20br07sdg7.jpg)
>
> 无论信号经过多少处理，最终都会被转换成一连串脉冲（如矩形脉冲），再调制到载波发射出去

## 正脉冲与负脉冲的幅度谱和相位谱

```python
# 正脉冲与负脉冲的幅度谱和相位谱
f = np.arange(-4,4,0.1)
plt.subplot(3,2,1)
X = abs(np.sinc(f))
plt.plot(f,X)
plt.title('postive pulse magnitude')

plt.subplot(3,2,3)
f = np.arange(-4,5,1)
P = [np.pi,0,np.pi,0,0,-np.pi,0,-np.pi,0]
plt.plot(f,P,drawstyle='steps-post')
plt.title('postive pulse phase')

f = np.arange(-4,4,0.1)
plt.subplot(3,2,2)
X = abs(-np.sinc(f))
plt.plot(f,X)
plt.title('negative pulse magnitude')

plt.subplot(3,2,4)
f = np.arange(-4,5,1)
P = [0,np.pi,0,np.pi,-np.pi,0,-np.pi,0,-np.pi]
plt.plot(f,P,drawstyle='steps-post')
plt.title('negative pulse phase')

plt.subplot(3,2,5)
x = np.arange(-1.5,2,0.5)
y=[0,0,0,1,1,0,0]
plt.plot(x,y,drawstyle='steps-pre')

plt.subplot(3,2,6)
y=[-1*t for t in y]
plt.plot(x,y,drawstyle='steps-pre')
plt.tight_layout()
plt.show()
```

![正脉冲与负脉冲的幅度谱和相位谱](http://ww1.sinaimg.cn/large/70815d51ly1g5ir9zib25j20bp07sdg0.jpg)

```python
# 连载84：采用对数坐标的矩形脉冲频谱
plt.subplot(2,1,1)
x = np.arange(-1.5,2,0.5)
y=[0,0,0,1,1,0,0]
plt.plot(x,y,drawstyle='steps-pre')

plt.subplot(2,1,2)
f=np.arange(-4,4.1,0.1)
X=abs(np.sinc(f))
plt.semilogy(f,X)
# plt.set_yscale('log')
plt.ylim([1.1*10**-6,1.1])
# plt.yticks([1.1,1.1*10**-2,1.1*10**-4,1.1*10**-6],['0','-20','-40','-60'])
# plt.ylabel('Aplitude(dB)')
```

![采用对数坐标的矩形脉冲频谱](http://ww1.sinaimg.cn/large/70815d51ly1g5irb9us4wj20ay06w0st.jpg)

## BPSK调制频谱

```python
# BPSK调制频谱
# input signal
plt.subplot(3,1,1)
t = np.arange(0,9,1)
d = [0,1,1,0,1,1,0,0,0]
plt.plot(t,d,drawstyle='steps-post')
plt.ylim([-0.5,1.5])
plt.annotate('0',xy=(0.5,1.2))
plt.text(1.5,1.2,'1',fontdict={'size':'8'})
# plt.annotate(['1','0'],xy=[(2.5,1.2),(3.5,1.2)]) #无法同时进行标注

# 基带调制信号(映射+基带调制)
plt.subplot(3,1,2)
t = np.arange(0,9,1)
d = [1,-1,-1,1,-1,-1,1,1,1]
plt.plot(t,d,drawstyle='steps-post')
plt.ylim([-1.5,1.8])
plt.annotate('1',xy=(0.5,1.2))
plt.annotate('-1',xy=(1.5,1.2))

# 频带调制信号(5Hz Cosine Wave)
plt.subplot(3,1,3)
t = np.arange(0,8.1,0.01)
y = [np.cos(2*np.pi*5*t) for t in t if t<1.1]
y.extend([np.cos(2*np.pi*5*t+np.pi) for t in t if 1.1<=t<3.1])
y.extend([np.cos(2*np.pi*5*t) for t in t if 3.1<=t<4.1])
y.extend([np.cos(2*np.pi*5*t+np.pi) for t in t if 4.1<=t<6.1])
y.extend([np.cos(2*np.pi*5*t) for t in t if 6.1<=t<8.1])
plt.plot(t,y)
plt.ylim([-1.8,1.8])
plt.annotate('0',xy=(0.5,1.2))
plt.annotate('$\pi$',xy=(1.5,1.2))

plt.tight_layout()
```

![输入,BPSK调制,频带调制](http://ww1.sinaimg.cn/large/70815d51ly1g5jxo9vwp3j20bs07saa8.jpg)

