linux命令速查

[Linux就该这么学](https://www.linuxprobe.com/chapter-00.html)

[Others Note](https://blog.csdn.net/u013961718/article/details/50463867)

[TOC]

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
#文件打包压缩or解压。-c 创建、-x 解开压缩、-t查看压缩包内容、-v过程详情，-f目标文件名
tar -czvf myetc.tar.gz	/etc#打包/etc并压缩文件，-z用Gzip压缩或解压
tar -xzvf filename.tar.gz -C /home/weidong  #解压并展开.gz压缩包
tar -xjvf filename.tar.bz2  #解压并展开.bzip2压缩包
```

## 系统信息

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
#显示当前目录
pwd
# 以易读形式(-h)显示当前(-d)目录的详细信息(-l)
ls -lhd

```

## 文件搜索与查询

文件类型采用 `file` 来查看，命令类型采用 `type` 来查看
根据文件名查找文件用 `locate` ，查找可执行程序用 `which` ，想不起命令名用 `apropos` 
比起 `man`， `whatis`  更有人情味一点，仅仅显示man page的第一行。
`history`会保存在`~/.bash_history`文件，编辑`/etc/profile`文件修改HISTSIZE值

```bash
# 文本搜索 -c显示找到的次数，-i忽略大小写 -n显示行号 -v列出没有关键词的行
grep entry /etc/passwd	>> entry.txt#找出文本中包含entry的行并输出到/tmp/entry.txt
# 查找文件 -name 匹配名称 -mtime -n 匹配n天前修改的文件 -prune 忽略某目录 --type
find /etx -name "host*" -print #搜索所有以host开头的文件
```

## 文本操作

```bash
cat -n ~/.bashrc   		#-n 显示行号，-b显示非空行行号， -A 显示空格、Tab等占位符
more filename.txt
less
head -n 10
tail -n 10
od -t x filename.txt			#以16进制打开文本
cat filename.txt | tr [a-z] [A-Z]    #tr转换文本字符，将小写转换成大写
wc	filename.txt				#-l 显示行数	-w  显示单词数	-c  显示字符数
grep ^root /etc/passwd |cut -d: -f1	#cut命令根据:分割符提取第一列的文本
diff -c fileA fileB		#-c是上下文详细对比，-b忽略空格差异，-B忽略空行差异
```

## 文件管理

```bash
#新建文件或者(-a 修改读取内容时间atime，-m 修改权限时间mtime， -d同时修改atime和mtime)
touch -d "2 days ago" test 
# 新建目录，-p：多层目录创建，-v：详细创建过程
mkdir mydir			
# 复制文件，cp [源文件] [目标]，若目标是目录，则复制到该目录下，若目标文件已存在，则覆盖
cp a.log b.log #-i 文件存在则询问是否覆盖，-r 目录复制
mv b.log c.log #移动文件或重命名
rm -i c.log	   #-i删除前询问，-r删除目录
# dd命令用于指定转换文件或指定大小的拷贝，bs:设置拷贝块大小，count:拷贝多少块
dd if=/dev/cdrom of=ubuntu.iso #将光驱拷贝成镜像文件
dd if=/dev/sda of=sda_image count=1 bs=512K #将硬盘MBR信息拷贝出来
```

## 用户与组管理

```bash
# 创建新用户dongwei
useradd dongwei
# 创建群组usrgroup
groupadd usrgroup
# 修改用户密码
passwd dongwei #-l 禁止登录，-u 解锁；-d 无密码；-e 使其强制修改密码
# 修改用户属性
usermod -L dongwei  #-dm 迁移家目录，-e账户到期时间，-g 变更所属用户组，=L锁定
# 删除用户
userdel -f dongwei	#-f 强制删除用户、家目录及其相关文件
```

## 管道命令符

"命令A|命令B"：将命令A的标准输出当作命令B的标准输入

`echo yes|sudo apt install `

STDIN，文件描述符0，默认键盘输入，为0则文件或命令输入
STDOUT，文件描述符1，默认输出到屏幕，为1则表示文件
STDERR，文件描述符2，默认屏幕，为2表示文件
命令 > 文件，清空文件并输出
命令 2>> 文件，追加错误输出内容到文件
命令 >> 文件 2>&1，标准输出和错误输出同时写入文件
命令 < 文件， 将文件作命令标准输入
`echo "Linux Command" >> readme.txt #给readme文件追加一行文字`



| 通配符 |                      |
| ------ | -------------------- |
| ？     | 匹配任意单个字符     |
| [0-9]  | 匹配范围内的数字     |
| [abc]  | 匹配括号中的单个字符 |
| *      | 匹配零个或多个字符   |

## 环境变量

用户输入命令后，
1.相对/绝对路径输入的命令将直接执行
2.检查是否alias别名命令
3.bash判断是内部命令（解释器内部的）还是外部命令（独立于解释器外），用`type`判断
4.bash将在`$PATH`环境变量处寻找命令文件，即`echo $PATH`是查看命令文件存放目录，
自定义的命令加入PATH后就可以被bash找到
`$PATH`之间的目录用：分割符隔开

```bash
env  #查看系统所有环境变量
echo $PATH #查看 查找执行文件路径
echo $PS1  #bash提示符
echo $RAMDOM  #随机输出数字
echo $SHELL $HOME $HISTSIZE $LANG
WORKDIR=/home/workdir #定义变量
echo $WORKDIR #使用变量
export WORKDIR #将局部变量提升为全局变量，即局限于某个用户的变量将能被全部用户使用
```

## Shell脚本

查看所有可用的Shell编辑器`cat /etc/shells`，查看当前Shell编辑器`echo $SHELL`

Shell工作分为交互式和批处理(Batch)，批处理通过运行脚本Script实现

Shell脚本需要许多Linux命令及正则表达式、管道命令及数据流重定向知识作支撑

```bash
#!/bin/bash  
# 以上脚本声明
# 运行需要文件具可执行权限：chmod u+x Example.sh
# 运行方式：(1)./Example.sh  (2)sh Example.sh (3)source Example.sh
echo "当前脚本名称是$0"
echo "共计$#个参数，分别是$*"
echo "上条命令成功情况$?"
```

Shell位置参数：命令行输入参数，则脚本调用`$1、$2 ...`
Shell预定义变量：`$0：Shell脚本当前程序名；$1-9,${10}；位置变量；$#参数个数；`
`$?：判断上条命令执行成功与否，$*：所有位置变量的值`

条件测试语句：判断特定表达式成立与否

```bash
#!/bin/bash
#文件测试，-d判断是否目录，-e判断存在性，-f判断是否文件，
#-r判断用户有否读入权限，-w判断写入权限，-x判断执行权限
[ -d /etc/fatab ]	#中括号左右必须有空格
echo $?				#输出0是成功，非0则失败
[ -e /etc/passwd ] && vim /etc/passwd
# 整数大小判断：eq(equal)/ne(not equal)/gt(greeater than)/lt/le(less equal)/ge
[ 10 -ge 9 ] && echo "10 is equal or greater than 9"
# 字符串判断：-z（zero）判空，= 判相等， !=
[ $LANG!="en.US" ]&&echo "Not en.US"
# 单分支if语句
DIR="/tmp/bin"
if [ !-e $DIR ]
  then 
  mkdir -p $DIR
fi
# 双分支if, then , else, fi
# for ... in [...], do , done
HLIST=$(cat ~/ipadds.txt)
for IP in $HLIST
do
ping -c 3 -i 0.2 -W 3 $IP &> /dev/null
if [ $? -eq 0 ] ; then
echo "Host $IP is On-line."
else
echo "Host $IP is Off-line."
fi
done
```

while语言编写猜数程序

```bash
#!/bin/bash
PRICE=$(expr $RANDOM % 1000)
TIMES=0
echo "商品实际价格为0-999之间，猜猜看是多少？"
while true
do
read -p "请输入您猜测的价格数目：" INT
let TIMES++
if [ $INT -eq $PRICE ] ; then
echo "恭喜您答对了，实际价格是 $PRICE"
echo "您总共猜测了 $TIMES 次"
exit 0  #退出死循环
elif [ $INT -gt $PRICE ] ; then
echo "太高了！"
else
echo "太低了！"
fi
done
```

类似C语言的switch语句的case语法

```bash
read -p "请输入一个字符，并按Enter键确认：" KEY
case "$KEY" in
[a-z]|[A-Z])
echo "您输入的是 字母。"
;;
[0-9])
echo "您输入的是 数字。"
;;
*)
echo "您输入的是 空格、功能键或其他控制字符。"
esac
```

## 计划任务服务程序

设置一次性计划任务：`echo "systemctl restart httpd | at 23:30"`
查看一次性计划任务：`at -l`
删除任务号是2的一次性计划任务：`atrm 2`

创建、编辑计划任务：`crontab -e`
查看当前计划任务：`crontab -l`
删除：`crontab -r`

```bash
#crontab命令格式： 分、时、日、月、星期 命令
# 计划任务中的“分”字段必须有数值，绝对不能为空或是*号，而“日”和“星期”字段不能同时使用，否则就##会发生冲突。
# For example, you can run a backup of all your user accounts
# at 5 a.m every week Monday with:
0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
```

## 用户组

管理员UID为0：系统的管理员用户。
系统用户UID为1～999： Linux系统为了避免因某个服务程序出现漏洞而被黑客提权至整台服务器，默认服务程序会有独立的系统用户负责运行，进而有效控制被破坏范围。
普通用户UID从1000开始：是由管理员创建的用于日常工作的用户。

`id weidong`

`passwd -S weidong`#查看weidong账号锁定情况及加密算法

## 文件权限

`ls -l`的第一个字符是文件标识字符，

 -：普通文件。

d：目录文件。

l：链接文件。

b：块设备文件。

c：字符设备文件。

p：管道文件

对目录文件来说，“可读”表示能够读取目录内的文件列表；“可写”表示能够在目录内新增、删除、重命名文件；而“可执行”则表示能够进入该目录。

### 文件特殊权限

**SUID**是一种对二进制程序进行设置的特殊权限，可以让二进制程序的执行者临时拥有属主的权限

> 例子：所有用户都可以执行passwd命令来修改自己的用户密码，而用户密码保存在/etc/shadow文件中。仔细查看这个文件就会发现它的默认权限是000，也就是说除了root管理员以外，所有用户都没有查看或编辑该文件的权限。但是，在使用passwd命令时如果加上SUID特殊权限位，就可让普通用户临时获得程序所有者的身份

`chmod -f u+s example.sh`
此时文件所有者的权限由rwx变成了rws



**SGID**让执行者临时拥有属组的权限（对拥有执行权限的二进制程序进行设置）；或在某个目录中创建的文件自动继承该目录的用户组（只可以对目录进行设置）

`chmod -Rf g+s testdir/ 
#针对目录进行操作时需要加上大写参数-R来表示递归操作，即对目录内所有的文件进行整体操作`
此时文件所属组的权限由rwx变成了rws



**SBIT**（Sticky Bit）特殊权限位了（也可以称之为特殊权限位之粘滞位）。SBIT特殊权限位可确保用户只能删除自己的文件，而不能删除其他用户的文件。换句话说，当对某个目录设置了SBIT粘滞位权限后，那么该目录中的文件就只能被其所有者执行删除操作了。

`chmod -R o+t linux/`
当目录被设置SBIT特殊权限位后，文件的其他人权限部分的x执行权限就会被替换成t或者T，原本有x执行权限则会写成t，原本没有x执行权限则会被写成T。



**隐藏属性**`lsattr ./linuxprobe`
设置隐藏属性`chattr +a ./linuxprobe`
chattr命令中用于隐藏权限的参数及其作用

参数	作用
i	无法对文件进行修改；若对目录设置了该参数，则仅能修改其中的子文件内容而不能新建或删除文件
a	仅允许补充（追加）内容，无法覆盖/删除内容（Append Only）
S	文件内容在变更后立即同步到硬盘（sync）
s	彻底从硬盘中删除，不可恢复（用0填充原文件所在硬盘区域）
A	不再修改这个文件或目录的最后访问时间（atime）
b	不再修改文件或目录的存取时间
D	检查压缩文件中的错误
d	使用dump命令备份时忽略本文件/目录
c	默认将文件或目录进行压缩
u	当删除该文件后依然保留其在硬盘中的数据，方便日后恢复
t	让文件系统支持尾部合并（tail-merging）
x	可以直接访问压缩文件中的内容



**文件访问控制列表ACL**

通俗来讲，基于普通文件或目录设置ACL其实就是针对指定的用户或用户组设置文件或目录的操作权限。另外，如果针对某个目录设置了ACL，则目录中的文件会继承其ACL；若针对文件设置了ACL，则文件不再继承其所在目录的ACL。

`getfacl命令用于显示文件上设置的ACL信息，格式为“getfacl 文件名称”`

`setfacl命令用于管理文件的ACL规则，格式为“setfacl [参数] 文件名称”。文件的ACL提供的是在所有者、所属组、其他人的读/写/执行权限之外的特殊权限控制，使用setfacl命令可以针对单一用户或用户组、单一文件或目录来进行读/写/执行权限的控制。`



**sudo命令**用于给普通用户提供额外的权限来完成原本root管理员才能完成的任务

root管理员使用`visudo 来修改用户权限`
`root ALL=(ALL) ALL
linuxprobe ALL=NOPASSWD: /usr/sbin/poweroff`



## 防火墙策略

主要功能都是依据策略对穿越防火墙自身的流量进行过滤。防火墙策略可以基于流量的源目地址、端口号、协议、应用等信息来定制，然后防火墙使用预先定制的策略规则监控出入的流量

**iptables**服务会把配置好的防火墙策略交由内核层面的netfilter网络过滤器来处理，而firewalld服务则是把配置好的防火墙策略交由内核层面的nftables包过滤框架来处理

防火墙会从上至下的顺序来读取配置的策略规则，在找到匹配项后就立即结束匹配工作并去执行匹配项中定义的行为（即放行或阻止）。如果在读取完所有的策略规则之后没有匹配项，就去执行默认的策略。一般而言，防火墙策略规则的设置有两种：一种是“通”（即放行），一种是“堵”（即阻止）。当防火墙的默认策略为拒绝时（堵），就要设置允许规则（通）

iptables服务把用于处理或过滤流量的策略条目称之为规则，多条规则可以组成一个规则链，而规则链则依据数据包处理位置的不同进行分类
从内网向外网发送的流量一般都是可控且良性的，因此我们使用最多的就是INPUT规则链，该规则链可以增大黑客人员从外网入侵内网的难度
针对不同的规则匹配实施不同的动作，动作对应到iptables服务的术语中分别是ACCEPT（允许流量通过）、REJECT（拒绝流量通过）、LOG（记录日志信息）、DROP（拒绝流量通过）。“允许流量通过”和“记录日志信息”都比较好理解，这里需要着重讲解的是REJECT和DROP的不同点。就DROP来说，它是直接将流量丢弃而且不响应；REJECT则会在拒绝流量后再回复一条“您的信息已经收到，但是被扔掉了”信息，从而让流量发送方清晰地看到数据被拒绝的响应信息。
iptables是一款基于命令行的防火墙策略管理工具
参数	作用
-P	设置默认策略
-F	清空规则链
-L	查看规则链
-A	在规则链的末尾加入新规则
-I num	在规则链的头部加入新规则
-D num	删除某一条规则
-s	匹配来源地址IP/MASK，加叹号“!”表示除这个IP外
-d	匹配目标地址
-i 网卡名称	匹配从这块网卡流入的数据
-o 网卡名称	匹配从这块网卡流出的数据
-p	匹配协议，如TCP、UDP、ICMP
--dport num	匹配目标端口号
--sport num	匹配来源端口号

```bash
#将INPUT规则链设置为只允许指定网段的主机访问本机的22端口，拒绝来自其他所有主机的流量
iptables -I INPUT -s 192.168.10.0/24 -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j REJECT
#防火墙策略规则是按照从上到下的顺序匹配的，因此一定要把允许动作放到拒绝动作前面，否则所有的流量就将被拒绝掉，从而导致任何主机都无法访问我们的服务
#使用iptables命令配置的防火墙规则默认会在系统下一次重启时失效，如果想让配置的防火墙策略永久生效，还要执行保存命令
service iptables save
```



**firewalld**支持动态更新技术并加入了区域（zone）的概念。简单来说，区域就是firewalld预先准备了几套防火墙策略集合（策略模板）



**SNAT**（Source Network Address Translation，源网络地址转换）技术。SNAT是一种为了解决IP地址匮乏而设计的技术，它可以使得多个内网中的用户通过同一个外网IP接入Internet。
当我们通过家中的网关设备（比如无线路由器）访问本书配套站点www.linuxprobe.com时，就用到了SNAT技术。
![使用SNAT技术](https://www.linuxprobe.com/wp-content/uploads/2015/03/%E4%BD%BF%E7%94%A8SNAT1.png)

对内网和对外网提供服务的网卡要选择的防火墙策略区域也是不一样的。也就是说，可以把网卡与防火墙策略区域进行绑定（见图8-12），这样就可以使用不同的防火墙区域策略，对源自不同网卡的流量进行针对性的监控，效果会更好



**TCP Wrappers**是RHEL 7系统中默认启用的一款流量监控程序，它能够根据来访主机的地址与本机的目标服务程序作出允许或拒绝的操作。

TCP Wrappers服务的防火墙策略由两个控制列表文件所控制，用户可以编辑允许控制列表文件来放行对服务的请求流量，也可以编辑拒绝控制列表文件来阻止对服务的请求流量。控制列表文件修改后会立即生效

系统将会先检查允许控制列表文件（/etc/hosts.allow），如果匹配到相应的允许策略则放行流量；如果没有匹配，则去进一步匹配拒绝控制列表文件（/etc/hosts.deny），若找到匹配项则拒绝该流量。如果这两个文件全都没有匹配到，则默认放行流量

编写拒绝策略规则时，填写的是服务名称，而非协议名称；
建议先编写拒绝策略规则，再编写允许策略规则，以便直观地看到相应的效果。



## 配置网卡服务

参考自https://www.linuxprobe.com/chapter-09.html

nmtui来配置网络

`nmcli connection show` ：查看网络信息

`nmcli con show eno16777736`：查看网卡状态

使用nmcli命令并按照“connection add con-name type ifname”的格式来创建网络会话，允许用户在多个配置文件中快速切换

`nmcli connection add con-name house type ethernet ifname eno16777736`

`nmcli connection up house `  ：激活house配置 



再添加一块网卡设备，请确保两块网卡都处在同一个网络连接中（即网卡模式相同），处于相同模式的网卡设备才可以进行网卡绑定，否则这两块网卡无法互相传送数据。
假设我们对两块网卡实施了绑定技术，这样在正常工作中它们会共同传输数据，使得网络传输的速度变得更快；而且即使有一块网卡突然出现了故障，另外一块网卡便会立即自动顶替上去，保证数据传输不会中断。
使用Vim文本编辑器来配置网卡设备的绑定参数。这些原本独立的网卡设备此时需要被配置成为一块“从属”网卡，服务于“主”网卡，不应该再有自己的IP地址等信息。

##### ## 不间断会话服务

screen是一款能够实现多窗口远程控制的开源服务程序，简单来说就是为了解决网络异常中断或为了同时控制多个远程终端窗口而设计的程序。用户还可以使用screen服务程序同时在多个远程会话中自由切换

screen命令不仅可以确保用户在极端情况下也不丢失对系统的远程控制，保证了生产环境中远程工作的不间断性，而且它还具有会话共享、分屏切割、会话锁定等实用的功能。其中，会话共享功能是一件很酷的事情，当多个用户同时控制主机的时候，它可以把屏幕内容共享出来，也就是说每个用户都可以看到相同的内容。

screen命令能做的事情非常多：可以用-S参数创建会话窗口；用-d参数将指定会话进行离线处理；用-r参数恢复指定会话；用-x参数一次性恢复所有的会话；用-ls参数显示当前已有的会话；以及用-wipe参数把目前无法使用的会话删除

