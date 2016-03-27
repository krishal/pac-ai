import pygame
import pacman
import time

import random

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

def main():
    lastTime = pygame.time.get_ticks()

    for i in range(0,20):
        '''
        cProfile.run("nn = nnControl(); pacman.pacmanGame(False, True, nn)", "restats")
        p = pstats.Stats('restats')
        p.sort_stats('tottime').print_stats()
        '''

        nn = nnControl()
        score = pacman.pacmanGame(False, True, nn)
        #print('Final score: {0}').format(score)

        print('Game time: {0}').format(pygame.time.get_ticks() - lastTime)
        lastTime = pygame.time.get_ticks()

if __name__ == '__main__':
    main()
