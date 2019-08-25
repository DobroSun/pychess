#!/usr/bin/env python3

import pygame
from pygame.locals import *


WIDTH = HEIGHT = 60

pygame.init()
display = pygame.display.set_mode((800, 600))
pygame.display.set_caption("chess")

clock = pygame.time.Clock()

surf = pygame.image.load('assets/background.png')
png_rect = surf.get_rect(center=(400, 300))

display.blit(surf, png_rect)

def foo(x):
    x = list(x)
    x[0] *= WIDTH
    x[0] += 158
         
    x[1] *= HEIGHT
    x[1] += 58
    return tuple(x)

def make_board():
    board = [[(x, i) for x in range(8)] for i in range(8)]
    board = list(map(lambda x: list(map(foo, x)), board))
    
    return board

def calculate_pos(mouse_pos):
    x, y = mouse_pos
    
    for i in range(len(board)):
        for j in range(len(board[i])):
            if x in range(board[i][j][0], board[i][j][0]+WIDTH+1):
                if y in range(board[i][j][1], board[i][j][1]+HEIGHT+1):
                    return board[i][j], i, j

def increase_move(obj):
    if hasattr(obj, "move"):
        obj.move += 1

board = make_board()
