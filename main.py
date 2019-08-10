#!/usr/bin/env python3

import pygame
from pygame.locals import *

import sys
import os.path

from display import *
from pieces import *

choosed = None

while 1:
    display.blit(surf, png_rect)
    update_pieces()
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit(0)    
        if event.type == pygame.MOUSEBUTTONDOWN:  
            if not choosed:
                choosed = check_pieces(mouse_pos)
            else:
                choosed.pos = mouse_pos

    pygame.display.flip()
    clock.tick(10)
