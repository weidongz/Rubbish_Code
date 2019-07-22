# 深入浅出通信原理Python代码版

> 深入浅出通信原理（http://www.txrjy.com/thread-394879-1-4.html）从2010年4月8日开始在C114通信人家园上线连载，从多项式乘法讲起，一步一步引出卷积、傅立叶级数展开、旋转向量、三维频谱、IQ调制、数字调制等一系列通信原理知识

## 连载1：从多项式乘法说起

$$
(x+1)(x^2+2x+5)=x^3+3x^2+7x+5
$$

```python
import sympy
x = sympy.Symbol('x')
sympy.expand((x+1)*(x*x+2*x+5))
```



![一步得到计算结果](http://download.txrjy.com/forum/month_1004/20100409_ab8bbd15a02b50868f846jgYjzr6SQ8c.jpg)

>这种计算方法总结起来就是：
>反褶：一般多项式都是按x的降幂排列，这里将其中一个多项式的各项按x的升幂排列。
>平移：将按x的升幂排列的多项式每次向右平移一个项。
>相乘：垂直对齐的项分别相乘。
>求和：相乘的各结果相加。
>
>**反褶、平移、相乘、求和**－这就是通信原理中最常用的一个概念“**卷积**”的计算过程。

## 连载2：卷积的表达式

将多项式转换成矩阵形式
$$
x+1 -> [1,1]\\
x^2+2x+5 -> [1,2,5]\\
x^3+3x^2+7x+5=[1,1]*[1,2,5]=[1,3,7,5]\\
其中卷积（*）的运算如下：\\
c(n)=a(n)*b(n)=\sum_{k=0}^n{a（k)b(n-k)},n=0~(n1+n2)\\
其中n1是a(n)的系数总个数，n2是b(n)的系数总个数
$$

## 连载3: Python计算卷积

```python
import numpy as np
np.convolve([1,1],[1,2,5]) #上例,result:[1, 3, 7, 5]
# 杨辉三角，输入行数，输出对应行的值
def pascal_triangle(n):
    if n == 0:
        return 1
    elif n == 1:
        return [1,1]
    else:
        return np.convolve([1,1],pascal_triangle(n-1))
# test code    
for i in range(0,7):
    print(pascal_triangle(i))
    
    
# 杨辉三角，迭代器形式
def triangles():
  nlist=[1]
  while True:
    yield nlist
    nlist.append(0)
    nlist = [nlist[i] + nlist[i-1] for i in range(len(nlist))]
# test code
tr = triangles()
for i in range(0,7):
    print(next(tr))
```

## 连载4：将信号表示成多项式的形式

$$
Fourier Transform:signal(x) = x_nx^n+\cdots+a_2x^2+a_1x+a_0\\
x^n=f(nw_0)\\
x = cosw_0t+jsinw_0t = e^{jw_0t} = f(w_0)\\
x^2 = (cosw_0t+jsinw_0t)^2 = cos^2w_0t-sin^2w_0t+j2sinw_0tcosw_0t=f(2w_0)
$$

## 连载5：欧拉公式证明

$$
欧拉公式:cosw_0t+jsinw_0t=e^{jw_0t}
$$

```python
import sympy
x = sympy.Symbol('x')
sympy.series(sympy.exp(sympy.I*x), x, 0, 10) #series perform Taylor expansion
sympy.expand(series(sin(x), x, 0, 10))
sympy.expand(series(cos(x), x, 0, 10))
```

利用泰勒展开，从输出结果易看出欧拉公式成立

## 连载6：利用卷积计算两个信号的乘积

若两个信号均表示成多项式形式，则可通过卷积计算信号相乘结果。

![陈老师连载6原图](http://download.txrjy.com/forum/month_1004/20100413_720bf3fc4d76a36ae60b1T4MgSttaTVm.jpg)

## 连载7： 信号进行傅里叶级数展开

$$
f(t)=\sum_{k=-\infty}^{+\infty}c_ke^{jkw_0t}
$$

> ck是傅里叶系数
>
> 以角频率w为横轴，傅里叶系数ck为纵轴，画出频谱图

```python
# Further improvement:https://blog.csdn.net/u012915522/article/details/91506120
import matplotlib.pyplot as plt
plt.subplot(3,1,1)
plt.stem([0,1,2,3],[6,5,1,0],use_line_collection=True)
plt.yticks([0,1,5,6])
# plt.axis('off')
plt.xticks([0,1,2,3],('0','w','2w','3w'))
plt.subplot(3,1,2)
plt.stem([0,1,2,3],[2,3,0,0],use_line_collection=True)
plt.xticks([0,1,2,3],('0','w','2w','3w'))
plt.yticks([0,1,2,3])
plt.subplot(3,1,3)
plt.stem([0,1,2,3],[12,28,17,3],use_line_collection=True)
plt.xticks([0,1,2,3],('0','w','2w','3w'))
plt.yticks([3,17,12,28])
# plt.axis('off')
plt.tight_layout()
plt.show()
```

![代码输出](data:image/png;base64,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)

## 连载8：时域信号相乘相当于频域卷积

由连载6显然如此

|          时域 |                       FFT                        | 频域           |
| ------------: | :----------------------------------------------: | :------------- |
|          f(t) |  $f(t)=\sum_{n=-\infty}^{+\infty}f[n]^{jkw_0t}$  | f[n]           |
|          g(t) | $$g(t)=\sum_{n=-\infty}^{+\infty}g[n]^{jkw_0t}$$ | g[n]           |
| y(t)=f(t)g(t) |  $y(t)=\sum_{n=-\infty}^{+\infty}y[n]^{jkw_0t}$  | y[n]=f[n]*g[n] |

