"""
The main script. Here there is the loop that involves each time an order
and an execution from the simulation.
"""

import numpy as np
import torch
import random
from Simulation import Simulation
from understanding import Understander
from listening import Listener


SEED = 3334

np.random.seed(SEED)
torch.manual_seed(SEED)
random.seed(SEED)

Brain = Understander()
Ears = Listener()

# prova = input("Give me an english request for a cocktail order/s to feed to the understander: ")
# print(Brain.understand(prova))

# phrase = Ears.listen()
# print(phrase)

sim = Simulation()

while True:
    end = input("Press \"q\" to exit the program...")
    if end == "q":
        break

    mode = input("You want a textual mode? (Because of noise or other problems) (Yes/No)")
    if mode == "Yes" or mode == "Y" or mode == "YES" or mode == "yes" or mode == "y":
        phrase = input("Give me an english request for a cocktail order/s to feed to the understander:\n")
    else:
        phrase = Ears.listen()

    orders = Brain.understand(phrase)

    for order in orders:
        sim.start()

        for ingredient in order:
            if ingredient == '?':
                sim.Baxter.dunno()
                break
            sim.Baxter.pick_and_pour(ingredient)

        sim.stop()

sim.shutdown()

print("Bye!")
