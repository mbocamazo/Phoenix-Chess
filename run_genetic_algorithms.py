# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 21:08:48 2014

@author: dchen

base class from which we's gonna run some genetic algorithms
"""
from ChessBoard import ChessBoard
from ChessAI import ChessAI
from multiprocessing import Pool
import random
import evaluation_functions
import prune_functions
import QFunctions
import math
import multiprocessing
import pickle 
import os

class Schedule:
    
    def __init__(self,recom_prob,mut_prob,mut_mag_calc_func,generations):
        """takes mutation probabilities and a tuple of mutation magnitudes for each generation"""
        self.recom_prob = recom_prob
        self.mut_prob = mut_prob
        self.mut_mag_calc_func = mut_mag_calc_func
        self.generations = generations
        self.population_size = 16
        self.tournaments = []
        self.final_AI_pop = None
        
    def run_schedule(self):
        AI_list = create_AI(self.population_size)
        for g in range(0,self.generations):
            t = SwissTournamentSimpleEvalExistingAI(AI_list) 
            AI_list = t.play_tourn()
            AI_list.sort(key=lambda x: x.tournament_score, reverse=True) #this sorts AI by fitness
            self.tournaments.append(t)
            self.recombine_genes(AI_list) #order of list must be maintained         
            self.mutate_genes(AI_list,g) #order of list must be maintained
            print "piece weights of AI of generation "+str(g)
            for index, ai in enumerate(AI_list):
                print "AI "+ str(ai.id) + " 's tournament score: "
                print ai.tournament_score
                ai.tournament_score = 0
                ai.piece_weights_history.append(ai.piece_weights.copy())
                ai.rank_history.append(index)
                piece_weights = ai.piece_weights
                print piece_weights
        self.final_AI_pop = AI_list
        
    def recombine_genes(self,AI_list):
        """doesnt modify order of AI list"""
        AI_num = len(AI_list)
        quartile = AI_num/4         
        for i in range(0,quartile):
            better_AI = AI_list[i]
            worse_AI = AI_list[-(i+1)]
            better_genome = better_AI.piece_weights
            worse_genome = worse_AI.piece_weights          
            for piece,score in better_genome.iteritems():
                if random.random() < self.recom_prob:
                    worse_genome[piece] = score
        
    def mutate_genes(self,AI_list,generation_num):
        """doesnt modify order of AI list"""
        for i in range(1,len(AI_list)): #mutate everything but the best AI which is put first
            genome = AI_list[i].piece_weights            
            for piece,score in genome.iteritems():
                if random.random() < self.mut_prob:
                    mut_mag = self.mut_mag_calc_func(generation_num)
                    genome[piece] += 4*(random.random()-0.5)*mut_mag
                    
def anneal_sched_mut_mag(generation_num):
    mut_mag = None    
    if 0 <= generation_num < 16:
        mut_mag = 1-generation_num/(16/.95)
    if 16<= generation_num < 20:
        mut_mag = .05
    if 20<= generation_num <= 30:
        mut_mag = 0
    return mut_mag
                
            
class TournamentAI(ChessAI):    
    
    last_initialized_id = None
    
    def __init__(self,eval_func,should_prune_func,q_func,piece_weights,ply):
        super(TournamentAI,self).__init__(None,None,eval_func,should_prune_func,q_func,piece_weights,ply)
        self.tournament_score = 0
        if TournamentAI.last_initialized_id == None:
            TournamentAI.last_initialized_id = 0
        else:
            TournamentAI.last_initialized_id += 1
        self.id = TournamentAI.last_initialized_id
        self.games_played_id = {}        
        self.piece_weights_history = []
        self.rank_history = []
        
        
class SwissTournamentSimpleEvalExistingAI:    
    """runs a swiss tournament between a list of specified
    AI w/random pair weightings, given an AI list. Specified number must be an even number. 
    Stores a list of AI sorted by rank, once the games have been played.
    Also stores all games played for examination and testing.
    AI has a simple material eval func"""
    def __init__(self,AI_list):
        self.AI_list = AI_list
        self.game_dict = {}
        AI_num = len(AI_list)
        self.round_num = int(math.ceil(math.log(AI_num,2)))
            
    def play_tourn(self):        
        for i in range(self.round_num):
            pool = Pool(processes=len(self.AI_list)/2)
            games = []
            for j in range(0,len(self.AI_list),2):
                p1 = self.AI_list[j]
                p2 = self.AI_list[j+1]
                g = Game(p1,p2)
                g.pickle_order_id = j #save the order that games are pickled in so we can reload them in the same order
                games.append(g)
                self.game_dict[g.id] = g
            pool.map(play_game,games) #parallelize game playing
            original_ai_list_length = len(self.AI_list)
            self.AI_list = [] #now reset the AI_list and load the newly modified AI from the pickle files
            for i in range(0,original_ai_list_length,2): #reload the ais back into the ai list
                file_name = 'game_'+str(i)+'.p'
                game = pickle.load(open(file_name,"rb"))      
                ai_1 = game.w_player
                ai_2 = game.b_player
                self.AI_list.append(ai_1)
                self.AI_list.append(ai_2)
                os.remove(file_name)
                
        return self.AI_list
            
def play_game(game):
    """helper function for multithreading"""
    game.play_game() #interesting threading intricacy: the first line of play_game MUST call a game object function
    game_number = game.pickle_order_id
    file_name = 'game_'+str(game_number)+'.p'
    with open(file_name, 'wb') as f:
        pickle.dump(game,f)
    
def create_AI(AI_num):
    assert AI_num%2 == 0
    AI_list = []
    for i in range(AI_num):
        random_piece_dict = build_random_piece_dict()
        AI = TournamentAI(evaluation_functions.terminal_dict_material_eval,
             prune_functions.never_prune,QFunctions.no_extension,random_piece_dict,4)
        AI_list.append(AI)
    return AI_list


    
class SwissTournamentSimpleEvalNewAI:    
    """runs a swiss tournament between a specified number of
    AI w/random pair weightings. Specified number must be an even number. 
    Stores a list of AI sorted by rank, once the games have been played.
    Also stores all games played for examination and testing.
    AI has a simple material eval func"""
    def __init__(self,AI_num,round_num):
        assert AI_num%2 == 0
        self.AI_list = []
        for i in range(AI_num):
            random_piece_dict = build_random_piece_dict()
            AI = TournamentAI(evaluation_functions.terminal_dict_material_eval,
                 prune_functions.never_prune,QFunctions.simple_end_game,random_piece_dict,2)
            self.AI_list.append(AI)
        self.game_dict = {}
        self.round_num = round_num
            
    def play_tourn(self):
        for i in range(self.round_num):
            pool = Pool(processes = self.AI_list/2)
            g_list = []
            for j in range(0,len(self.AI_list),2):
                p1 = self.AI_list[j]
                p2 = self.AI_list[j+1]
                print "playing game between AI "+str(p1.id) +" and AI "+str(p2.id)
                g = Game(p1,p2)
                self.game_dict[g.id] = g
                g_list.append(g)
            pool.map(g.play_game(),g_list)
            self.AI_list.sort(key=lambda x: x.tournament_score, reverse=True)
            
class SwissTournamentPairEval:
    """runs a swiss tournament between a specified number of
    AI w/random pair weightings. Specified number must be an even number. 
    Stores a list of AI sorted by rank, once the games have been played.
    Also stores all games played for examination and testing.
    AI have a random pair eval func"""
    def __init__(self,AI_num,round_num):
        assert AI_num%2 == 0
        self.AI_list = []
        for i in range(AI_num):
            random_piece_dict = build_random_pair_piece_dict()
            AI = TournamentAI(evaluation_functions.terminal_paired_material_eval,
                 prune_functions.never_prune,QFunctions.simple_end_game,random_piece_dict,2)
            self.AI_list.append(AI)
        self.game_dict = {}
        self.round_num = round_num
            
    def play_tourn(self):
        for i in range(self.round_num):
            for j in range(0,len(self.AI_list),2):
                p1 = self.AI_list[j]
                p2 = self.AI_list[j+1]
                print "playing game between AI "+str(p1.id) +" and AI "+str(p2.id)
                g = Game(p1,p2)
                self.game_dict[g.id] = g
                g.play_game()
                self.AI_list.sort(key=lambda x: x.tournament_score, reverse=True)
            
            

class Game:
    """given two AI players, runs a game between them and stores the result.
    Modifies the swiss tourny scores and colors of the AI that play."""
    
    BLACK_WIN = -1
    WHITE_WIN = 1
    DRAW = 0
    last_initialized_id = None
    
    def __init__(self,w_player,b_player):
        self.w_player = w_player
        self.b_player = b_player
        self.w_player.color = ChessBoard.WHITE
        self.b_player.color = ChessBoard.BLACK
        self.game_result = None
        self.saved_moves = None
        if Game.last_initialized_id == None:
            Game.last_initialized_id = 0
        else:
            Game.last_initialized_id += 1
        self.id = Game.last_initialized_id
        # opponent_id: game as the key/val pair
        w_player.games_played_id[b_player.id] = self.id
        b_player.games_played_id[b_player.id] = self.id
        
    def play_game(self):
        chess = ChessBoard()
        self.w_player.chess = chess
        self.b_player.chess = chess
        while not chess.isGameOver():
            self.w_player.make_next_move()
            if chess.isGameOver():
                break
            self.b_player.make_next_move()
        r = chess.getGameResult()
        print r
        if r == 1:
            self.game_result = Game.WHITE_WIN
            self.w_player.tournament_score += 1
        if r == 2:
            self.game_result = Game.BLACK_WIN
            self.b_player.tournament_score += 1
        if r in [3,4,5]:
            self.w_player.tournament_score += .5
            self.b_player.tournament_score += .5
            self.game_result = Game.DRAW
        self.saved_moves = chess.getAllTextMoves()
        
    def get_game_result(self):
        return self.game_result 
    
def build_random_piece_dict():
    """generates a random piece dictionary that is used by the
    material eval function. AI will store and pass this
    dictionary/attribute to the material eval func.king and pawn weights
    are defined elsewhere in the evaluate simple material func
    since they aren't uniquely determined"""
    piece_score_dict = {}
    b_piece_list = ['r','n','b','q']
    for b in b_piece_list:
        rand_num = random.uniform(-10,0)
        piece_score_dict[b] = rand_num  
    return piece_score_dict
    
        
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

if __name__ == '__main__': 
    s = Schedule(.25,.2,anneal_sched_mut_mag,25)
    s.run_schedule()
    with open('evolved_AI_pop.p', 'wb') as f:
        print "Saved to %s" % "evolved_AI_pop"
        pickle.dump(s.final_AI_pop,f)