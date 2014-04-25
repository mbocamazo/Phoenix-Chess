# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 20:34:17 2014

@author: dchen
"""

END_GAME_PIECE_COUNT = 8
MAXIMUM_DEPTH_EXTENSION = -2

def simple_end_game(chess,depth):
    if chess.isGameOver():
        return False
#    print "qfunc depth: "+str(depth)
    if depth <= MAXIMUM_DEPTH_EXTENSION or depth > 0:
        return False
    if piece_count(chess) < END_GAME_PIECE_COUNT: #if the board has less than a certain amount of pieces, trigger deeper ply search
        return True

def no_extension(chess,depth):
    return False    
    
def piece_count(chess):
    board = chess.getShallowBoard()
    w_piece_count = 0
    b_piece_count = 0
    for row in board:
        for piece in row:
            if piece != '.':
                if 'A'<= piece <='Z':
                    w_piece_count += 1
                elif 'a'<= piece <='z':
                    b_piece_count += 1
    return w_piece_count+b_piece_count
#    return min(w_piece_count,b_piece_count)