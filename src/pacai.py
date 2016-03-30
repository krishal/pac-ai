import pygame
import pacman
import time

import pickle

import math
import os
from functools import partial
from multiprocessing import Process, Pool, Queue

from neat import nn, parallel, population, visualize

import cProfile
import pstats

def initKeys():
    keys = {}
    keys[pygame.K_RIGHT] = False
    keys[pygame.K_LEFT] = False
    keys[pygame.K_DOWN] = False
    keys[pygame.K_UP] = False
    keys[pygame.K_ESCAPE] = False
    keys[pygame.K_RETURN] = False
    return keys

# Grid dimension used for inputs to neural net
GRID_DIMENSION=3

def GetGridInputs():
    gridInputs=[]
    ghostRow=[]
    ghostCol=[]
    mid = int(GRID_DIMENSION/2)

    for g in range(4):
        ghostRow.append(pacman.ghosts[g].nearestRow)
        ghostCol.append(pacman.ghosts[g].nearestCol)

    for i in range(GRID_DIMENSION):
        yVal = pacman.player.nearestRow - mid + i

        for j in range(GRID_DIMENSION):
            if i == mid and j == mid:
                continue
            xVal = pacman.player.nearestCol - mid + j
            if pacman.thisLevel.IsWall((yVal, xVal)): #Check for wall
                # gridInputs.append(1)
                gridInputs.extend([1,0,0])
            elif yVal in ghostRow and xVal in ghostCol: #Check for ghosts
                # gridInputs.append(2)
                gridInputs.extend([0,1,0])
            elif pacman.thisLevel.GetMapTile((yVal, xVal))<4 and pacman.thisLevel.GetMapTile((yVal, xVal))>0: #Check for pellets
                # gridInputs.append(0)
                gridInputs.extend([0,0,1])
            else: #Check for  empty space
                # gridInputs.append(3)
                gridInputs.extend([0,0,0])

    return gridInputs

class nnControl():
    def __init__(self, genome):
        self.i = 0
        self.genome = genome
        self.net = nn.create_feed_forward_phenotype(genome)
        self.keys = initKeys()

    def getDotDistancesIn4Dirs(self):
        d = [0]*4
        pd = [0]*4
        closest = [(0,0)]*4
        pclosest = [(0,0)]*4

        pelletTile = pacman.tileID['pellet']
        ppelletTile = pacman.tileID['pellet-power']

        for i in range(0, pacman.thisLevel.lvlWidth):
            for j in range(0, pacman.thisLevel.lvlHeight):

                tile = pacman.thisLevel.GetMapTile((i,j))
                if tile == pelletTile:
                    dx = j - pacman.player.nearestCol
                    dy = i - pacman.player.nearestRow
                    th = math.atan2(dy, dx)
                    dist = math.sqrt(dx*dx + dy*dy)

                    if dist == 0:
                        dist = 1
                    else:
                        dist = 1/dist

                    if th > 3./4*math.pi or th < -3./4*math.pi:
                        # Left
                        if dist < d[0]:
                            d[0] = dist
                            closest[0] = (i,j)
                    elif th < 3./4*math.pi and th > 1./4*math.pi:
                        # Down
                        if dist < d[1]:
                            d[1] = dist
                            closest[1] = (i,j)
                    elif th < 1./4*math.pi and th > -1./4*math.pi:
                        # Right
                        if dist < d[2]:
                            d[2] = dist
                            closest[2] = (i,j)
                    elif th < -1./4*math.pi and th > -3./4*math.pi:
                        # Up
                        if dist < d[3]:
                            d[3] = dist
                            closest[3] = (i,j)
                elif tile == ppelletTile:
                    dx = j - pacman.player.nearestCol
                    dy = i - pacman.player.nearestRow
                    th = math.atan2(dy, dx)
                    dist = math.sqrt(dx*dx + dy*dy)

                    if dist == 0:
                        dist = 1
                    else:
                        dist = 1/dist

                    if th > 3./4*math.pi or th < -3./4*math.pi:
                        # Left
                        if dist < pd[0]:
                            pd[0] = dist
                            pclosest[0] = (i,j)
                    elif th < 3./4*math.pi and th > 1./4*math.pi:
                        # Down
                        if dist < pd[1]:
                            pd[1] = dist
                            pclosest[1] = (i,j)
                    elif th < 1./4*math.pi and th > -1./4*math.pi:
                        # Right
                        if dist < pd[2]:
                            pd[2] = dist
                            pclosest[2] = (i,j)
                    elif th < -1./4*math.pi and th > -3./4*math.pi:
                        # Up
                        if dist < pd[3]:
                            pd[3] = dist
                            pclosest[3] = (i,j)

        #print closest
        #print (pacman.player.nearestCol, pacman.player.nearestRow)
        #print d
        return d + pd

    def getGhostDistancesIn4Dirs(self):
        d = [0]*4

        for i in range(0, 4):
            if not pacman.ghosts[i] == 2:
                dx = pacman.ghosts[i].nearestCol - pacman.player.nearestCol
                dy = pacman.ghosts[i].nearestRow - pacman.player.nearestRow
                th = math.atan2(dy, dx)
                dist = math.sqrt(dx*dx + dy*dy)

                if dist == 0:
                    dist = 1
                else:
                    dist = 1/dist

                if th > 3./4*math.pi or th < -3./4*math.pi:
                    # Left
                    if dist < d[0]:
                        d[0] = dist
                elif th < 3./4*math.pi and th > 1./4*math.pi:
                    # Down
                    if dist < d[1]:
                        d[1] = dist
                elif th < 1./4*math.pi and th > -1./4*math.pi:
                    # Right
                    if dist < d[2]:
                        d[2] = dist
                elif th < -1./4*math.pi and th > -3./4*math.pi:
                    # Up
                    if dist < d[3]:
                        d[3] = dist

        return d

    def getBlueGhostDistancesIn4Dirs(self):
        d = [0]*4

        for i in range(0, 4):
            if pacman.ghosts[i] == 2:
                dx = pacman.ghosts[i].nearestCol - pacman.player.nearestCol
                dy = pacman.ghosts[i].nearestRow - pacman.player.nearestRow
                th = math.atan2(dy, dx)
                dist = math.sqrt(dx*dx + dy*dy)

                if dist == 0:
                    dist = 1
                else:
                    dist = 1/dist

                if th > 3./4*math.pi or th < -3./4*math.pi:
                    # Left
                    if dist < d[0]:
                        d[0] = dist
                elif th < 3./4*math.pi and th > 1./4*math.pi:
                    # Down
                    if dist < d[1]:
                        d[1] = dist
                elif th < 1./4*math.pi and th > -1./4*math.pi:
                    # Right
                    if dist < d[2]:
                        d[2] = dist
                elif th < -1./4*math.pi and th > -3./4*math.pi:
                    # Up
                    if dist < d[3]:
                        d[3] = dist

        return d

    def getDistanceToHome(self):
        nearestRow = int(((pacman.player.homeY + 8) / 16))
        nearestCol = int(((pacman.player.homeX + 8) / 16))

        dx = nearestCol - pacman.player.nearestCol
        dy = nearestRow - pacman.player.nearestRow

        dist = math.sqrt(dx*dx + dy*dy)

        if dist == 0:
            dist = 1
        else:
            dist = 1/dist

        return [dist]

    def update(self):
        self.i = self.i + 1

        self.keys = initKeys()

        ghostd = self.getGhostDistancesIn4Dirs()
        blueghostd = self.getBlueGhostDistancesIn4Dirs()
        pelletd = self.getDotDistancesIn4Dirs()
        homed = self.getDistanceToHome()

        grid = GetGridInputs()

        inputs = ghostd + blueghostd + pelletd + grid + homed
        output = self.net.serial_activate(inputs)

        if output[0] > 0.5:
            self.keys[pygame.K_RIGHT] = True
        if output[1] > 0.5:
            self.keys[pygame.K_LEFT] = True
        if output[2] > 0.5:
            self.keys[pygame.K_DOWN] = True
        if output[3] > 0.5:
            self.keys[pygame.K_UP] = True

    def getKeys(self):

        return self.keys

def runPacman(genome):
    print "Starting game"
    control = nnControl(genome)
    success = False
    while not success:
        try:
            score = pacman.pacmanGame(False, True, control)
        except pacman.RecurseError:
            print "Ghost Pathplanning Failed"
        else:
            success = True

    return score

def main():

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'pacai_config')

    pe = parallel.ParallelEvaluator(8, runPacman)
    pop = population.Population(config_path)

    for i in range(0, 1):
        pop.run(pe.evaluate, 1)
        winner = pop.statistics.best_genome()
        print winner
        filename = "winner{0}".format(i)
        with open(filename, 'wb') as f:
            pickle.dump(winner, f)

        visualize.plot_stats(pop.statistics)
        visualize.plot_species(pop.statistics)
        visualize.draw_net(winner, view=True)


if __name__ == '__main__':
    cProfile.run("main()", "profileStats")
    p = pstats.Stats('profileStats')
    p.strip_dirs().sort_stats(-1).print_stats()
