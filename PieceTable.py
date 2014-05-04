# -*- coding: utf-8 -*-
"""
Created on Sat May  3 22:11:30 2014

@author: dchen
"""
import numpy as np

class PieceTable():
    pawn_board_black = np.array([
       [-0. , -0. , -0. , -0. , -0. , -0. , -0. , -0. ],
       [-0.5, -1. , -1. ,  2.5,  2.5, -1. , -1. , -0.5],
       [-0.5,  0.5,  1. , -0. , -0. ,  1. ,  0.5, -0.5],
       [-0. , -0. , -0. , -2.5, -2.5, -0. , -0. , -0. ],
       [-0.5, -0.5, -1. , -2.7, -2.7, -1. , -0.5, -0.5],
       [-1. , -1. , -2. , -3. , -3. , -2. , -1. , -1. ],
       [-5. , -5. , -5. , -5. , -5. , -5. , -5. , -5. ],
       [-0. , -0. , -0. , -0. , -0. , -0. , -0. , -0. ]])
    pawn_board_white = np.array([
       [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
       [ 5. ,  5. ,  5. ,  5. ,  5. ,  5. ,  5. ,  5. ],
       [ 1. ,  1. ,  2. ,  3. ,  3. ,  2. ,  1. ,  1. ],
       [ 0.5,  0.5,  1. ,  2.7,  2.7,  1. ,  0.5,  0.5],
       [ 0. ,  0. ,  0. ,  2.5,  2.5,  0. ,  0. ,  0. ],
       [ 0.5, -0.5, -1. ,  0. ,  0. , -1. , -0.5,  0.5],
       [ 0.5,  1. ,  1. , -2.5, -2.5,  1. ,  1. ,  0.5],
       [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ]])
    knight_board_black = np.array([
       [ 3. ,  3. ,  3. ,  3. ,  3. ,  3. ,  3. ,  3. ],
       [ 3. ,  2. , -0. , -0. , -0. , -0. ,  2. ,  3. ],
       [ 3. , -0. , -1. , -1.5, -1.5, -1. , -0. ,  3. ],
       [ 3. , -0.5, -1.5, -2. , -2. , -1.5, -0.5,  3. ],
       [ 3. , -0. , -1.5, -2. , -2. , -1.5, -0. ,  3. ],
       [ 3. , -0.5, -1. , -1.5, -1.5, -1. , -0.5,  3. ],
       [ 3. ,  2. , -0. , -0.5, -0.5, -0. ,  2. ,  3. ],
       [ 3. ,  3. ,  3. ,  3. ,  3. ,  3. ,  3. ,  3. ]])
    knight_board_white = np.array([
       [-3. , -3. , -3. , -3. , -3. , -3. , -3. , -3. ],
       [-3. , -2. ,  0. ,  0. ,  0. ,  0. , -2. , -3. ],
       [-3. ,  0. ,  1. ,  1.5,  1.5,  1. ,  0. , -3. ],
       [-3. ,  0.5,  1.5,  2. ,  2. ,  1.5,  0.5, -3. ],
       [-3. ,  0. ,  1.5,  2. ,  2. ,  1.5,  0. , -3. ],
       [-3. ,  0.5,  1. ,  1.5,  1.5,  1. ,  0.5, -3. ],
       [-3. , -2. ,  0. ,  0.5,  0.5,  0. , -2. , -3. ],
       [-3. , -3. , -3. , -3. , -3. , -3. , -3. , -3. ]])
    bishop_board_black = np.array([
       [ 2. ,  1. ,  4. ,  1. ,  1. ,  4. ,  1. ,  2. ],
       [ 1. , -1.0,  0. ,  0. ,  0. ,  0. , -1.0,  1. ],
       [ 1. , -1. , -1. ,  1. ,  1. , -1. , -1. ,  1. ],
       [ 1. ,  0. , -1. , -1. , -1. , -1. ,  0. ,  1. ],
       [ 1. , -0.5, -0.5, -1. , -1. , -0.5, -0.5,  1. ],
       [ 1. ,  0. , -0.5, -1. , -1. , -0.5,  0. ,  1. ],
       [ 1. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  1. ],
       [ 2. ,  1. ,  1. ,  1. ,  1. ,  1. ,  1. ,  2. ]])
    bishop_board_white = np.array([
       [-2. , -1. , -1. , -1. , -1. , -1. , -1. , -2. ],
       [-1. , -0. , -0. , -0. , -0. , -0. , -0. , -1. ],
       [-1. , -0. ,  0.5,  1. ,  1. ,  0.5, -0. , -1. ],
       [-1. ,  0.5,  0.5,  1. ,  1. ,  0.5,  0.5, -1. ],
       [-1. , -0. ,  1. ,  1. ,  1. ,  1. , -0. , -1. ],
       [-1. ,  1. ,  1. , -1. , -1. ,  1. ,  1. , -1. ],
       [-1. ,  1.0, -0. , -0. , -0. , -0. ,  1.0, -1. ],
       [-2. , -1. , -4. , -1. , -1. , -4. , -1. , -2. ]])
    king_board_black = np.array([
       [ 0.,  0., -4.,  0.,  0.,  0., -4.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]])
    king_board_white = np.array([
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  4.,  0.,  0.,  0.,  4.,  0.]])
    king_board_black_end = np.array([
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]])
    king_board_white_end = np.array([
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]])
    
    table_dict = {'p':pawn_board_black,'P':pawn_board_white,
    'n':knight_board_black,'N':knight_board_white,
    'b':bishop_board_black,'B':bishop_board_white}
    table_dict_king = {'k':king_board_black,'K':king_board_white}
    table_dict_king_end = {'k':king_board_black_end,'K':king_board_white_end}
    
    def __init__(self):
        pass
    
    def get_location_score(self,piece,location,is_end_game):
        if piece == 'q' or piece =='Q' or piece == 'r' or piece == 'R':
            return 0
        elif piece == 'k' or piece == 'K':
            if is_end_game:
                loc_dict = self.table_dict_king_end[piece]
                return loc_dict[location[0]][location[1]]
            else:
                loc_dict = self.table_dict_king[piece]
                return loc_dict[location[0]][location[1]]
        else:
            loc_dict = self.table_dict[piece]
            return loc_dict[location[0]][location[1]]
            
def test_piece_tables():
    """unit tests for the piece tables class"""
    p = PieceTable()
    print "expecting 5.0"
    print p.get_location_score('n',(0,0),False)
    print "expecting 0"
    print p.get_location_score('q',(0,0),False)
    print "expecting 5"
    print p.get_location_score('k',(0,0),True)        
    print "expecting -2"        
    print p.get_location_score('k',(0,0),False)   
