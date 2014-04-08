#/usr/bin/env python
import os, pygame,math
from pygame.locals import *
from pprint import pprint
from ChessAI import *
import evaluation_functions
import prune_functions
from copy import deepcopy
from pprint import pprint
import pygame
from ChessBoard import ChessBoard
    
class ChessClient:

    def mainLooptemp(self):     

        chess = ChessBoard()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((480, 480),1)
        pygame.display.set_caption('ChessBoard Client')
        view = PyGameWindowView(chess,screen)
        controller = Controller(chess)        
        running = True
        
        player_1 = Human(ChessBoard.WHITE)
 #       player_1 = ChessAI(ChessBoard.WHITE,chess,evaluation_functions.simple_piece_eval,prune_functions.never_prune,2)
        AI2ply = 2
        player_2 = ChessAI(ChessBoard.BLACK,chess,evaluation_functions.simple_piece_eval,prune_functions.never_prune,AI2ply)
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
                    print "AI 1 (WHITE) making turn"
                    player_1.make_next_move()
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
                    print "AI 2 (BLACK) making turn"
                    player_2.make_next_move()
                    
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
            

def main():
    pygame.init()
    g = ChessClient()
    g.mainLooptemp()
    
#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()


