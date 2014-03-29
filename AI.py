'''
Created on Mar 28, 2014

@author: dchen and mbocomazo

AI for chess
'''
import ChessBoard

class AI():
    BOARDWIDTH = 8
    
    def __init__(self,name,color,board, opponent):
        self.name = name
        self.color = color
        self.Board = board
        self.opponent = opponent
        
    def get_next_move(self):
        """Get the next move from the AI. AI accesses board model to make its decision"""
        if self.color == ChessBoard.WHITE:
            player_num = 1
        else:
            player_num = -1
        ply = 3
        best_move, best_score = self.negamax(ply,player_num)
        return best_move
        
    def negamax(self,depth,player_num):
        """using the pseudocode from wiki: http://en.wikipedia.org/wiki/Negamax"""
        best_score = None
        best_move = None
        if depth == 0 or self.Board.isGameOver():
            return (player_num * self.evaluate_board(),best_move)
        possible_moves = self.get_valid_moves()
        
        for m in possible_moves:
            self.board.addMove(m)
            score = -self.negamax(depth-1,-player_num)
            if score > best_score:
                best_score = score
                best_move = m
            self.board.undo()
        return best_score,best_move
                 
            
    def get_valid_moves(self):
        """returns valid moves in the form [((xi,yi),(xf,yf)),...] where xi and yi represent the initial position of 
        the moved piece and xf and yf represent the final position"""
        moves = []
        for i in range(AI.BOARDWIDTH):
            for j in range(AI.BOARDWIDTH):
                valid_moves = self.board.getValidMoves(i,j) 
                for m in valid_moves:
                    moves.append((i,j),tuple(m))
        return moves
            
        
    
        