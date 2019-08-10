#!/usr/bin/env python3


import pygame
from display import *

import abc


pygame.init()
list_ = []

class Piece(abc.ABC):
    def possible_moves():
        pass

    def draw():
        pass



class Pawn(Piece, pygame.sprite.Sprite):
    def __init__(self, ind):        
        self.choosed = False
        self.ind = ind
        self.color = 1
        if ind >= 8:
            self.color = 0
        pygame.sprite.Sprite.__init__(self)
        
        if self.color:
            self.image = pygame.image.load('assets/Chess_plt60.png')
            self.pos = (board[6][ind][0], board[6][ind][1])
        else:
            self.image = pygame.image.load('assets/Chess_pdt60.png')
            self.pos = (board[1][ind-8][0], board[1][ind-8][1])
        self.size = (self.pos[0], self.pos[0] + 60), (self.pos[1], self.pos[1] + 60)


    def possible_moves(self):
        pass

    def draw(self, image, pos):
        display.blit(image, pos)
        self.choosed = False

def create_pieces():
    for i in range(16):
        pawn = Pawn(i)
        list_.append(pawn)

def update_pieces():
    for i in list_:
        if i.choosed:
            i.possible_moves()
        i.draw(i.image, i.pos)

def check_pieces(mouse_pos):
    for i in list_:
        if i.size[0][0] < mouse_pos[0] < i.size[0][1] and i.size[1][0] < mouse_pos[1] < i.size[1][1]:
            i.choosed = True
            return i

create_pieces()




