import pygame
import pacman
import time

import random

import cProfile
import pstats

from functools import partial
from multiprocessing import Process, Pool, Queue

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
    def __init__(self):
        self.i = 0

    def update(self):
        self.i = self.i + 1

    def getKeys(self):
        keys = initKeys()

        if(self.i % 20 == 0):
            randKey = random.randint(0,3)
            if randKey == 0:
                keys[pygame.K_RIGHT] = True
            elif randKey == 1:
                keys[pygame.K_LEFT] = True
            elif randKey == 2:
                keys[pygame.K_DOWN] = True
            elif randKey == 3:
                keys[pygame.K_UP] = True
            elif randKey == 4:
                keys[pygame.K_ESCAPE] = True
            elif randKey == 5:
                keys[pygame.K_RETURN] = True

        return keys

    def setSuccess(self, success):
        self.success = success
    
    def setScore(self, score):
        self.score = score

def runPacman(control):
    try:
        score = pacman.pacmanGame(False, True, control)
    except pacman.RecurseError:
        print "Ghost Pathplanning Failed"
        control.setSuccess(False)
    else:
        control.setSuccess(True)
        control.setScore(score)
    finally:
        q.put(control)

def main():
    global q
    q = Queue()

    numNNs = 1000
    nns = [nnControl()]*numNNs
    p = Pool(16)

    p.map(runPacman, nns)

    print "Finished first pass"
    while not q.empty():
        nn = q.get()
        if nn.success:
            print "Success"
            # Do something
        else:
            print "Restart"
            runPacman(nn)


if __name__ == '__main__':
    main()
