# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 21:08:48 2014

@author: dchen

base class from which we's gonna run some genetic algorithms
"""
from ChessBoard import ChessBoard
from ChessAI import *
import random
import pygame
from ChessClient import *
import evaluation_functions
import prune_functions
import QFunctions

class SwissTournament:
    """runs a swiss tournament between a specified number of
    AI w/random pair weightings. Specified number must be an even number. 
    Stores a list of AI sorted by rank, once the games have been played.
    Also stores all games played for examination and testing."""
    def __init__(self,AI_num,round_num):
        assert AI_num%2 == 0
        self.AI_list = []
        for i in range(AI_num):
            random_piece_dict = build_random_pair_piece_dict()
            AI = ChessAI(None,None,evaluation_functions.terminal_paired_material_eval,
                 prune_functions.never_prune,QFunctions.simple_end_game,random_piece_dict,2)
            self.AI_list.append(AI)
        self.game_list = []
        self.round_num = round_num
            
    def play_tourn(self):
        for i in range(self.round_num):
            for j in range(0,2,len(self.AI_list)):
                p1 = self.AI_list[j]
                p2 = self.AI_list[j+1]
                g = Game(p1,p2)
                self.game_list.append(g)
                g.play_game()
                self.AI_list.sort(key=lambda x: x.swiss_tourn_score, reverse=True)
            
            

class Game:
    """given two AI players, runs a game between them and stores the result.
    Modifies the swiss tourny scores and colors of the AI that play."""
    
    BLACK_WIN = -1
    WHITE_WIN = 1
    DRAW = 0
    
    def __init__(self,w_player,b_player):
        self.w_player = w_player
        self.b_player = b_player
        self.w_player.color = ChessBoard.WHITE
        self.b_player.color = ChessBoard.BLACK
        self.game_result = None
        self.saved_moves = None
        
    def play_game(self):
        chess = ChessBoard()
        self.w_player.chess = chess
        self.b_player.chess = chess
        while not chess.isGameOver():
            self.w_player.make_next_move()
            self.b_player.make_next_move()
        r = chess.getGameResult()
        print r
        if r == 1:
            self.game_result = Game.WHITE_WIN
            self.w_player.swiss_tourn_score += 1
        if r == 2:
            self.game_result = Game.BLACK_WIN
            self.b_player.swiss_tourn_score += 1
        if r in [3,4,5]:
            self.w_player.swiss_tourn_score += .5
            self.b_player.swiss_tourn_score += .5
            self.game_result = Game.DRAW
        self.saved_moves = chess.getAllTextMoves()
        
    def get_game_result(self):
        return self.game_result
        
def build_random_pair_piece_dict():
    """generates a random pair piece dictionary that is used by the
    pair material eval function. AI will store and pass this
    dictionary/attribute to the pair material eval func. currently no distinguishing
    between different bishops and only takes presence of pieces of board into account
    (ex. doesn't distinguish between the enemy having two rooks or one rook when
    weighting the value of my queen)"""
    piece_list = ['r','n','b','q','R','N','B','Q']
    pair_piece_dict = {}
    for p in piece_list:
        no_p = list(piece_list)
        no_p.remove(p) #create copy of list without the piece in it
        inner_piece_dict = {}
        for n in no_p:
            inner_piece_dict[n] = random.uniform(-.5,.5) #random double between -1 and 1 for pair piece vals          
        pair_piece_dict[p] = inner_piece_dict
    return pair_piece_dict     
    
def watch_game(saved_moves):
    chess = ChessBoard()
    screen = pygame.display.set_mode((480, 480),1)
    pygame.display.set_caption('Saved Game')
    view = PyGameWindowView(chess,screen)
    print view
    running = True
    move_index = 0
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                pygame.quit()
                return
        raw_input("Press enter to watch next move...")
        if move_index < len(saved_moves):
            chess.addTextMove(saved_moves[move_index])
        else:
            break
        move_index += 1
        view.draw(chess)
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__': 
    t = SwissTournament(2,2)
    print t.AI_list
    print t.game_list
    t.play_tourn()
    print t.AI_list
    print t.game_list
#    piece_dict_w = build_random_pair_piece_dict()
#    piece_dict_b = build_random_pair_piece_dict()
#    AI_w_ply = 2
#    AI_b_ply = 2
#    #AI colors and chess models are set inside of the Game object
#    player_w = ChessAI(None,None,evaluation_functions.terminal_paired_material_eval,
#                       prune_functions.never_prune,QFunctions.simple_end_game,piece_dict_w,
#                       AI_w_ply)
#    player_b = ChessAI(None,None,evaluation_functions.terminal_paired_material_eval,
#                       prune_functions.never_prune,QFunctions.simple_end_game,piece_dict_b,
#                       AI_b_ply)
#    test_g = Game(player_w,player_b)
#    test_g.play_game()
#    print test_g.saved_moves
#    print "game result: " + str(test_g.get_game_result())
#    watch_game(test_g.saved_moves)
