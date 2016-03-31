import pickle

from neat import nn, parallel, population, visualize

import pacman
import pacai

if __name__ == "__main__":
    with open('winner', 'rb') as f:
        c = pickle.load(f)

    print c
    control = pacai.nnControl(c)
    score = pacman.pacmanGame(True, True, control)
    print "Final score: {0}".format(score)

