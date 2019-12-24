#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/21 9:45 下午
# @Author  : Nanzhi.Wang
# @User    : rango
# @Site    : https://github.com/rango94
# @File    : CA.py
# @Software: PyCharm

import pygame
import sys
from pygame.locals import *
import time
import random as rd
from CA_Backend import CA_map

import numpy as np
import copy

def draw_cell(screen,i,j,cell_size,color):
    pygame.draw.rect(screen, color, [i*cell_size+1,j*cell_size+1, cell_size-1,cell_size-1], 0)

def refresh(screen,size,gap):
    screen.fill([255, 255, 255])
    for i in range(0, size+gap, gap):
        pygame.draw.line(screen, GRAY, [0, i], [size, i], 1)
        pygame.draw.line(screen, GRAY, [i, 0], [i, size], 1)

def text(str_):
    text = pygame.font.SysFont("arialblackttf", 30)
    text_fmt = text.render(str_, 1, (0, 0, 0))
    return text_fmt

bzj=[()]

state='init'
cell_size=2
map_size=720
cell_num=int(map_size/cell_size)
BLACK=[0,0,0]
GRAY=[200,200,200]
WHITE=[255,255,255]

pygame.init()  # 初始化pygame

screen = pygame.display.set_mode((map_size,map_size+30))  # 显示窗口
refresh(screen, map_size, cell_size)
screen.blit(text('press SPACE to set cells'), (0, map_size-15))

CM = CA_map(map_size, cell_size)
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == pygame.K_SPACE and (state=='init' or state=='show'):
                refresh(screen, map_size, cell_size)
                CM = CA_map(map_size, cell_size)
                state='set'
                pygame.display.update()
                continue

            if event.key == pygame.K_SPACE and (state=='set' or state=='playing'):
                state='playing'
                x, y = CM.map.shape
                CM.update()
                for i,j in CM.need_to_update_bak:
                    if CM.map[i, j]==1:
                        draw_cell(screen, i, j, cell_size, BLACK)
                    else:
                        draw_cell(screen, i, j, cell_size, WHITE)
                screen.blit(text('press SPACE to continue'), (0, map_size - 15))
                pygame.display.update()

            if event.key == pygame.K_ESCAPE:
                state='init'

            if event.key == pygame.K_c and state == 'playing':
                state='continue_play'

            if event.key == pygame.K_r and (state=='init' or state=='show'):
                refresh(screen, map_size, cell_size)
                CM = CA_map(map_size, cell_size)
                state = 'playing'
                num=1000
                for i in range(num):
                    x=rd.randint(int(map_size/cell_size/2-num**0.5),int(map_size/cell_size/2+num**0.5))
                    y=rd.randint(int(map_size/cell_size/2-num**0.5),int(map_size/cell_size/2+num**0.5))
                    draw_cell(screen,x,y, cell_size, BLACK)
                    CM.set_cell(x,y, 1)
                pygame.display.update()

            if event.key == pygame.K_l and (state=='init' or state=='show'):
                refresh(screen, map_size, cell_size)
                CM = CA_map(map_size, cell_size)
                state = 'playing'
                num=128
                for i in range(num):
                    x=int(cell_num/2)
                    y=int(cell_num/2)-int(num/2)+i
                    draw_cell(screen,x,y, cell_size, BLACK)
                    CM.set_cell(x,y, 1)
                pygame.display.update()

        if state == 'continue_play':
            x, y = CM.map.shape
            CM.update()
            for i, j in CM.need_to_update_bak:
                if CM.map[i, j] == 1:
                    draw_cell(screen, i, j, cell_size, BLACK)
                else:
                    draw_cell(screen, i, j, cell_size, WHITE)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN and state == 'set':
            x, y = event.pos
            x_ = int(x / cell_size)
            y_ = int(y / cell_size)
            draw_cell(screen, x_, y_, cell_size,BLACK)
            CM.set_cell(x_, y_, 1)
            screen.blit(text('press SPACE to begin'), (0, map_size - 15))
            pygame.display.update()

        if event.type == pygame.QUIT:
            sys.exit()

pygame.quit()  # 退出pygame