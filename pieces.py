#!/usr/bin/env python3

import pygame
import abc


from screen import *



list_ = []

class Piece(abc.ABC):
    @abc.abstractmethod
    def possible_moves():
        pass
    
    @abc.abstractmethod
    def can_attack():
        pass

    def draw_moves(self):
        possible_moves, attack_moves, castling_moves  = self.possible_moves()
        possible_moves.extend(attack_moves)
        possible_moves.extend(castling_moves)
        
        for move in possible_moves:
            pygame.draw.circle(display, (192, 192, 192), 
                               (board[move[0]][move[1]][0] + 30, board[move[0]][move[1]][1] + 30), 10)
    
    def draw(self, image, pos):
        display.blit(image, pos)
        self.size = (pos[0], pos[0] + WIDTH), (pos[1], pos[1] + HEIGHT)
    
    def attack(self, i, j):
        for item in list_:
            if item.x == i and item.y == j:
                list_.remove(item)
                return 




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
            self.x, self.y = 6, ind
        else:
            self.image = pygame.image.load('assets/Chess_pdt60.png')
            self.pos = (board[1][ind-8][0], board[1][ind-8][1])
            self.x, self.y = 1, ind-8
        self.size = (self.pos[0], self.pos[0] + WIDTH), (self.pos[1], self.pos[1] + HEIGHT)

    def can_attack(self):
        attack_moves = []
        if self.color == 0:
            for item in list_:
                if item.color == 1 and self.x + 1 == item.x and self.y + 1 == item.y:
                    attack_moves.append((self.x + 1, self.y + 1))
                elif item.color == 1 and self.x + 1 == item.x and self.y - 1 == item.y:
                    attack_moves.append((self.x + 1, self.y - 1))
        else:
            for item in list_:
                if item.color == 0 and self.x - 1 == item.x and self.y + 1 == item.y:
                    attack_moves.append((self.x - 1, self.y + 1))
                elif item.color == 0 and self.x - 1 == item.x and self.y - 1 == item.y:
                    attack_moves.append((self.x - 1, self.y - 1))
            
        return attack_moves

    def possible_moves(self):
        
        if self.color == 0:
            possible_moves = [(self.x + 1, self.y) if self.x + 1 <= 7 else (self.x, self.y)]
            if self.x == 1:
                possible_moves.append((self.x + 2, self.y))
            
            tmp = list_.pop(list_.index(self))
            
            for move in possible_moves:
                for item in list_:
                    if item.x == move[0] and item.y == move[1]:
                        wrong_move = possible_moves.pop(possible_moves.index(move))
                        for move in possible_moves:
                            if move[0] > wrong_move[0] and move[1] == wrong_move[1]:
                                possible_moves.remove(move)

        else:
            possible_moves = [(self.x - 1, self.y) if self.x - 1 >= 0 else (self.x, self.y)]
            
            if self.x == 6:
                possible_moves.append((self.x - 2, self.y))
            
            tmp = list_.pop(list_.index(self))
            
            for move in possible_moves:
                for item in list_:
                    if item.x == move[0] and item.y == move[1]:
                        wrong_move = possible_moves.pop(possible_moves.index(move))
                        for move in possible_moves:
                            if move[0] < wrong_move[0] and move[1] == wrong_move[1]:
                                possible_moves.remove(move)

            
        attack_moves = self.can_attack()
        list_.append(tmp)

        return possible_moves, attack_moves, {}

    
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
            self.pos = (board[7][4][0], board[7][4][1])
            self.x, self.y = 7, 4
        else:
            self.image = pygame.image.load('assets/Chess_kdt60.png')
            self.pos = (board[0][4][0], board[0][4][1])
            self.x, self.y = 0, 4
        self.castling = True
        self.move = 0
        self.size = (self.pos[0], self.pos[0] + WIDTH), (self.pos[1], self.pos[1] + HEIGHT)

    def can_attack(self, possible_moves):
        attack_moves = []

        for move in possible_moves:
            for item in list_:
                if item.x == move[0] and item.y == move[1] and item.color != self.color:
                    possible_moves.remove(move)
                    attack_moves.append(move)

        return attack_moves

    def possible_moves(self):
        attack_moves = []
        possible_moves = [(self.x + 1, self.y), (self.x - 1, self.y), (self.x, self.y + 1), (self.x, self.y - 1), \
                          (self.x + 1, self.y + 1), (self.x + 1, self.y - 1), (self.x - 1, self.y + 1), \
                          (self.x - 1, self.y - 1)]
        
        moves = []
        for move in possible_moves:
            if (0 <= move[0] <= 7) and (0 <= move[1] <= 7):
                moves.append(move)
        possible_moves = moves
        
        tmp = list_.pop(list_.index(self))

        wrong_moves = []
        
        for move in possible_moves:
            for item in list_:
                if item.x == move[0] and item.y == move[1] and item.color == self.color:
                    wrong_moves.append(move)

        for move in wrong_moves:
            possible_moves.remove(move)
        
        attack_moves = self.can_attack(possible_moves)
         
        long_, sh_ = self.check_castling()
        castle_moves = self.castle(long_, sh_) if self.castling else {}


        list_.append(tmp)
        return possible_moves, attack_moves, castle_moves
        
    def check_castling(self):
        sh_castle = [(self.x, self.y + 1), (self.x, self.y + 2)]
        long_castle = [(self.x, self.y - 1), (self.x, self.y - 2), (self.x, self.y - 3)]
        
        sh_rock = None
        long_rock = None

        rock_pos = [(self.x, self.y + 3), (self.x, self.y - 4)]
        for move in sh_castle:
            for item in list_:        
                if item.x == move[0] and item.y == move[1]:
                    sh_rock = 0
                    break
        if sh_rock is None:
            for item in list_:
                if item.x == rock_pos[0][0] and item.y == rock_pos[0][1] and item.ind in [0, 7, 1, 8] \
                                        and item.move == 0:       
                    
                    sh_rock = item

        for move in long_castle:
            for item in list_:
                if item.x == move[0] and item.y == move[1]:
                    long_rock = 0
                    break
        if long_rock is None:
            for item in list_:
                if item.x == rock_pos[1][0] and item.y == rock_pos[1][1] and item.ind in [0, 7, 1, 8] \
                                        and item.move == 0 and self.move == 0:
                    long_rock = item

        return long_rock, sh_rock

    def castle(self, long_, sh_):
        castling_moves = {}
        if long_:
            castling_moves[(self.x, self.y - 2)] = long_
        if sh_:
            castling_moves[(self.x, self.y + 2)]  = sh_
        return castling_moves

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
            self.pos = (board[7][3][0], board[7][3][1])
            self.x, self.y = 7, 3
        else:
            self.image = pygame.image.load('assets/Chess_qdt60.png')
            self.pos = (board[0][3][0], board[0][3][1])
            self.x, self.y = 0, 3
        self.size = (self.pos[0], self.pos[0] + WIDTH), (self.pos[1], self.pos[1] + HEIGHT)

    
    def can_attack(self, possible_moves):
        attack_moves = []
       
 
        tmp = [self.x, self.y]
        if (tmp[0] + 1, tmp[1] + 1) in possible_moves:
            tmp = tmp[0] + 1, tmp[1] + 1
            while tmp in possible_moves:
                tmp = (tmp[0] + 1, tmp[1] + 1)
        else:
            tmp = tmp[0] + 1, tmp[1] + 1

        for item in list_:
            if tmp[0] == item.x and tmp[1] == item.y and item.color != self.color:
                attack_moves.append(tmp)


        tmp = [self.x, self.y]
        if (tmp[0] + 1, tmp[1] - 1) in possible_moves:
            tmp = tmp[0] + 1, tmp[1] - 1
            while tmp in possible_moves:
                tmp = (tmp[0] + 1, tmp[1] - 1)
        else:
            tmp = tmp[0] + 1, tmp[1] - 1
    
        for item in list_:
            if tmp[0] == item.x and tmp[1] == item.y and item.color != self.color:
                attack_moves.append(tmp)

        tmp = [self.x, self.y]
        if (tmp[0] - 1, tmp[1] + 1) in possible_moves:
            tmp = tmp[0] - 1, tmp[1] + 1
            while tmp in possible_moves:
                tmp = (tmp[0] - 1, tmp[1] + 1)
        else:
            tmp = tmp[0] - 1, tmp[1] + 1
            
        for item in list_:
            if tmp[0] == item.x and tmp[1] == item.y and item.color != self.color:
                attack_moves.append(tmp)

        tmp = [self.x, self.y]
        if (tmp[0] - 1, tmp[1] - 1) in possible_moves:
            tmp = tmp[0] - 1, tmp[1] - 1
            while tmp in possible_moves:
                tmp = (tmp[0] - 1, tmp[1] - 1)
        else:
            tmp = tmp[0] - 1, tmp[1] - 1
        
        for item in list_:
            if tmp[0] == item.x and tmp[1] == item.y and item.color != self.color:
                attack_moves.append(tmp)
 
        
        tmp = [self.x, self.y]
        if (tmp[0] + 1, tmp[1]) in possible_moves:
            tmp = tmp[0] + 1, tmp[1]
            while tmp in possible_moves:
                tmp = (tmp[0] + 1, tmp[1])
        else:
            tmp = tmp[0] + 1, tmp[1]

        for item in list_:
            if tmp[0] == item.x and tmp[1] == item.y and item.color != self.color:
                attack_moves.append(tmp)


        tmp = [self.x, self.y]
        if (tmp[0] - 1, tmp[1]) in possible_moves:
            tmp = tmp[0] - 1, tmp[1]
            while tmp in possible_moves:
                tmp = (tmp[0] - 1, tmp[1])
        else:
            tmp = tmp[0] - 1, tmp[1]
    
        for item in list_:
            if tmp[0] == item.x and tmp[1] == item.y and item.color != self.color:
                attack_moves.append(tmp)

        tmp = [self.x, self.y]
        if (tmp[0], tmp[1] + 1) in possible_moves:
            tmp = tmp[0], tmp[1] + 1
            while tmp in possible_moves:
                tmp = (tmp[0], tmp[1] + 1)
        else:
            tmp = tmp[0], tmp[1] + 1
            
        for item in list_:
            if tmp[0] == item.x and tmp[1] == item.y and item.color != self.color:
                attack_moves.append(tmp)

        tmp = [self.x, self.y]
        if (tmp[0], tmp[1] - 1) in possible_moves:
            tmp = tmp[0], tmp[1] - 1
            while tmp in possible_moves:
                tmp = (tmp[0], tmp[1] - 1)
        else:
            tmp = tmp[0], tmp[1] - 1
        
        for item in list_:
            if tmp[0] == item.x and tmp[1] == item.y and item.color != self.color:
                attack_moves.append(tmp)

        return attack_moves



    def possible_moves(self):
        attack_moves = []
        possible_moves = []

        tmp = 0
        while 0 <= tmp <= 7:
            if tmp == self.x:
                tmp += 1
                continue
            possible_moves.append((tmp, self.y))
            tmp += 1

        tmp = 0
        while 0 <= tmp <= 7:
            if tmp == self.y:
                tmp += 1
                continue
            possible_moves.append((self.x, tmp))
            tmp += 1


        tmp = 0
        while 0 <= tmp <= 7:
            
            if tmp == self.x:
                tmp += 1
                continue
            possible_moves.append((tmp, self.y - self.x + tmp)) if 0 <= self.y - self.x + tmp <= 7 else possible_moves
            possible_moves.append((tmp, self.x + self.y - tmp)) if 0 <= self.x + self.y - tmp <= 7 else possible_moves
            possible_moves.append((tmp, self.y - self.x + tmp)) if 0 <= self.y - self.x + tmp <= 7 else possible_moves

            tmp += 1
           


       

        tmp = list_.pop(list_.index(self))

        wrong_moves = []
        
        for move in possible_moves:
            for item in list_:
                if item.x == move[0] and item.y == move[1]:
                    wrong_moves.append(move)
                   
                    if move[0] == self.x:       
                        if self.y > move[1]:       
                            cur = move[1]     
                            while cur > 0:                                                    
                                cur -= 1
                                wrong_moves.append((move[0], cur))
                        if self.y < move[1]:                           
                            cur = move[1]                   
                            while cur < 7:                                         
                                cur += 1                    
                                wrong_moves.append((move[0], cur))
                    if move[1] == self.y:                
                        if self.x > move[0]:                                
                            cur = move[0]                
                            while cur > 0:                                               
                                cur -= 1          
                                wrong_moves.append((cur, move[1]))

                        if self.x < move[0]:                          
                            cur = move[0]     
                            while cur < 7:                                             
                                cur += 1
                                wrong_moves.append((cur, move[1]))
                    
                    if item.x > self.x and item.y < self.y:
                        x, y = item.x, item.y
                        while 0 < x < 7 and 0 < y < 7:
                            x += 1
                            y -= 1
                            wrong_moves.append((x, y))

                    if item.x > self.x and item.y > self.y:
                        x, y = item.x, item.y
                        while 0 < x < 7 and 0 < y < 7:
                            x += 1
                            y += 1
                            wrong_moves.append((x, y))
                    
                    if item.x < self.x and item.y < self.y:
                        x, y = item.x, item.y
                        while 0 < x < 7 and 0 < y < 7:
                            x -= 1
                            y -= 1
                            wrong_moves.append((x, y))
                    
                    if item.x < self.x and item.y > self.y:
                        x, y = item.x, item.y
                        while 0 < x < 7 and 0 < y < 7:
                            x -= 1
                            y += 1
                            wrong_moves.append((x, y))




        wrong_moves = set(wrong_moves)
        possible_moves = set(possible_moves)

        for move in wrong_moves:                                       
            possible_moves.remove(move)  
        
        attack_moves = self.can_attack(possible_moves)
        possible_moves = list(possible_moves)


        list_.append(tmp)
        return possible_moves, attack_moves, {}



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
            self.x, self.y = 7, ind
        else:
            self.image = pygame.image.load('assets/Chess_rdt60.png')
            self.pos = (board[0][ind-1][0], board[0][ind-1][1])
            self.x, self.y = 0, ind-1
        self.move = 0
        self.size = (self.pos[0], self.pos[0] + WIDTH), (self.pos[1], self.pos[1] + HEIGHT)
    
    def can_attack(self, possible_moves):
        attack_moves = []
        
        
        tmp = [self.x, self.y]
        if (tmp[0] + 1, tmp[1]) in possible_moves:
            tmp = tmp[0] + 1, tmp[1]
            while tmp in possible_moves:
                tmp = (tmp[0] + 1, tmp[1])
        else:
            tmp = tmp[0] + 1, tmp[1]

        for item in list_:
            if tmp[0] == item.x and tmp[1] == item.y and item.color != self.color:
                attack_moves.append(tmp)


        tmp = [self.x, self.y]
        if (tmp[0] - 1, tmp[1]) in possible_moves:
            tmp = tmp[0] - 1, tmp[1]
            while tmp in possible_moves:
                tmp = (tmp[0] - 1, tmp[1])
        else:
            tmp = tmp[0] - 1, tmp[1]
    
        for item in list_:
            if tmp[0] == item.x and tmp[1] == item.y and item.color != self.color:
                attack_moves.append(tmp)

        tmp = [self.x, self.y]
        if (tmp[0], tmp[1] + 1) in possible_moves:
            tmp = tmp[0], tmp[1] + 1
            while tmp in possible_moves:
                tmp = (tmp[0], tmp[1] + 1)
        else:
            tmp = tmp[0], tmp[1] + 1
            
        for item in list_:
            if tmp[0] == item.x and tmp[1] == item.y and item.color != self.color:
                attack_moves.append(tmp)

        tmp = [self.x, self.y]
        if (tmp[0], tmp[1] - 1) in possible_moves:
            tmp = tmp[0], tmp[1] - 1
            while tmp in possible_moves:
                tmp = (tmp[0], tmp[1] - 1)
        else:
            tmp = tmp[0], tmp[1] - 1
        
        for item in list_:
            if tmp[0] == item.x and tmp[1] == item.y and item.color != self.color:
                attack_moves.append(tmp)

        return attack_moves




    def possible_moves(self):
        attack_moves = []
        possible_moves = []

        tmp = 0
        while 0 <= tmp <= 7:
            if tmp == self.x:
                tmp += 1
                continue
            possible_moves.append((tmp, self.y))
            tmp += 1

        tmp = 0
        while 0 <= tmp <= 7:
            if tmp == self.y:
                tmp += 1
                continue
            possible_moves.append((self.x, tmp))
            tmp += 1


       

        tmp = list_.pop(list_.index(self))

        wrong_moves = []
        
        for move in possible_moves:
            for item in list_:
                if item.x == move[0] and item.y == move[1]:
                    wrong_moves.append(move)
                   
                    if move[0] == self.x:       
                        if self.y > move[1]:       
                            cur = move[1]     
                            while cur > 0:                                                    
                                cur -= 1
                                wrong_moves.append((move[0], cur))
                        if self.y < move[1]:                           
                            cur = move[1]                   
                            while cur < 7:                                         
                                cur += 1                    
                                wrong_moves.append((move[0], cur))
                    if move[1] == self.y:                
                        if self.x > move[0]:                                
                            cur = move[0]                
                            while cur > 0:                                               
                                cur -= 1          
                                wrong_moves.append((cur, move[1]))

                        if self.x < move[0]:                          
                            cur = move[0]     
                            while cur < 7:                                             
                                cur += 1
                                wrong_moves.append((cur, move[1]))



        wrong_moves = set(wrong_moves)
        

        for move in wrong_moves:                                       
            possible_moves.remove(move)  
        
        attack_moves = self.can_attack(possible_moves)
        
        list_.append(tmp)
        return possible_moves, attack_moves, {}

       

    
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
            self.x, self.y = 7, ind
        else:
            self.image = pygame.image.load('assets/Chess_bdt60.png')
            self.pos = (board[0][ind-1][0], board[0][ind-1][1])
            self.x, self.y = 0, ind-1
        self.size = (self.pos[0], self.pos[0] + WIDTH), (self.pos[1], self.pos[1] + HEIGHT)
     
    def can_attack(self, possible_moves):
        attack_moves = []

         
        tmp = [self.x, self.y]
        if (tmp[0] + 1, tmp[1] + 1) in possible_moves:
            tmp = tmp[0] + 1, tmp[1] + 1
            while tmp in possible_moves:
                tmp = (tmp[0] + 1, tmp[1] + 1)
        else:
            tmp = tmp[0] + 1, tmp[1] + 1

        for item in list_:
            if tmp[0] == item.x and tmp[1] == item.y and item.color != self.color:
                attack_moves.append(tmp)


        tmp = [self.x, self.y]
        if (tmp[0] + 1, tmp[1] - 1) in possible_moves:
            tmp = tmp[0] + 1, tmp[1] - 1
            while tmp in possible_moves:
                tmp = (tmp[0] + 1, tmp[1] - 1)
        else:
            tmp = tmp[0] + 1, tmp[1] - 1
    
        for item in list_:
            if tmp[0] == item.x and tmp[1] == item.y and item.color != self.color:
                attack_moves.append(tmp)

        tmp = [self.x, self.y]
        if (tmp[0] - 1, tmp[1] + 1) in possible_moves:
            tmp = tmp[0] - 1, tmp[1] + 1
            while tmp in possible_moves:
                tmp = (tmp[0] - 1, tmp[1] + 1)
        else:
            tmp = tmp[0] - 1, tmp[1] + 1
            
        for item in list_:
            if tmp[0] == item.x and tmp[1] == item.y and item.color != self.color:
                attack_moves.append(tmp)

        tmp = [self.x, self.y]
        if (tmp[0] - 1, tmp[1] - 1) in possible_moves:
            tmp = tmp[0] - 1, tmp[1] - 1
            while tmp in possible_moves:
                tmp = (tmp[0] - 1, tmp[1] - 1)
        else:
            tmp = tmp[0] - 1, tmp[1] - 1
        
        for item in list_:
            if tmp[0] == item.x and tmp[1] == item.y and item.color != self.color:
                attack_moves.append(tmp)
        
        return attack_moves




    def possible_moves(self):
        attack_moves = []
        possible_moves = []

        tmp = 0
        while 0 <= tmp <= 7:
            
            if tmp == self.x:
                tmp += 1
                continue
            possible_moves.append((tmp, self.y - self.x + tmp)) if 0 <= self.y - self.x + tmp <= 7 else possible_moves
            possible_moves.append((tmp, self.x + self.y - tmp)) if 0 <= self.x + self.y - tmp <= 7 else possible_moves
            possible_moves.append((tmp, self.y - self.x + tmp)) if 0 <= self.y - self.x + tmp <= 7 else possible_moves

            tmp += 1
           

        tmp = list_.pop(list_.index(self))

        wrong_moves = []
        
        for move in possible_moves:
            for item in list_:
                if item.x == move[0] and item.y == move[1]:
                    wrong_moves.append(move)
                    

                    if item.x > self.x and item.y < self.y:
                        x, y = item.x, item.y
                        while 0 < x < 7 and 0 < y < 7:
                            x += 1
                            y -= 1
                            wrong_moves.append((x, y))

                    if item.x > self.x and item.y > self.y:
                        x, y = item.x, item.y
                        while 0 < x < 7 and 0 < y < 7:
                            x += 1
                            y += 1
                            wrong_moves.append((x, y))
                    
                    if item.x < self.x and item.y < self.y:
                        x, y = item.x, item.y
                        while 0 < x < 7 and 0 < y < 7:
                            x -= 1
                            y -= 1
                            wrong_moves.append((x, y))
                    
                    if item.x < self.x and item.y > self.y:
                        x, y = item.x, item.y
                        while 0 < x < 7 and 0 < y < 7:
                            x -= 1
                            y += 1
                            wrong_moves.append((x, y))

        possible_moves = set(possible_moves)
        wrong_moves = set(wrong_moves)

        for move in wrong_moves:                                       
            possible_moves.remove(move)  
        
        attack_moves = self.can_attack(possible_moves)
        possible_moves = list(possible_moves)

        list_.append(tmp)
        return possible_moves, attack_moves, {}


     

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
            self.x, self.y = 7, ind
        else:
            self.image = pygame.image.load('assets/Chess_ndt60.png')
            self.pos = (board[0][ind-1][0], board[0][ind-1][1])
            self.x, self.y = 0, ind-1
        self.size = (self.pos[0], self.pos[0] + WIDTH), (self.pos[1], self.pos[1] + HEIGHT)

    def can_attack(self, possible_moves):
        attack_moves = []

        for move in possible_moves:
            for item in list_:
                if item.x == move[0] and item.y == move[1] and item.color != self.color:
                    possible_moves.remove(move)
                    attack_moves.append(move)

        return attack_moves


 
    def possible_moves(self):
        attack_moves = []
        possible_moves = [(self.x + 2, self.y + 1), (self.x + 2, self.y - 1), (self.x + 1, self.y + 2), \
                          (self.x + 1, self.y - 2), (self.x - 1, self.y + 2), (self.x - 1, self.y - 2), \
                          (self.x - 2, self.y + 1), (self.x - 2, self.y - 1)]

        moves = []
        for move in possible_moves:
            if (0 <= move[0] <= 7) and (0 <= move[1] <= 7):
                moves.append(move)
        possible_moves = moves
        
        tmp = list_.pop(list_.index(self))

        wrong_moves = []
        
        for move in possible_moves:
            for item in list_:
                if item.x == move[0] and item.y == move[1] and item.color == self.color:
                    wrong_moves.append(move)

        for move in wrong_moves:
            possible_moves.remove(move)
            
        attack_moves = self.can_attack(possible_moves)

        list_.append(tmp)
        return possible_moves, attack_moves, {}

      

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
            i.draw_moves()
        i.draw(i.image, i.pos)

def check_pieces(mouse_pos, side):
    for i in list_:
        if i.size[0][0] < mouse_pos[0] < i.size[0][1] and i.size[1][0] < mouse_pos[1] < i.size[1][1]:
            if side % 2 == i.color:
                i.choosed = True
                return i

def calculate_pos(mouse_pos):
    x, y = mouse_pos
    
    for i in range(len(board)):
        for j in range(len(board[i])):
            if x in range(board[i][j][0], board[i][j][0]+WIDTH+1):
                if y in range(board[i][j][1], board[i][j][1]+HEIGHT+1):
                    return board[i][j], i, j
    
create_pieces()




