# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 09:42:12 2019

@ Description
# Use for test a Vantage Point-tree (VP-tree)

@author: Weidong
"""
    
import numpy as np
import VPTree
import VisualizeTree
import string
import random

#%% 定义向量欧几里德距离
def euclidean(p1, p2):
  return np.sqrt(np.sum(np.power(p2 - p1, 2)))

#%%定义字符串编辑距离
def edit_distance(stra, strb):
    lena = len(stra)
    lenb = len(strb)
    d = np.zeros((lena,lenb))
    for i in range(0,lena):
        d[i][0] = i
    for j in range(0,lenb):
        d[0][j] = j
        
    for i in range(1,lena):
        for j in range(1,lenb):
            if stra[i-1] == strb[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                d[i][j] = min(d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1]+2)
    return d[lena-1][lenb-1]
#stra = 'meelove'
#strb = 'meloove'
#edit_distance(stra, strb)

#%% 随机生成由数字大小写字母组成的字符串
def rand_string(length):
    return ''.join(random.choice(
            string.ascii_lowercase + string.ascii_uppercase + string.digits)
                   for i in range(length)
            )
#print("Example1:", rand_string(length=np.random.randint(1,1000)))
#points = []
#num = input('请输入随机生成元素个数：')
#for i in range(0,int(num)):
#    points.append(rand_string(length=np.random.randint(1,1000)))#限制字符串长度在1-1000之间
    
#%% 选择随机生成或文件读入建立VP树
readchoice = input('随机生成数据点输入0，从文件读取数据输入1：')
if int(readchoice) == 1:#读入文件
#    points = np.loadtxt('vectordata.txt')
    points = []
    for line in open("strdata.txt","r"): #设置文件对象并读取每一行文件
        line=line.strip('\n')
        points.append(line)               #将每一行文件加入到list中
    tree = VPTree.VPTree(points,edit_distance)
else:#随机生成
    pointsnum = int(input('请输入随机生成的数据个数：'))
    num_strchoice = int(input('选择生成向量则输入0，生成字符串输入1：'))
    if num_strchoice == 0:
        vecdim = int(input('请输入向量维度：'))
        points = np.random.randint(1, 100, size=[pointsnum,vecdim])
        # 建立VP树
        tree = VPTree.VPTree(points,euclidean)
    elif num_strchoice == 1:
        points = []
        for i in range(0,int(pointsnum)):
            points.append(rand_string(length=np.random.randint(1,10)))#限制字符串长度在1-10之间
        tree = VPTree.VPTree(points,edit_distance)
    else:
        raise ValueError('必须为0或1')
# 随机产生数据点
#points = np.random.randn(20, 2)
#points = np.random.randint(1, 100, size=[10,2])

#%% 可视化VP树
# 建立用于可视化的字典index
indexdict = VisualizeTree.createindex(points)
# 把VP树转换成字典
treedict = VisualizeTree.tree2dict(tree, indexdict)


depth = VisualizeTree.getTreeDepth(treedict)+1
print('tree depth is ' + str(depth))
show_tree = int(input('显示树则输入1：'))
if show_tree == 1:
    VisualizeTree.createPlot(treedict)# 可视化树


#%% 进行查询

if int(readchoice) == 0 and num_strchoice == 0:
    query = [50]*vecdim        #初始化查询数组
else:
    query = input('请输入查询字符：')
    
queryrange = input('请输入查询范围,输入q退出：')
while queryrange != 'q':
    result=tree.range_search(query, int(queryrange)+1)
    print(result)
    queryrange = input('请输入查询范围,输入q退出：')







