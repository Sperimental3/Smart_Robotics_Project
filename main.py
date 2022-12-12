"""
A script used a lot in the beginning of the project to test out the movements of Baxter in different situation.
Specifically to test the working of the pick_and_pour operation.
"""

from os.path import dirname, join, abspath
from pyrep import PyRep
from pyrep.robots.arms.baxter import BaxterLeft, BaxterRight
from pyrep.robots.end_effectors.baxter_gripper import BaxterGripper
from pyrep.objects.dummy import Dummy
from pyrep.objects.shape import Shape
import numpy as np
import torch
import random
from Simulation import Simulation
from understanding import Understander

SEED = 3334

np.random.seed(SEED)
torch.manual_seed(SEED)
random.seed(SEED)

Brain = Understander()

# prova = input("Give me an english request for a cocktail order/s to feed to the understander: ")
# print(Brain.understand(prova))

sim = Simulation()

while True:
    end = input("Press \"q\" to exit the program...")
    if end == "q":
        break

    phrase = input("Give me an english request for a cocktail order/s to feed to the understander: ")

    orders = Brain.understand(phrase)

    for order in orders:
        sim.start()

        for ingredient in order:
            if ingredient == '?':
                # TODO: an action that makes understand that baxter doesn't get it
                break
            sim.Baxter.pick_and_pour(ingredient)

        sim.stop()

sim.shutdown()
print("Bye!")
