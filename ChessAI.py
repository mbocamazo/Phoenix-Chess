'''
Created on Mar 28, 2014

@author: dchen and mbocamazo

AI for chess
'''
import ChessBoard
from ChessClient import Player
import random

class ChessAI(Player):
    chessWIDTH = 8
    #write eval_func and should_prune_func and pass it into chessclient when it initalizes AIs
    def __init__(self,color,chess,eval_func,should_prune_func,ply):
        """AI gets passed the evaluation function and prune function it will use when searching 
        the game tree. Prune returns a true or false value telling you if the AI should continue
        searching the children of a node, while the eval_func returns the score of the board"""
        super(Player,self).__init__(color)
        self.color = color
        self.chess = chess
        self.eval_func = eval_func
        self.should_prune_func = should_prune_func 
        self.ply = ply
        
    def make_next_move(self):
        pass        
    
    def make_random_next_move(self):
        valid_moves = self.get_valid_moves()
        self.chess.addMove(random.choice(valid_moves))
        
    def get_next_move(self):
        """Get the next move from the AI. AI accesses board model to make its decision"""
        self.make_random_next_move()
#        if self.color == ChessBoard.WHITE:
#            player_num = 1
#        else:
#            player_num = -1
#        ply = 3
#        best_move, best_score = self.negamax(ply,player_num)
#        return best_move
        
    def negamax(self,depth,player_num):
        """using the pseudocode from wiki: http://en.wikipedia.org/wiki/Negamax"""
        best_score = None
        best_move = None
        if depth == 0 or self.chess.isGameOver() or self.should_prune_func(self.color,self.chess.getBoard()):
            return (player_num * self.eval_function(),best_move)
        possible_moves = self.get_valid_moves()
        
        for m in possible_moves:
            self.chess.addMove(m)
            score = -self.negamax(depth-1,-player_num)
            if score > best_score:
                best_score = score
                best_move = m
            self.chess.undo()
        return best_score,best_move
                 
            
    def get_valid_moves(self):
        """returns valid moves in the form [((xi,yi),(xf,yf)),...] where xi and yi represent the initial position of 
        the moved piece and xf and yf represent the final position"""
        moves = []
        for i in range(AI.BOARDWIDTH):
            for j in range(AI.BOARDWIDTH):
                valid_moves = self.chess.getValidMoves(i,j) 
                for m in valid_moves:
                    moves.append((i,j),tuple(m))
        return moves
            
        
    
        