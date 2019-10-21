# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 14:58:25 2019

@ Description
# an implementatio a Vantage Point-tree (VP-tree)
@ Example:
>> import VPTree
>> points = np.random.randint(1, 100, size=[10,2])
>> query = [.5] * 2
>> tree = VPTree.VPTree(points)
>> tree.range_search(query, 2)

@author: Weidong
"""

import numpy as np
# import matplotlib.pyplot as plt

## Define distance function.


class VPTree:
#   构建VPTree -- points: 数据点； dist_fn：距离函数； leaf_size:叶子里面数据个数上限
    def __init__(self, points, dist_fn, leaf_size = 1):
        # 定义叶子里面数据个数上限
        self.leaf_size = leaf_size
        # 定义某节点左右子树及该节点子树所有点与VP点的距离最小最大值
        self.left = None
        self.right = None
        self.left_min = np.inf
        self.left_max = 0
        self.right_min = np.inf
        self.right_max = 0
        self.dist_fn = dist_fn
        self.data = None
        left_points = []
        right_points = []
        
        # 判断叶子个数输入合法性
        if leaf_size < 1 or not isinstance(leaf_size, int):
            raise ValueError('必须为大于0的整数')
        
        # 点集判空
        if not len(points):
            raise ValueError('点集不可为空')

        # 选择与父母距离最大的点作有利点（VP），初始随机
        vp_i = 0
        
        # 判断是否叶子节点
#        if 1 <= len(points) <= leaf_size:
        if len(points) == leaf_size:
            self.data = points
            
        self.vp = points[vp_i]
        points = np.delete(points, vp_i, axis=0)
     
        if len(points) == 0:
            return

        # 选择VP点与子树所有点距离的中位数作划分依据
        distances = [self.dist_fn(self.vp, p) for p in points]
        median = np.median(distances)
        
        # 递归构建左右子树
        for point, distance in zip(points, distances):
            # 如果距离大于中位数，则在圆外，属于右子树
            if distance >= median:
                self.right_min = min(distance, self.right_min)
                if distance > self.right_max:
                    self.right_max = distance
                    right_points.insert(0, point) # 距离最大的点放在第0个点
                else:
                    right_points.append(point)
            # 否则该点属于左子树
            else:
                self.left_min = min(distance, self.left_min)
                if distance > self.left_max:
                    self.left_max = distance
                    left_points.insert(0, point) 
                else:
                    left_points.append(point)

        if len(left_points) > 0:    #leaf_size-1
            self.left = VPTree(points=left_points, dist_fn=self.dist_fn, leaf_size=self.leaf_size)

        if len(right_points) > 0:    #leaf_size-1:
            self.right = VPTree(points=right_points, dist_fn=self.dist_fn, leaf_size=self.leaf_size)

    # 判断该节点是否叶子节点
    def _is_leaf(self):
        return (self.left is None) and (self.right is None)
    
    # 求树的深度
#    def tree_depth(self, node):
#        if node == None:
#            return
#        else:
#            return max(self.tree_depth(node.left), self.tree_depth(node.right)) + 1

    # 构建查询函数，反复接收范围查询并给出查询结果（含数据及其与查询对象的距离）
    # query：查询点； range：查询范围
    def range_search(self, query, range):
        # range_points包含距离及查询结果
        range_points = list()
        # 取出根节点
        nodes_to_visit = [(self, 0)]

        while len(nodes_to_visit) > 0:
            node, d0 = nodes_to_visit.pop(0)
            if node is None or d0 > range:
                continue
            # 求有利点与查询点的距离
            d = self.dist_fn(query, node.vp)
            if d < range:
                range_points.append((d, node.vp)) #在查询范围内则把距离及有利点加入
            # 叶子节点则无需后续操作
            if node._is_leaf():
                continue
            # 查询范围完全落在左子树
            if node.left_min <= d <= node.left_max:
                nodes_to_visit.insert(0, (node.left, 0))
            # d(VP1,q) < R1 - r
            elif node.left_min - range <= d <= node.left_max + range:
                nodes_to_visit.append((node.left,
                                       node.left_min - d if d < node.left_min
                                       else d - node.left_max))

            if node.right_min <= d <= node.right_max:
                nodes_to_visit.insert(0, (node.right, 0))
            elif node.right_min - range <= d <= node.right_max + range:
                nodes_to_visit.append((node.right,
                                       node.right_min - d if d < node.right_min
                                       else d - node.right_max))

        return range_points
