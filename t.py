

                                                                                                   
    if move[0] == coords[0]:                                                                                               
        if coords[1] > move[1]:                                                                                            
            cur = move[1]                                                                                                  
            while cur > 0:                                                                                                 
                cur -= 1                                                                                                   
                wrong_moves.append((move[0], cur)) if (move[0], cur) not in wrong_moves else wrong_moves                           if coords[1] < move[1]:                                                                                            
            cur = move[1]                                                                                                  
            while cur < 7:                                                                                                 
                cur += 1                                                                                                   
                wrong_moves.append((move[0], cur)) if (move[0], cur) not in wrong_moves else wrong_moves                   
                                                                                                                           
                                                                                                                           
                                                                                                                           
                                                                                                                           
    elif move[1] == coords[1]:                                                                                             
         if coords[0] > move[0]:                                                                                           
            cur = move[0]                                                                                                  
            while cur > 0:                                                                                                 
                cur -= 1                                                                                                   
                wrong_moves.append((cur, move[1])) if (cur, move[1]) not in wrong_moves else wrong_moves                   
         if coords[0] < move[0]:                                                                                           
            cur = move[0]                                                                                                  
            while cur < 7:                                                                                                 
                cur += 1                                                                                                   
                wrong_moves.append((cur, move[1])) if (cur, move[1]) not in wrong_moves else wrong_moves                   
                                                                                                                           
                                                                                                                           
for move in wrong_moves:                                                                                                   
    possible_moves.remove(move)   
