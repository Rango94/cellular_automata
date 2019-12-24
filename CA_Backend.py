#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/21 10:19 下午
# @Author  : Nanzhi.Wang
# @User    : rango
# @Site    : https://github.com/rango94
# @File    : CA_Backend.py
# @Software: PyCharm
import numpy as np
import copy
class CA_map:
    def __init__(self,size,gap):
        if size%gap!=0:
            print('size和gap的组合不合法')
            exit()
        self.size=int(size/gap)
        self.map=np.zeros((self.size,self.size))
        self.need_to_update=[]
        self.need_to_update_bak=[]

    def set_cell(self,i,j,value):
        self.map[i,j]=value
        for i_ in range(max(0, i - 1), min(i + 2, self.size)):
            for j_ in range(max(0, j - 1), min(j + 2, self.size)):
                if (i_, j_) not in self.need_to_update:
                    self.need_to_update.append((i_, j_))

    def update(self):
        self.need_to_update_bak=copy.deepcopy(self.need_to_update)
        self.need_to_update=[]
        new_map=copy.deepcopy(self.map)
        for i,j in self.need_to_update_bak:
            value=self.cell_update(i, j)
            if value!=self.map[i,j]:
                for i_ in range(max(0,i-1),min(i+2,self.size)):
                    for j_ in range(max(0,j-1),min(j+2,self.size)):
                        if (i_,j_) not in self.need_to_update:
                            self.need_to_update.append((i_, j_))
            new_map[i,j]=value
        self.map=new_map

    def cell_update(self, x, y):
        env=np.sum(self.map[max(0,x-1):min(x+2,self.size),max(0,y-1):min(y+2,self.size)].flatten())-self.map[x,y]
        if env==3:
            return 1
        elif env==2:
            return self.map[x,y]
        else:
            return 0

    def stop(self):
        if np.sum(self.map)==0:
            return True
        else:
            return False