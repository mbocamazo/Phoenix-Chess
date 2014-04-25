'''
Created on Mar 28, 2014

@author: dchen and mbocamazo

AI for chess
'''
from ChessBoard import ChessBoard
import random
from abc import ABCMeta, abstractmethod
import numpy as np
import time

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
    def __init__(self,color,chess,eval_func,should_prune_func,q_func,piece_weights,ply):
        """AI gets passed the evaluation function and prune function it will use when searching 
        the game tree. Prune returns a true or false value telling you if the AI should continue
        searching the children of a node, while the eval_func returns the score of the board"""
        self.color = color
        self.chess = chess
        self.eval_func = eval_func
        self.should_prune_func = should_prune_func 
        self.should_go_deeper = q_func
        self.piece_weights = piece_weights
        self.ply = ply
 
    def make_random_next_move(self):
        self.chess.addMove(self.get_random_next_move())
        
    def get_random_next_move(self):
        valid_moves = self.get_valid_moves()
        if len(valid_moves) == 0:
            return None
        return random.choice(valid_moves())        
        
    def make_next_move(self):
        """Get the next move from the AI. AI accesses board model to make its decision"""
        if self.color == ChessBoard.WHITE:
            player_num = 1
        else:
            player_num = -1
##        best_moves = []
#        best_score,best_move = self.negamax(self.ply,player_num,is_top_layer = True)
        start_time = time.time()
        best_score,best_move = self.negamax_ab_move_order(self.ply,player_num,-np.inf,np.inf,is_top_layer=True)
        current_time = time.time()
        print "thinking time:   %.10f" % (current_time - start_time)
        print "nodes/second:    " + str(self.chess.nodesSearched/(current_time-start_time))
        print "score of best move: " + str(best_score)
        self.chess.nodesSearched = 0
#        print "best move " + str(best_move)
#        best_move = random.choice(best_moves) #choose randomly amongst best_moves. If there's one element, the best move is chosen. If there are multiple elements with the same score, one element is randomly chosen 
        player_before_add_move = self.chess.getTurn()  
        if best_move != None:
            ret = self.chess.addMove(best_move[0],best_move[1])
            if ret != True:
                    print str(player_before_add_move)+" tried to make the illegal move" +str(best_move)
                    print "Reason: "
                    print self.chess.getReason()
            if self.color == ChessBoard.WHITE:
                print "white makes the move " + self.chess._formatAIMove(best_move)       
            if self.color == ChessBoard.BLACK:
                print "black makes the move " + self.chess._formatAIMove(best_move)
            
    def negamax_ab_2(self,depth,player_num,alpha,beta,is_top_layer=False):
        """negamax function.  Depth is a positive integer."""
        self.chess.nodesSearched += 1
        if depth == 0 or self.chess.isGameOver() or self.should_prune_func(self.chess): #and not continue q search (chess)
            score = self.eval_func(self.chess)
            if score == None: print "eval func None Type found"; score = 0  
            board_weight = player_num * score
            return board_weight
        valid_moves = self.get_valid_moves()
        for candidate in valid_moves:
            self.chess.addMove(candidate[0],candidate[1])
            score = -1*self.negamax_ab_2(depth-1,-player_num,-beta,-alpha)
            self.chess.undo()
            if score > alpha:
                alpha = score
                best_move = candidate
            if alpha >= beta:
                break
        if is_top_layer:
            print "nodes evaluated: "+str(self.chess.nodesSearched)
#            self.chess.nodesSearched = 0
            return alpha,best_move
        else:
            return alpha
            
    def negamax_ab_move_order(self,depth,player_num,alpha,beta,is_top_layer=False):
        """negamax function.  Depth is a positive integer."""
        self.chess.nodesSearched += 1
        if (depth <= 0 or self.chess.isGameOver() or self.should_prune_func(self.chess)) and not self.should_go_deeper(self.chess,depth): 
    #            board_weight = player_num * self.eval_func(self.chess,alpha,beta)     #use this line for all other eval funcs       
                board_weight = player_num * self.eval_func(self.chess,alpha,beta,self.piece_weights) #this line is for the paired_piece_eval func        
                if is_top_layer:
                    "print: WARNING, negamax cut off search on first node, returning a random move!"
                    return board_weight,self.get_random_next_move()
                else:
                    return board_weight
        valid_moves = self.get_valid_moves()
        scored_valid_moves = self.score_move_order(valid_moves)
        capture_moves_left_in_dict = True
        while len(scored_valid_moves) > 0:
            if capture_moves_left_in_dict:
                candidate, move_order_score = self.return_and_del_largest_element(scored_valid_moves)
                if move_order_score < -100: #no more capture moves are left. 
                    capture_moves_left_in_dict = False
            else:
                #stop looking for max values in the dictionary. just grab any move and remove it from the dict.
                candidate = scored_valid_moves.keys()[0]
                scored_valid_moves.pop(candidate)
            self.chess.addMove(candidate[0],candidate[1])
            score = -1*self.negamax_ab_move_order(depth-1,-player_num,-beta,-alpha)
            self.chess.undo()
            if score > alpha:
                alpha = score
                best_move = candidate
            if alpha >= beta:
                break
        if is_top_layer:
            print "nodes evaluated: "+str(self.chess.nodesSearched)
#            self.chess.nodesSearched = 0
            return alpha,best_move
        else:
            return alpha
                       
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
            
    def score_move_order(self,valid_moves):
        """returns a list of dictionaries, where the keys are moves of format ((i,j),(k,l)) and values are the negative of the material score 
        of the piece doing the capture in that move (ex: score of a pawn capturing something is -1, score of queen capturing is -9,
        score of no capture move is -1000 (arbitrarily largely negative, but we avoided numpy.inf because it is compared to numpy.inf later).
        Example output: {((i,j),(k,l)):-1,((i,j),(k,l)):-1000,((i,j),(k,l)):-3}. this score move order heuristic assumes that capturing
        with a low value piece is more likely to indicate a high alpha for the player and to trigger alpha cutoffs early."""
        score_dict = {'P':-1,'R':-5,'N':-3,'B':-3.25,'Q':-9,'K':-100}    
        
        score_list = [None]*len(valid_moves)
        for i, m in enumerate(valid_moves):
            move_from = m[0]
            move_dest = m[1]
            #line below checks to see if a piece is being captured by the valid move.
            if self.chess.getColor(move_dest[0],move_dest[1]) != ChessBoard.NOCOLOR and self.chess.getColor(move_dest[0],move_dest[1]) != self.color:
                piece = self.chess._board[move_from[1]][move_from[0]].upper() 
                score = score_dict[piece]
            else:
                score = -1000
            if self.chess.isCheck():
                score = 0
            score_list[i] = score
        moves_and_scores = dict(zip(valid_moves,score_list))
        return moves_and_scores
        
    def return_and_del_largest_element(self,scored_valid_moves):
        """returns highest scored move in the dictionary and removes it. gets a dictionary of moves and scores, returns just a move.
        example input: {((i,j),(k,l)):-1,((a,b),(c,d)):-1000,((e,f),(g,h)):-3} output: ((i,j),(k,l)). It's fine to store this info
        in a dictionary because we're not interested in sorting the whole dictionary at once anyway. just find the max as needed."""
        max_score = -np.inf
        highest_scored_move = None
        for move in scored_valid_moves:
            score = scored_valid_moves[move]
            if score > max_score:
                max_score = score
                highest_scored_move = move
        scored_valid_moves.pop(highest_scored_move)
        return highest_scored_move, max_score
        
            
    
        
