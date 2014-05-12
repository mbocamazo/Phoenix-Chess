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

pickle_file = "evolved_AI_pop_1_saved.p"
ai_list = p.load(open(pickle_file,"rb"))

history_avg_piece_weights = []

for i in range(len(ai_list[0].piece_weights_history)):
    avg_piece_weights = {'q':0,'r':0,'b':0,'n':0}
    for ai in ai_list:
        piece_weights = ai.piece_weights_history[i]
        for key in piece_weights:
            avg_piece_weights[key] = avg_piece_weights[key] + piece_weights[key]
    avg_piece_weights[key] = avg_piece_weights[key]/16.0
    history_avg_piece_weights.append(avg_piece_weights)
    
print history_avg_piece_weights