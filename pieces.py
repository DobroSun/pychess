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
        self.size = (self.pos[0], self.pos[0] + WIDTH), (self.pos[1], self.pos[1] + HEIGHT)


    def possible_moves(self):
        pass

    def draw(self, image, pos):
        display.blit(image, pos)
        self.size = (pos[0], pos[0] + WIDTH), (pos[1], pos[1] + HEIGHT)

class King(Piece, pygame.sprite.Sprite):
    def __init__(self, ind):        
        self.choosed = False
        self.ind = ind
        self.color = 1
        if ind == 1:
            self.color = 0
        pygame.sprite.Sprite.__init__(self)
        
        if self.color:
            self.image = pygame.image.load('assets/Chess_klt60.png')
            self.pos = (board[7][3][0], board[7][3][1])
        else:
            self.image = pygame.image.load('assets/Chess_kdt60.png')
            self.pos = (board[0][3][0], board[0][3][1])
        self.size = (self.pos[0], self.pos[0] + WIDTH), (self.pos[1], self.pos[1] + HEIGHT)


    def possible_moves(self):
        pass

    def draw(self, image, pos):
        display.blit(image, pos)
        self.size = (pos[0], pos[0] + WIDTH), (pos[1], pos[1] + HEIGHT)

class Queen(Piece, pygame.sprite.Sprite):
    def __init__(self, ind):        
        self.choosed = False
        self.ind = ind
        self.color = 1
        if ind == 1:
            self.color = 0
        pygame.sprite.Sprite.__init__(self)
        
        if self.color:
            self.image = pygame.image.load('assets/Chess_qlt60.png')
            self.pos = (board[7][4][0], board[7][4][1])
        else:
            self.image = pygame.image.load('assets/Chess_qdt60.png')
            self.pos = (board[0][4][0], board[0][4][1])
        self.size = (self.pos[0], self.pos[0] + WIDTH), (self.pos[1], self.pos[1] + HEIGHT)


    def possible_moves(self):
        pass

    def draw(self, image, pos):
        display.blit(image, pos)
        self.size = (pos[0], pos[0] + WIDTH), (pos[1], pos[1] + HEIGHT)

class Rock(Piece, pygame.sprite.Sprite):
    def __init__(self, ind):        
        self.choosed = False
        self.ind = ind
        self.color = 1
        if ind == 1 or ind == 8:
            self.color = 0
        pygame.sprite.Sprite.__init__(self)
        
        if self.color:
            self.image = pygame.image.load('assets/Chess_rlt60.png')
            self.pos = (board[7][ind][0], board[7][ind][1])
        else:
            self.image = pygame.image.load('assets/Chess_rdt60.png')
            self.pos = (board[0][ind-1][0], board[0][ind-1][1])
        self.size = (self.pos[0], self.pos[0] + WIDTH), (self.pos[1], self.pos[1] + HEIGHT)


    def possible_moves(self):
        pass

    def draw(self, image, pos):
        display.blit(image, pos)
        self.size = (pos[0], pos[0] + WIDTH), (pos[1], pos[1] + HEIGHT)

class Bishop(Piece, pygame.sprite.Sprite):
    def __init__(self, ind):        
        self.choosed = False
        self.ind = ind
        self.color = 1
        if ind == 3 or ind == 6:
            self.color = 0
        pygame.sprite.Sprite.__init__(self)
        
        if self.color:
            self.image = pygame.image.load('assets/Chess_blt60.png')
            self.pos = (board[7][ind][0], board[7][ind][1])
        else:
            self.image = pygame.image.load('assets/Chess_bdt60.png')
            self.pos = (board[0][ind-1][0], board[0][ind-1][1])
        self.size = (self.pos[0], self.pos[0] + WIDTH), (self.pos[1], self.pos[1] + HEIGHT)


    def possible_moves(self):
        pass

    def draw(self, image, pos):
        display.blit(image, pos)
        self.size = (pos[0], pos[0] + WIDTH), (pos[1], pos[1] + HEIGHT)

class Knight(Piece, pygame.sprite.Sprite):
    def __init__(self, ind):        
        self.choosed = False
        self.ind = ind
        self.color = 1
        if ind == 2 or ind == 7:
            self.color = 0
        pygame.sprite.Sprite.__init__(self)
        
        if self.color:
            self.image = pygame.image.load('assets/Chess_nlt60.png')
            self.pos = (board[7][ind][0], board[7][ind][1])
        else:
            self.image = pygame.image.load('assets/Chess_ndt60.png')
            self.pos = (board[0][ind-1][0], board[0][ind-1][1])
        self.size = (self.pos[0], self.pos[0] + WIDTH), (self.pos[1], self.pos[1] + HEIGHT)


    def possible_moves(self):
        pass

    def draw(self, image, pos):
        display.blit(image, pos)
        self.size = (pos[0], pos[0] + WIDTH), (pos[1], pos[1] + HEIGHT)





def create_pieces():
    for i in range(16):
        pawn = Pawn(i)
        list_.append(pawn)
    
    for i in range(2):
        king = King(i)
        list_.append(king)

    for i in range(2):
        queen = Queen(i)
        list_.append(queen)

    for i in [0, 7, 1, 8]:
        rock = Rock(i)
        list_.append(rock)
    
    for i in [2, 5, 3, 6]:
        bishop = Bishop(i)
        list_.append(bishop)
    
    for i in [1, 6, 2, 7]:
        knight = Knight(i)
        list_.append(knight)


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

def calculate_pos(mouse_pos):
    x, y = mouse_pos
    
    for row in board:
        for cell in row:
            if x in range(cell[0], cell[0]+WIDTH+1):
                if y in range(cell[1], cell[1]+HEIGHT+1):
                    return cell
    
create_pieces()




