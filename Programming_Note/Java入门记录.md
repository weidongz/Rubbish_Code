# Java入门记录

## Java发展史

### Java起源

- 公司：Sun公司
- 发明者：Java之父——James Gosling(高斯林)
- 目标：改造自C++，跨平台，具有实时性
- 火爆：开发将程序嵌入网页执行的技术Applet，从而随着网络繁盛而风靡，Applet更名Java

### Java体系(J2EE, J2Se)

- J2ME（Java2 Micro Edition， Java2 平台的微型版） ， 应用于移动、 无线及有限资源的环境；致力于消费产品 和嵌入式设备的最佳解决方案 ，应用场景少
- **J2SE**（Java 2 Standard Edition， Java 2 平台的标准版） ， 各应用平台的基础， 应用于桌面环境；
- J2EE（Java 2 Enterprise Edition， Java 2 平台的企业版） ， 应用于基于 Java 的应用服务器。 

### Java版本里程碑

- 2004 年 J2SE1.5 包括泛型支持、 基本类型的自动装箱、 改进的循环、 枚举类型、 格式化、I/O 及可变参数。 
- 2014 年  Java SE8，带来了全新的 Lambda 表达式、 流式编程等大量新特性 
- 2018 年 Java SE 11  第一个长期支持版本 



## Java特性

纯面向对象、跨平台（JVM）、健壮（去除c++的指针和内存管理）、安全性较高（垃圾回收，强制类型检查，去除指针操作）

### 跨平台原理(JVM)

Java源码(.java文件) ----编译----> 通用的Java字节码（.class文件） ----JVM翻译---->平台相关的机器码

![JVM](C:\IBrain\Rubbish_Code\Programming_Note\pic\JVM.PNG)

JVM 可以理解成一个可运行 Java 字节码的虚拟计算机系统 (是什么)

### 垃圾回收器（GC）

JVM 提供了一种系统线程跟踪存储空间的分配情况。 并在 JVM 的空闲时， 检查并释放那些可以被释放的存储空间。 

垃圾回收器在 Java 程序运行过程中自动启用， 消除了程序员回收无用内存空间的责任，程序员无法精确控制和干预。 

### Java SE组成部分(JVM, JRE, JDK)

- JVM：Java解释器+即时编译器+运行期系统
- JRE：JVM + **基础类库**(LAng&Util、IO、Reflection、Collections、Math、Concurrency、Logging) + **整合类库**（JDBC、JNDI、RMI）+ **用户界面工具箱**（AWT、Swing、Java 2D）+ **开发技术**（Deployment、Java Web Start、Java Plug-in）

- JDK：JRE + 工具程序与API（编译器javac、运行时解释器java、打包工具jar、文档化工具javadoc、反汇编器javap）

### JRE功能

1. 加载代码： 由类加载器(class loader)完成 
2. 校验代码： 由字节码校验器(byte code verifier)完成 
3. 执行代码： 由运行时解释器(runtime interpreter)完成 



## JDK安装

1. Oracle官网 -> JDK11(LTS) -> 下载对应平台的安装包

2. 配置环境变量：
   - 方式1：JDK安装文件夹\bin 添加进Path中，不便于多版本切换
   - 方式2：创建新变量JAVA_HOME，配置值是安装文件夹，配置JAVA_HOME\bin 进Path，以后切换版本只需要修改JAVA_HOME, 减少Path更改次数

环境变量使得Java能在操作系统全局使用，而不仅仅是JDK子文件夹

命令提示符：`java -version` 查看JDK版本



## Java Hello World

 ```java
public class hello {
	public static void main(String[] args) {
		System.out.println("Hello World!");
	}
}
 ```



`javac hello.java`编译

`java hello`运行

## Eclipse Hello World

eclipse: new->Project->[Java Project]->next->rename project->Finish->Don't create module->No Perspective

src右键new class，重命名package和class name

关机程序如下

```java
package day1;

import java.io.IOException;

public class demo01 {
	/**
	 * 此函数完成关机功能
	 * @param args
	 * @throws IOException 
	 */
	public static void shutDownFunc(Boolean comfirmShut) throws IOException {
		if(comfirmShut) {
			Runtime.getRuntime().exec("shutdown -s -t 3600");
		}
		if(comfirmShut==false) {
			Runtime.getRuntime().exec("shutdown -a");
		}
	}
	
	public static void main(String[] args) throws IOException {
//		System.out.println("Hello");
//		shutDownFunc(true);
		shutDownFunc(false);
	}
}
```

