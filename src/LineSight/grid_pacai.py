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
        score = pacman.pacmanGame(True, True, control)
    except pacman.RecurseError:
        print "Ghost Pathplanning Failed"
        score = 0

    return score

def runPacmanShow(genome):
    control = nnControl(genome)
    try:
        score = pacman.pacmanGame(True, True, control)
    except pacman.RecurseError:
        print "Ghost Pathplanning Failed"
        score = 0

    return score

def main():

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'grid_pacai_config')

    pe = parallel.ParallelEvaluator(2, runPacman)
    pop = population.Population(config_path)

    pop.run(pe.evaluate, 400)

    winner = pop.statistics.best_genome()

    print('Number of evaluations: {0}'.format(pop.total_evaluations))

    # Visualize the winner network and plot/log statistics.
    visualize.plot_stats(pop.statistics)
    visualize.plot_species(pop.statistics)
    visualize.draw_net(winner, view=True, filename="xor2-all.gv")
    visualize.draw_net(winner, view=True, filename="xor2-enabled.gv", show_disabled=False)
    visualize.draw_net(winner, view=True, filename="xor2-enabled-pruned.gv", show_disabled=False, prune_unused=True)

if __name__ == '__main__':
    main()
