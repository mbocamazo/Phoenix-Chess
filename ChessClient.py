#/usr/bin/env python

from ChessBoard import ChessBoard
#import AI
import os, pygame,math
from pygame.locals import *

from pprint import pprint
"""List of grievances: parallelization
quit on machine's turn
beginning menu
Chris: if an issue, implement multithreading
"""

class Player:
    def __init__(self,color):
        self.color = color
        
class Human(Player):
    def __init__(self,color,board_model):
        super(Player,self).__init__(color)
        self.board_model = board_model
        
    def get_next_move(self,event):
        pass
                                
    def make_next_move(event):
        move = self.get_next_move(event)
        board_model.addMove(move)

class ChessClient:

    def mainLooptemp(self):    
        
        chess = ChessBoard()
        board = chess.getBoard()
        turn = chess.getTurn()

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((480, 480),1)
        pygame.display.set_caption('ChessBoard Client')
        view = PyGameWindowView(chess,screen)
        
        running = True
        
#        posRect = pygame.Rect(0,0,60,60)
        posRect = chess.posRect

        mousePos = chess.mousePos
        markPos = chess.markPos
        validMoves = chess.validMoves
        
        gameResults = ["","WHITE WINS!","BLACK WINS!","STALEMATE","DRAW BY THE FIFTY MOVES RULE","DRAW BY THE THREE REPETITION RULE"]
        
        while running:
            clock.tick(30)        
    
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    pygame.quit()
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
                    elif event.key == K_LEFT:
                        chess.undo()
                    elif event.key == K_RIGHT:
                        chess.redo()
                    elif event.unicode in ("f","F"):
                        print chess.getFEN()
                    elif event.unicode in ("a","A"):
                        an = chess.getAllTextMoves(chess.AN)
                        if an:
                            print "AN: " + ", ".join(an)
                    elif event.unicode in ("s","S"):
                        san = chess.getAllTextMoves(chess.SAN)
                        if san:
                            print "SAN: " + ", ".join(san)
                    elif event.unicode in ("l","L"):
                        lan = chess.getAllTextMoves(chess.LAN)
                        if lan:
                            print "LAN: " + ", ".join(lan)
                    board = chess.getBoard()
                    turn = chess.getTurn()
                    markPos[0] = -1
                    validMoves = [] 
                        
                if not chess.isGameOver():
                    if event.type == MOUSEMOTION:
                        mx = event.pos[0]
                        my = event.pos[1]
                        mousePos[0] = mx/60
                        mousePos[1] = my/60
                    elif event.type == MOUSEBUTTONDOWN:
                        if mousePos[0] != -1:
                            if markPos[0] == mousePos[0] and markPos[1] == mousePos[1]:
                                markPos[0] = -1
                                validMoves = []
                            else: 
                                if (turn==ChessBoard.WHITE and board[mousePos[1]][mousePos[0]].isupper()) or \
                                   (turn==ChessBoard.BLACK and board[mousePos[1]][mousePos[0]].islower()):    
                                    markPos[0] = mousePos[0]
                                    markPos[1] = mousePos[1]
                                    validMoves = chess.getValidMoves(tuple(markPos))
                                    
                                else:
                                    if markPos[0] != -1:
                                        res = chess.addMove(markPos,mousePos)
                                        if not res and chess.getReason() == chess.MUST_SET_PROMOTION:
                                            chess.setPromotion(chess.QUEEN)                                                
                                            res = chess.addMove(markPos,mousePos)                                            
                                        if res:
                                            #print chess.getLastMove()
                                            print chess.getLastTextMove(chess.SAN)
                                            board = chess.getBoard()
                                            turn = chess.getTurn()
                                            markPos[0] = -1
                                            validMoves = [] 

            if chess.isGameOver():
                pygame.display.set_caption("Game Over! (Reason:%s)" % gameResults[chess.getGameResult()])
                validMoves = []
                markPos[0] = -1
                markPos[1] = -1
            else:
                pygame.display.set_caption('ChessBoard Client') 
                                            
            view.draw(chess)
#            y = 0
#            for rank in board:
#                x = 0
#                for p in rank:
#                    screen.blit(pieces[(x+y)%2][p],(x*60,y*60))
#                    x+=1
#                y+=1             

#            if markPos[0] != -1:
#                posRect.left = markPos[0]*60
#                posRect.top = markPos[1]*60
#                pygame.draw.rect(screen, (255,255,0),posRect, 4)

#            for v in validMoves:
#                posRect.left = v[0]*60
#                posRect.top = v[1]*60
#                pygame.draw.rect(screen, (255,255,0),posRect, 4)
                                       
            pygame.display.flip()  
        pygame.quit()

class PyGameWindowView:
    """Renders the state of the view and contains draw functions"""
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
                
#        self.posRect = pygame.Rect(0,0,60,60)
#        self.mousePos = [-1,-1]
#        self.markPos = [-1,-1]
    
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
#        self.chess = ChessBoard()
        self.board = chess.getBoard()
        self.drawPieces(chess)
        self.drawMarkPos(chess)
        self.drawHighlights(chess)
            
def main():
    pygame.init()
    g = ChessClient()
    g.mainLooptemp()
    
    

#    model = TDModel(tile_grid)
#    view = PyGameWindowView(model,screen)
#    controller = PyGameMouseController(model,view)
#    running = True
#    while running:
#        for event in pygame.event.get():
#            if event.type == QUIT:
#                pygame.mouse.set_cursor(*pygame.cursors.arrow)
#                running = False
#            controller.handle_mouse_event(event)
#        model.update()
#        view.draw()
#        time.sleep(.001)
#    pygame.quit()
 
#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()


