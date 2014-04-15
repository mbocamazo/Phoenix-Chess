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
        score = 0
        board = chess.getShallowBoard()
        piece_dict = {}
        for row in board:
            for piece in row:
                if piece in piece_dict:
                    piece_dict[piece] += 1
                else:
                    piece_dict[piece] = 1
        score += simple_material_eval(chess,piece_dict)
#        score += simple_pos_eval(chess,board,piece_dict)
        return score
        
def terminal_eval2(chess):
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
        score = 0
        board = chess.getShallowBoard()
        piece_dict = {}
        for row in board:
            for piece in row:
                if piece in piece_dict:
                    piece_dict[piece] += 1
                else:
                    piece_dict[piece] = 1
        score += simple_material_eval(chess,piece_dict)
        score += simple_pos_eval(chess,board,piece_dict)
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
    return m_score
    
def simple_pos_eval(chess,board,piece_dict):
    """Analyzes positional control and returns numerical score"""
    p_score = 0
    p_score += simple_activity_eval(chess,board,piece_dict)
#    p_score += pawn_structure_eval(chess,board,piece_dict)
    return p_score
    
def simple_activity_eval(chess,board,piece_dict):
    """Analyzes absolute activity of pieces"""
        #very simple activity scoring, could be detrimental
    act_score = 0
    for y in range(8):
        for x in range(8):
            act_score += 0.01*chess.getValidMovesS([x,y])
    return act_score
    
def pawn_structure_eval(chess,board,piece_dict):
    """Analyzes pawn structure and promotion chances"""
    pawn_score = 0
    wpp = [0,0,0,0,0,0,0,0,0,0] #white pawn profile, length 10 to shift with pawn islands and promotions
    bpp = [0,0,0,0,0,0,0,0,0,0] #black pawn profile
    W_islands = 0
    B_islands = 0
    W_extra = 0
    B_extra = 0
    W_passers = 0
    B_passers = 0
    for y in range(8):
        for x in range(8): #for x position in row
            if board[y][x] == 'p':
                bpp[x+1] += 1
#                pawn_score += -()
            if board[y][x] == 'P':
                wpp[x+1] += 1
    for x in range(9):
        W_islands += xor(wpp[x],wpp[x+1]) #double-counts pawn islands by shifting by one and xor-ing
        B_islands += xor(bpp[x],bpp[x+1])
    for x in range(8):
        W_extra += (wpp[x+1]-1)*bool(wpp[x+1]) #counts super-one pawns in each file
        B_extra += (bpp[x+1]-1)*bool(bpp[x+1])
        W_passers += bool(wpp[x+1]) and not(bpp[x]+bpp[x+1]+bpp[x+2]) #no opponent pawns -1, 0, 1
        B_passers += bool(bpp[x+1]) and not(wpp[x]+wpp[x+1]+wpp[x+2]) #also, single-counts stacked passers, intentional bc strat accurate
    
    pawn_score += -bool(W_islands-2)*0.2*W_islands/2.0+bool(B_islands-2)*0.2*B_islands/2.0
    pawn_score += -W_extra*0.4+B_extra*0.4
    pawn_score += W_passers-B_passers
    return pawn_score
    
def xor(p,q):
    return (not(p) and q) or (p and not(q))

         