# -*- coding: utf-8 -*-
"""
Created on Sun Apr  6 00:58:55 2014

@author: dchen
"""
import numpy as np

def terminal_eval(chess):
    """returns sum of individual evaluation functions"""
    if chess.isGameOver():
        if chess.getGameResult() == 1:
            score = 100000
        elif chess.getGameResult() == 2:
            score = -100000
        else:
            score = 0
        return score
    else:
        board = chess.getBoard()
        piece_dict = {}
        for row in board:
            for piece in row:
                if piece in piece_dict:
                    piece_dict[piece] += 1
                else:
                    piece_dict[piece] = 1
        score = simple_material_eval(chess,piece_dict) + simple_pos_eval(chess,board,piece_dict)
        return score
    
def simple_material_eval(chess,piece_dict):
    """returns a score for the board based on piece values. A positive score
    indicates a better board position for white, and a negative score indicates
    a better board position for black. It gets passed a list of list of
    characters which give you piece information."""
    score_dict = {'r':-5,'n':-3,'b':-3.25,'q':-9,'k':-10000,'p':-1,'.':0,'P':1,'R':5,'N':3,'B':3.25,'Q':9,'K':10000}
    m_score = 0
    for piece in piece_dict:
        m_score += score_dict[piece]*piece_dict[piece]
#    print "eval func returning score: " + str(score)
    return m_score
    
def simple_pos_eval(chess,board,piece_dict):
    """Analyzes positional control and returns numerical score"""
    p_score = 0
    #very simple activity scoring, could be detrimental
    for y in range(8):
        for x in range(8):
            p_score += 0.01*len(chess.getValidMoves([x,y]))*chess.getColorS(x,y)
    return p_score

    
