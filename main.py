#!/usr/bin/env python3

import sys
import pygame
from pygame.locals import *


from screen import *
from pieces import *

choosed = None
ismove = False
side = 1

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
                choosed = check_pieces(mouse_pos, side)
                if choosed:
                    ismove = True
            else:
                
                mouse_pos, i, j = calculate_pos(mouse_pos)

                possible_moves, attack_moves, castle_moves = choosed.possible_moves()
                if (i, j) in possible_moves:   
                    increase_move(choosed)

                    choosed.x, choosed.y = i, j
                    choosed.pos = mouse_pos
                    
                    side += 1
                elif (i, j) in attack_moves:
                    increase_move(choosed)
                    
                    choosed.attack(i, j)
                    choosed.x, choosed.y = i, j
                    choosed.pos = mouse_pos
                    side += 1
                elif (i, j) in castle_moves:
                    increase_move(choosed)

                    rock = castle_moves[(i, j)]
                    
                    if j < rock.y:
                        rock.x, rock.y = i, j - 1
                    else:
                        rock.x, rock.y = i, j + 1

                    choosed.x, choosed.y = i, j
    
                    rock.pos = (board[rock.x][rock.y][0], board[rock.x][rock.y][1]) 
                    choosed.pos = mouse_pos
                    side += 1
                    
                else:
                    choosed.pos = (board[choosed.x][choosed.y][0], board[choosed.x][choosed.y][1])
                choosed.choosed = False
                choosed = None
                ismove = False

    if ismove and choosed and 180 < mouse_pos[0] < 620 and 75 < mouse_pos[1] < 520:
        choosed.pos = (mouse_pos[0]-30, mouse_pos[1]-30)

    pygame.display.flip()
    clock.tick(30)
