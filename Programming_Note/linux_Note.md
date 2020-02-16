linux命令速查

```bash
#命令行下载网络资源
wget
-b     后台下载模式
-O    下载到指定目录
-t      最大尝试次数
-c  	断点续传
-p	  下载页面所有资源包括图片、视频
-r		递归下载
wget -r -p www.baidu.com
```



```bash
#查看当前网卡配置和网络状态等
ifconfig 
```

```bash
#查看版本内核信息，即内核名称、发行版本、节点名称、处理器类型、操作系统位数等
uname -a
cat /proc/cpuinfo
```

```bash
#查看负载状态(输出当前时间、已运行时间、在线用户数，平均负载数(1min, 5min, 15min))
uptime
#查看内存使用量（-m以Mb为的单位，-g以Gb为单位）
free -m
```

```bash
#查看当前登录主机用户情况
who
#所有系统的登入记录
last
```



`history`会保存在`~/.bash_history`文件，编辑`/etc/profile`文件修改HISTSIZE值

`pwd` 显示当前目录

`ls -lhd`以易读形式(-h)显示当前(-d)目录的详细信息(-l)



```bash
cat -n ~/.bashrc   #-n 显示行号，-b显示非空行行号， -A 显示空格、Tab等占位符
```

