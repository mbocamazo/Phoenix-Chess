# -*- coding: utf-8 -*-
"""
Created on Sun Apr  6 00:58:55 2014

@author: dchen
"""
import numpy as np
from PieceTable import PieceTable

def terminal_eval_simple(chess,alpha,beta,layers_remaining):
    """returns sum of individual evaluation functions"""
    if chess.isGameOver():
        if chess.getGameResult() == 1:
            score = 100000 + layers_remaining #faster checks are worth more
        elif chess.getGameResult() == 2:
            score = -100000 - layers_remaining
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
#        if len(chess._state_stack) < 12:
        score += piece_table_pos_eval(chess,piece_dict)/10.0 #to fix high piece weights
#        else:
        score += simple_pos_eval(chess,board,piece_dict)
        return score

def piece_table_pos_eval(chess,piece_dict):
    piece_table_score = 0
    board = chess.getShallowBoard()
    location_dict = {}
    p = PieceTable()
    for row_num, row in enumerate(board):
        for col_num, piece in enumerate(row):
            if piece not in ['.','q','Q','r','R']:
                location_dict[piece] = (row_num,col_num)
    is_end_game = end_game_piece_count(chess)
    for piece in location_dict:
        piece_table_score += p.get_location_score(piece,location_dict[piece],is_end_game)
    return piece_table_score
        
def terminal_eval(chess,alpha,beta):
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

        if score < alpha - 2 or score > beta + 2:
            return score

        score += simple_pos_eval(chess,board,piece_dict)
        return score
        
def terminal_dict_material_eval(chess,alpha,beta,piece_weights):
    """returns sum of individual evaluation functions
    this one calls a modified material eval that considers pairs of pieces 
    in evaluating piece vals.AI passes this function its unique
    piece_weights dictionary when calling it"""
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
        score += dict_material_eval(piece_dict,piece_weights)

        if score < alpha - 2 or score > beta + 2:
            return score

        score += simple_pos_eval(chess,board,piece_dict)
        return score        
        
def dict_material_eval(piece_dict,score_dict):
    """scores the board based on pieces present. The AI
    class passes this function piece_weights when called through terminal_paired_material_eval, a dictionary
    that is unique to every AI. pieces have
    some intrinsic value as defined by the dictionary."""
    dict_copy = {}
    for p in score_dict:
        dict_copy[p] = score_dict[p]
        dict_copy[p.upper()] = -score_dict[p] #flip the lower case scores to give the reverse for upper case scores
    dict_copy['p']=-1
    dict_copy['P']= 1
    dict_copy['k']=-10000
    dict_copy['K']= 10000
    m_score = 0
    piece_dict.pop('.',None) #remove all pieces that aren't relevant to pair weighting
    for piece in piece_dict:
        m_score += dict_copy[piece]*piece_dict[piece]    
    return m_score
        
def terminal_paired_material_eval(chess,alpha,beta,paired_piece_weights):
    """returns sum of individual evaluation functions
    this one calls a modified material eval that considers pairs of pieces 
    in evaluating piece vals.AI passes this function its unique
    paired_piece_weights dictionary when calling it"""
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
        score += paired_material_eval(piece_dict,paired_piece_weights)

        if score < alpha - 2 or score > beta + 2:
            return score

        score += simple_pos_eval(chess,board,piece_dict)
        return score
        
def paired_material_eval(piece_dict,paired_score_dict):
    """scores the board based on pieces and pairs of pieces present. The AI
    class passes this function paired_piece_weights when called through terminal_paired_material_eval, a dictionary
    that is unique to every AI. pieces have
    some intrinsic value and that value is modified based on the presence or lackthereof
    of all other pieces. (exclulding pawns and kings)"""
    single_score_dict = {'r':-5,'n':-3,'b':-3.25,'q':-9,'k':-10000,'p':-1,'.':0,'P':1,'R':5,'N':3,'B':3.25,'Q':9,'K':10000}
    m_score = 0
    for piece in piece_dict:
        m_score += single_score_dict[piece]*piece_dict[piece]    
    piece_dict.pop('.',None)
    piece_dict.pop('k',None)
    piece_dict.pop('K',None)
    piece_dict.pop('p',None)
    piece_dict.pop('P',None)#remove all pieces that aren't relevant to pair weighting
    for p in piece_dict:
        pair_dict = paired_score_dict[p]
        for pair_piece in pair_dict:
            if pair_piece in piece_dict:
                m_score += pair_dict[pair_piece]*piece_dict[pair_piece]
    return m_score
        
def terminal_eval2(chess,alpha,beta):
    """returns sum of individual evaluation functions"""
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
        score += simple_pos_eval3(chess,board,piece_dict)
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
    p_score = 01
    p_score += pawn_promo_eval(chess,board,piece_dict) #either, but not both (double counting)
#    p_score += pawn_structure_eval(chess,board,piece_dict)
    return p_score
    
def simple_pos_eval2(chess,board,piece_dict):
    """Analyzes positional control and returns numerical score"""
    p_score = 0
    p_score += simple_activity_eval(chess,board,piece_dict)
#    p_score += pawn_promo_eval(chess,board,piece_dict) #either, but not both (double counting)
    p_score += pawn_structure_eval(chess,board,piece_dict)
    return p_score
    
def simple_pos_eval3(chess,board,piece_dict):
    """Analyzes positional control and returns numerical score"""
    p_score = 0
    p_score += simple_activity_eval(chess,board,piece_dict)
    p_score += pawn_promo_eval(chess,board,piece_dict) #either, but not both (double counting)
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
    #promo eval
    for x in range(8):
        if bool(wpp[x+1]) and not(bpp[x]+bpp[x+1]+bpp[x+2]): #no opponent pawns -1, 0, 1
            for y in range(8):
                if board[y][x]=='P':
                    pawn_score += 0.1*(8-y)
#                    break #(valid?)
        if bool(bpp[x+1]) and not(wpp[x]+wpp[x+1]+wpp[x+2]):
            for y in range(8):
                if board[7-y][x]=='p':
                    pawn_score += -0.1*y
    return pawn_score
    
def pawn_promo_eval(chess,board,piece_dict):
    """Analyzes pawn structure and promotion chances"""
    pawn_score = 0
    wpp = [0,0,0,0,0,0,0,0,0,0] #white pawn profile, length 10 to shift with pawn islands and promotions
    bpp = [0,0,0,0,0,0,0,0,0,0] #black pawn profile
    for y in range(8):
        for x in range(8): #for x position in row
            if board[y][x] == 'p':
                bpp[x+1] += 1
#                pawn_score += -()
            if board[y][x] == 'P':
                wpp[x+1] += 1
    for x in range(8):
        if bool(wpp[x+1]) and not(bpp[x]+bpp[x+1]+bpp[x+2]): #no opponent pawns -1, 0, 1
            for y in range(8):
                if board[y][x]=='P':
                    pawn_score += 0.1*(8-y)
#                    break #(valid?)
        if bool(bpp[x+1]) and not(wpp[x]+wpp[x+1]+wpp[x+2]):
            for y in range(8):
                if board[7-y][x]=='p':
                    pawn_score += -0.1*y
    return pawn_score
    
def xor(p,q):
    return (not(p) and q) or (p and not(q))
    
def end_game_piece_count(chess):
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
    if w_piece_count + b_piece_count < 10:
        return True
    if w_piece_count <= 4 or b_piece_count <= 4:
        return True
    return False

         