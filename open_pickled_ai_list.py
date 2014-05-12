# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 03:21:57 2014

@author: dchen
"""

from ChessBoard import ChessBoard
from ChessAI import ChessAI
from run_genetic_algorithms import *
from multiprocessing import Pool
import random
import evaluation_functions
import prune_functions
import QFunctions
import math
import multiprocessing
import pickle as p

pickle_file = "evolved_AI_pop.p"
ai_list = p.load(open(pickle_file,"rb"))
history_avg_piece_weights = []
first_place_piece_weights = []
standard_deviations = []

for i in range(len(ai_list[0].piece_weights_history)):
    avg_piece_weights = {'q':0,'r':0,'b':0,'n':0}
    standard_deviation = {'q':0,'r':0,'b':0,'n':0}
    queen_weight_list = []
    rook_weight_list = []
    knight_weight_list = []
    bishop_weight_list = []
    for ai in ai_list:
        rank = ai.rank_history[i]
        if rank == 0:
            first_place_piece_weights.append(ai.piece_weights_history[i])
        piece_weights = ai.piece_weights_history[i]
        queen_weight_list.append(piece_weights['q'])
        rook_weight_list.append(piece_weights['r'])
        bishop_weight_list.append(piece_weights['b'])
        knight_weight_list.append(piece_weights['n'])
        for key in piece_weights:
            print key
            avg_piece_weights[key] = avg_piece_weights[key] + piece_weights[key]
    for key in avg_piece_weights:
        avg_piece_weights[key] = avg_piece_weights[key]/16.0
        
    standard_deviation['q'] = numpy.std(queen_weight_list)
    standard_deviation['r'] = numpy.std(rook_weight_list)
    standard_deviation['b'] = numpy.std(bishop_weight_list)
    standard_deviation['n'] = numpy.std(knight_weight_list)
    
    standard_deviations.append(standard_deviation)
    history_avg_piece_weights.append(avg_piece_weights)
    
print "avg piece weights over time"
print history_avg_piece_weights
print "best ai piece weights over time"
print first_place_piece_weights
print "standard deviation over time"
print standard_deviations