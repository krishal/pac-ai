import pygame
import pacman
import time

import random

import cProfile
import pstats

import os
import pickle
from functools import partial
from multiprocessing import Process, Pool, Queue

from neat import nn, parallel, population, visualize

def initKeys():
    keys = {}
    keys[pygame.K_RIGHT] = False
    keys[pygame.K_LEFT] = False
    keys[pygame.K_DOWN] = False
    keys[pygame.K_UP] = False
    keys[pygame.K_ESCAPE] = False
    keys[pygame.K_RETURN] = False
    return keys

class nnControl():
    def __init__(self, genome):
        self.i = 0
        self.genome = genome
        self.net = nn.create_feed_forward_phenotype(genome)

    def update(self):
        self.i = self.i + 1

    def getKeys(self, gridInput):
        keys = initKeys()

        output = self.net.serial_activate(gridInput)

        if output[0] > 0.5:
            keys[pygame.K_RIGHT] = True
        if output[1] > 0.5:
            keys[pygame.K_LEFT] = True
        if output[2] > 0.5:
            keys[pygame.K_DOWN] = True
        if output[3] > 0.5:
            keys[pygame.K_UP] = True

        return keys

    def setSuccess(self, success):
        self.success = success
    
    def setScore(self, score):
        self.score = score

def runPacman(genome):
    control = nnControl(genome)
    try:
        start = time.clock();
        score = pacman.pacmanGame(False, True, control)
    except pacman.RecurseError:
        print "Ghost Pathplanning Failed"
        score = 0
    print('time: {0}').format(time.clock()-start)
    return score

def main():

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'grid_pacai_config')

    pe = parallel.ParallelEvaluator(2, runPacman)
    pop = population.Population(config_path)
    genJump=10

    for numGen in range(0,1000,genJump):
        pop.run(pe.evaluate, genJump)

        print('Number of evaluations: {0:d}'.format(pop.total_evaluations))

        with open('nn_pop'+str(numGen), 'wb') as f:
            pickle.dump(pop, f)

if __name__ == '__main__':
    main()
