# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 21:50:59 2019

@ Description
# to visualize a Vantage Point-tree (VP-tree)
@ Example:
>> import VisualizeTree
>> 
>> indexdict = VisualizeTree.createindex(points)
>> treedict = VisualizeTree.tree2dict(tree, indexdict)
>> VisualizeTree.createPlot(treedict)
>> depth = VisualizeTree.getTreeDepth(treedict)
@author: Weidong
"""
#import importlib
#importlib.reload(VisualizeTree)
#import VPTree
import matplotlib.pyplot as plt

VPNode = dict(boxstyle="sawtooth", fc="0.8")    #VP点样式
leafnode = dict(boxstyle="round4", fc="0.8")    #叶子节点样式
arrow_args = dict(arrowstyle="<-")

def plotNode(nodeTxt, centerPt, parentPt, nodeType): #绘制带箭头的注释
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction', #createPlot.ax1会提供一个绘图区
                            xytext=centerPt, textcoords='axes fraction', \
                            va="center", ha="center",bbox=nodeType, arrowprops=arrow_args)
    
#def createPlot():
#    fig = plt.figure(1,facecolor='white')
#    fig.clf()
#    axprops = dict(xticks=[],yticks=[])
#    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
#    plotNode('VPPoint', (0.5,0.1), (0.1,0.5), VPNode)
#    plotNode('leafPoint', (0.8,0.1), (0.3,0.8), leafnode)
#    plt.show()
    
def getNumLeafs(myTree):#获取树叶节点的数目
    numLeafs = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():#测试节点的数据类型是不是字典，如果是则就需要递归的调用getNumLeafs()函数
        if type(secondDict[key]).__name__=='dict':#test to see if the nodes are dictonaires, if not they are leaf nodes
            numLeafs += getNumLeafs(secondDict[key])
        else:   numLeafs +=1
    return numLeafs

def getTreeDepth(myTree):#获取树的层数
    maxDepth = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':#test to see if the nodes are dictonaires, if not they are leaf nodes
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:   thisDepth = 1
        if thisDepth > maxDepth: maxDepth = thisDepth
    return maxDepth

def plotMidText(cntrPt, parentPt, txtString):#计算父节点和子节点的中间位置，在父节点间填充文本的信息
    xMid = (parentPt[0]-cntrPt[0])/2.0 + cntrPt[0]
    yMid = (parentPt[1]-cntrPt[1])/2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString, va="center", ha="center", rotation=30)
    
def plotTree(myTree, parentPt, nodeTxt):#if the first key tells you what feat was split on
    numLeafs = getNumLeafs(myTree)  #首先计算树的宽和高
    firstStr = list(myTree.keys())[0]     #the text label for this node should be this
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW, plotTree.yOff)
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, VPNode)#标记子节点的属性值
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':#test to see if the nodes are dictonaires, if not they are leaf nodes   
            plotTree(secondDict[key],cntrPt,str(key))        #recursion
        else:   #it's a leaf node print the leaf node
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafnode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD
    
def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)    #no ticks
    #createPlot.ax1 = plt.subplot(111, frameon=False) #ticks for demo puropses 
    plotTree.totalW = float(getNumLeafs(inTree))#c存储树的宽度
    plotTree.totalD = float(getTreeDepth(inTree))#存储树的深度。我们使用这两个变量计算树节点的摆放位置
    plotTree.xOff = -0.5/plotTree.totalW; plotTree.yOff = 1.0;
    plotTree(inTree, (0.5,1.0), '')
    plt.show()

def createindex(points):    #创建VP树的字典index
    indexdict = {}
    for i in range(len(points)):
        indexdict[str(points[i])] = str(points[i])
    return indexdict
    
def tree2dict(node, indexdict):       #调用createPlot（）需要将树结构转换成字典
    if node.left or node.right:
        treedict = {indexdict[str(node.vp)]:{}}
    else:
#        if node.data:
#            return indexdict[str(node.data)]
#        else:
#            return indexdict[str(node.vp)]
        return indexdict[str(node.vp)]
    if node.left:
        treedict[indexdict[str(node.vp)]]['<'] = tree2dict(node.left, indexdict)#递归调用以计算左子树
    if node.right:
        treedict[indexdict[str(node.vp)]]['>='] = tree2dict(node.right, indexdict)#递归调用以计算右子树
    return treedict