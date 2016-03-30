# Test the performance of the best genome produced by nn_evolve.py.

# Test the performance of the best genome produced by nn_evolve.py.
from __future__ import print_function

import pickle

from neat import nn, parallel, population, visualize

# load the winner
with open('nn_pop0', 'rb') as f:
    pop = pickle.load(f)

winner = pop.statistics.best_genome()

# Plot the evolution of the best/average fitness.
visualize.plot_stats(pop.statistics, ylog=True, filename="nn_fitness.svg")
# Visualizes speciation
visualize.plot_species(pop.statistics, filename="nn_speciation.svg")
# Visualize the best network.
visualize.draw_net(winner, view=False, filename="nn_winner.gv")
visualize.draw_net(winner, view=False, filename="nn_winner-enabled.gv", show_disabled=False)
visualize.draw_net(winner, view=False, filename="nn_winner-enabled-pruned.gv", show_disabled=False, prune_unused=True)