'''
Created on Mar 28, 2014

@author: dchen and mbocamazo

AI for chess
'''
from ChessBoardModule import ChessBoard
import random
from abc import ABCMeta, abstractmethod

class Player(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def make_next_move(self):
        pass
    
class Human(Player):
    def __init__(self,color):
        self.color = color
    def make_next_move(self):
        print "You shouldn't be calling this function! I'm not an AI!"

class ChessAI(Player):
    BOARDWIDTH = 8
    #write eval_func and should_prune_func and pass it into chessclient when it initalizes AIs
    def __init__(self,color,chess,eval_func,should_prune_func,ply):
        """AI gets passed the evaluation function and prune function it will use when searching 
        the game tree. Prune returns a true or false value telling you if the AI should continue
        searching the children of a node, while the eval_func returns the score of the board"""
        self.color = color
        self.chess = chess
        self.eval_func = eval_func
        self.should_prune_func = should_prune_func 
        self.ply = ply
 
    def make_random_next_move(self):
        valid_moves = self.get_valid_moves()
        self.chess.addMove(random.choice(valid_moves))
        
    def make_next_move(self):
        """Get the next move from the AI. AI accesses board model to make its decision"""
        if self.color == ChessBoard.WHITE:
            player_num = 1
        else:
            player_num = -1
        best_moves = []
        best_score, best_moves = self.negamax(self.ply,player_num,best_moves,is_top_layer = True)
        print best_score
        best_move = random.choice(best_moves) #choose randomly amongst best_moves. If there's one element, the best move is chosen. If there are multiple elements with the same score, one element is randomly chosen 
        player_before_add_move = self.chess.getTurn()   
        ret = self.chess.addMove(best_move[0],best_move[1])
        if ret != True:
                print str(player_before_add_move)+" tried to make the illegal move" +str(best_move)
                print "Reason: "
                print self.chess.getReason()
        if self.color == ChessBoard.WHITE:
            print "white makes the move " + str((best_move[0],best_move[1]))        
        if self.color == ChessBoard.BLACK:
            print "black makes the move " + str((best_move[0],best_move[1]))
            
            
    def negamax(self,depth,player_num,best_moves,is_top_layer):
        """using the pseudocode from wiki: http://en.wikipedia.org/wiki/Negamax"""
        best_score = -1
        if depth == 0 or self.chess.isGameOver() or self.should_prune_func(self.color,self.chess.getBoard()):
			print (player_num * self.eval_func(self.chess.getBoard()), None)
            return player_num * self.eval_func(self.chess.getBoard())
			
		possible_moves = self.get_valid_moves()
        
        for m in possible_moves:
            ret = self.chess.addMove(m[0],m[1])
            if ret != True:
                print "tried to make the illegal move in negamax" +str(m)
                print "Reason: "
                print self.chess.getReason()
            score,move = -1*self.negamax(depth-1,-player_num,best_moves, is_top_layer = False)
            if score > best_score:
                best_score = score
                best_moves = [m]
                if is_top_layer:
					print str(best_score)
            elif score == best_score and is_top_layer: #only add tied scores on the first layer. otherwise you end up adding future moves and opponent moves.
                best_moves.append(m)
            self.chess.undo()
#        print "printing the best move before negamax returns it!"
#        print best_moves
		print (best_score,best_moves)
        return (best_score,best_moves)
                 
            
    def get_valid_moves(self):
        """returns valid moves in the form [((xi,yi),(xf,yf)),...] where xi and yi represent the initial position of 
        the moved piece and xf and yf represent the final position"""
        moves = []
        for i in range(ChessAI.BOARDWIDTH):
            for j in range(ChessAI.BOARDWIDTH):
                valid_moves = self.chess.getValidMoves((i,j)) 
                for m in valid_moves:
                    moves.append(((i,j),tuple(m)))
        return moves
            
        
    
        
