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
print ai_list[0].piece_weights
print ai_list[5].piece_weights