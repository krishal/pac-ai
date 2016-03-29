import pygame
import pacman
import time

import random

import cProfile
import pstats

import os
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

    def getKeys(self):
        keys = initKeys()

        randKey = [random.randint(0,3)]
        output = self.net.serial_activate(randKey)

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
        score = pacman.pacmanGame(True, True, control)
    except pacman.RecurseError:
        print "Ghost Pathplanning Failed"
        score = 0

    return score

def main():

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'pacai_config')

    pe = parallel.ParallelEvaluator(1, runPacman)
    pop = population.Population(config_path)

    pop.run(pe.evaluate, 400)

    winner = pop.statistics.best_genome()

if __name__ == '__main__':
    main()
