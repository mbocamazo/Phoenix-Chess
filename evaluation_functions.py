# -*- coding: utf-8 -*-
"""
Created on Sun Apr  6 00:58:55 2014

@author: dchen
"""

def simple_piece_eval(board):
    """returns a score for the board based on piece values. A positive score
    indicates a better board position for white, and a negative score indicates
    a better board position for black. It gets passed a list of list of
    characters which give you piece information."""
    score_dict = {'r':-5,'n':-3,'b':-3.25,'q':-9,'k':-10000,'p':-1,'.':0,'P':1,'R':5,'N':3,'B':3.25,'Q':9,'K':10000}
    piece_dict = {}
    for row in board:
        for piece in row:
            if piece in piece_dict:
                piece_dict[piece] += 1
            else:
                piece_dict[piece] = 1
    score = 0
    for piece in piece_dict:
        score += score_dict[piece]*piece_dict[piece]
#    print "eval func returning score: " + str(score)
    return score
