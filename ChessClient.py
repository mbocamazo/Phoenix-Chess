#/usr/bin/env python

from ChessBoard import ChessBoard
import os, pygame,math
from pygame.locals import *
from abc import ABCMeta, abstractmethod
from pprint import pprint
#from ChessAI import ChessAI
import random

class Player(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def get_next_move(self):
        pass
    
class Human(Player):
    def __init__(self,color):
        self.color = color
    def get_next_move(self):
        print "You shouldn't be calling this function! I'm not an AI!"
    
class ChessClient:

    def mainLooptemp(self):    
        
        chess = ChessBoard()

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((480, 480),1)
        pygame.display.set_caption('ChessBoard Client')
        view = PyGameWindowView(chess,screen)
        controller = Controller(chess)        
        running = True
        
        player_1 = ChessAI(ChessBoard.WHITE,chess,None,None,1)
        player_2 = ChessAI(ChessBoard.BLACK,chess,None,None,1)
##        AI_color = ChessBoard.BLACK
#        player_color = ChessBoard.WHITE
#        human_player = Player(player_color)
##        AI = (AI_color)    
#        player_2_color = ChessBoard.BLACK
#        human_player_2 = Player(player_2_color)
        
        while running:
            clock.tick(30)        
    
            if chess.getTurn() == player_1.color and not chess.isGameOver():
                if type(player_1) == Human:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            running = False
                            pygame.quit()
                            return
                        else:
                            controller.handle_event(event)   
                else:
                    player_1.get_next_move()
            elif chess.getTurn() == player_2.color and not chess.isGameOver():
                if type(player_2) == Human:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            running = False
                            pygame.quit()
                            return
                        else:
                            controller.handle_event(event)   
                else:
                    player_2.get_next_move()
                    
            #multithread in python to be able to make calculations and quit during player's turn
            
#            if chess.getTurn() == AI.color:
#                    turn = machine.get_turn()
#                    board.updatewithMachine'sturn
                    
            if chess.isGameOver():
                view.title_game_display(chess)
                chess.validMoves = []
                chess.markPos[0] = -1
                chess.markPos[1] = -1
                for event in pygame.event.get():
                    if event.type == QUIT:
                        running = False
                        pygame.quit()
                        return
            else:
                pygame.display.set_caption('ChessBoard Client') 
                                            
            view.draw(chess)
            pygame.display.flip()  
            
        pygame.quit()
        
class Controller:
    def __init__(self,chess):
        self.chess = chess
        self.board = chess.getBoard()

    def update_board(self):
        self.board = self.chess.getBoard()
        
    def handle_event(self,event):
        self.update_board()        
        
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return
            elif event.key == K_LEFT:
                self.chess.undo()
            elif event.key == K_RIGHT:
                self.chess.redo()
            elif event.unicode in ("f","F"):
                print self.chess.getFEN()
            elif event.unicode in ("a","A"):
                an = self.chess.getAllTextMoves(self.chess.AN)
                if an:
                    print "AN: " + ", ".join(an)
            elif event.unicode in ("s","S"):
                san = self.chess.getAllTextMoves(self.chess.SAN)
                if san:
                    print "SAN: " + ", ".join(san)
            elif event.unicode in ("l","L"):
                lan = self.chess.getAllTextMoves(self.chess.LAN)
                if lan:
                    print "LAN: " + ", ".join(lan)
            self.chess.markPos[0] = -1
            self.chess.validMoves = [] 
                
        if not self.chess.isGameOver():
            if event.type == MOUSEMOTION:
                mx = event.pos[0]
                my = event.pos[1]
                self.chess.mousePos[0] = mx/60
                self.chess.mousePos[1] = my/60
            elif event.type == MOUSEBUTTONDOWN:
                if self.chess.mousePos[0] != -1:
                    if self.chess.markPos[0] == self.chess.mousePos[0] and self.chess.markPos[1] == self.chess.mousePos[1]:
                        self.chess.markPos[0] = -1
                        self.chess.validMoves = []
                    else: 
                        #if its your turn, you haven't selected any pieces yet, and the piece you clicked on is your own piece
                        if (self.chess.getTurn()==ChessBoard.WHITE and self.board[self.chess.mousePos[1]][self.chess.mousePos[0]].isupper()) or \
                           (self.chess.getTurn()==ChessBoard.BLACK and self.board[self.chess.mousePos[1]][self.chess.mousePos[0]].islower()): 
                            self.chess.markPos[0] = self.chess.mousePos[0]
                            self.chess.markPos[1] = self.chess.mousePos[1]
                            #sets the selected piece position equal to the mouse position
                            self.chess.validMoves = self.chess.getValidMoves(tuple(self.chess.markPos))
#                            print self.chess.validMoves
                            
                        else:
                            if self.chess.markPos[0] != -1:
                                res = self.chess.addMove(self.chess.markPos,self.chess.mousePos)
                                if not res and self.chess.getReason() == self.chess.MUST_SET_PROMOTION:
                                    self.chess.setPromotion(self.chess.QUEEN)                                                
                                    res = self.chess.addMove(self.chess.markPos,self.chess.mousePos)                                            
                                if res:
                                    print self.chess.getLastTextMove(self.chess.SAN)
                                    self.chess.markPos[0] = -1
                                    self.chess.validMoves = [] 


class PyGameWindowView:
    """Renders the state of the view and contains draw functions"""
    gameResults = ["","WHITE WINS!","BLACK WINS!","STALEMATE","DRAW BY THE FIFTY MOVES RULE","DRAW BY THE THREE REPETITION RULE"]
    def __init__(self,chess,screen):
        self.chess = chess
        self.board = self.chess.getBoard()
        self.turn = self.chess.getTurn()
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.pieces = [{},{}]
        self.pieces[0]["r"] = pygame.image.load("./img/brw.png")                
        self.pieces[0]["n"] = pygame.image.load("./img/bnw.png")                
        self.pieces[0]["b"] = pygame.image.load("./img/bbw.png")                
        self.pieces[0]["k"] = pygame.image.load("./img/bkw.png")                
        self.pieces[0]["q"] = pygame.image.load("./img/bqw.png")                
        self.pieces[0]["p"] = pygame.image.load("./img/bpw.png")                
        self.pieces[0]["R"] = pygame.image.load("./img/wrw.png")                
        self.pieces[0]["N"] = pygame.image.load("./img/wnw.png")                
        self.pieces[0]["B"] = pygame.image.load("./img/wbw.png")                
        self.pieces[0]["K"] = pygame.image.load("./img/wkw.png")                
        self.pieces[0]["Q"] = pygame.image.load("./img/wqw.png")                
        self.pieces[0]["P"] = pygame.image.load("./img/wpw.png")                
        self.pieces[0]["."] = pygame.image.load("./img/w.png")                
        self.pieces[1]["r"] = pygame.image.load("./img/brb.png")                
        self.pieces[1]["n"] = pygame.image.load("./img/bnb.png")                
        self.pieces[1]["b"] = pygame.image.load("./img/bbb.png")                
        self.pieces[1]["k"] = pygame.image.load("./img/bkb.png")                
        self.pieces[1]["q"] = pygame.image.load("./img/bqb.png")                
        self.pieces[1]["p"] = pygame.image.load("./img/bpb.png")                
        self.pieces[1]["R"] = pygame.image.load("./img/wrb.png")                
        self.pieces[1]["N"] = pygame.image.load("./img/wnb.png")                
        self.pieces[1]["B"] = pygame.image.load("./img/wbb.png")                
        self.pieces[1]["K"] = pygame.image.load("./img/wkb.png")                
        self.pieces[1]["Q"] = pygame.image.load("./img/wqb.png")                
        self.pieces[1]["P"] = pygame.image.load("./img/wpb.png")                
        self.pieces[1]["."] = pygame.image.load("./img/b.png") 
        
    
    def drawPieces(self,chess):
        """Draws Board tiles and pieces"""
        y = 0
        for rank in self.board:
            x = 0
            for p in rank:
                self.screen.blit(self.pieces[(x+y)%2][p],(x*60,y*60))
                x+=1
            y+=1
            
    def drawMarkPos(self,chess):
        """draws selected position"""
        if self.chess.markPos[0] != -1:
            self.chess.posRect.left = self.chess.markPos[0]*60
            self.chess.posRect.top = self.chess.markPos[1]*60
            pygame.draw.rect(self.screen, (255,255,0),self.chess.posRect, 4)        
            
    def drawHighlights(self,chess):
        """Draws highlighted possible move squares"""    
        for v in self.chess.validMoves:
            self.chess.posRect.left = v[0]*60
            self.chess.posRect.top = v[1]*60
            pygame.draw.rect(self.screen, (255,255,0),self.chess.posRect, 4)
        
        
    def draw(self,chess):
        self.board = chess.getBoard()
        self.drawPieces(chess)
        self.drawMarkPos(chess)
        self.drawHighlights(chess)
        self.title_game_display(chess)
        
    def title_game_display(self,chess):
        if chess.isGameOver():
            pygame.display.set_caption("Game Over! (Reason:%s)" % self.gameResults[chess.getGameResult()])
        else:
            pygame.display.set_caption('ChessBoard Client') 
            
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
        
    def make_next_move(self):
        pass        
    
    def make_random_next_move(self):
        valid_moves = self.get_all_valid_moves()
        rand_move = random.choice(valid_moves)
        self.chess.addMove(rand_move[0],rand_move[1])
        
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
        possible_moves = self.get_all_valid_moves()
        
        for m in possible_moves:
            self.chess.addMove(m)
            score = -self.negamax(depth-1,-player_num)
            if score > best_score:
                best_score = score
                best_move = m
            self.chess.undo()
        return best_score,best_move
                 
            
    def get_all_valid_moves(self):
        """returns valid moves in the form [((xi,yi),(xf,yf)),...] where xi and yi represent the initial position of 
        the moved piece and xf and yf represent the final position"""
        moves = []
        for i in range(ChessAI.BOARDWIDTH):
            for j in range(ChessAI.BOARDWIDTH):
                valid_moves = self.chess.getValidMoves((i,j)) 
                for m in valid_moves:
                    moves.append(((i,j),tuple(m)))
        return moves
            
            
def main():
    pygame.init()
    g = ChessClient()
    g.mainLooptemp()
    
#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()


