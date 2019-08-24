#!/usr/bin/env python3

import pygame
from pygame.locals import *


WIDTH = 60
HEIGHT = 60


pygame.init()


display = pygame.display.set_mode((800, 600))
pygame.display.set_caption("chess")

clock = pygame.time.Clock()

surf = pygame.image.load('assets/background.png')
png_rect = surf.get_rect(center=(400, 300))


display.blit(surf, png_rect)


def foo(x):
    x = list(x)
    x[0] *= 60
    x[0] += 158
         
    x[1] *= 60
    x[1] += 58
    return tuple(x)


board = [[(x, i) for x in range(8)] for i in range(8)]
board = list(map(lambda x: list(map(foo, x)), board))
print(board)
