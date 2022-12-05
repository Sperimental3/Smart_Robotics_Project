import os.path as P
import numpy as np
import cv2 as cv
import torch

from pyrep import PyRep
from pyrep.objects.shape import Shape
from pyrep.objects.dummy import Dummy
from pyrep.backend import sim

from Baxter import Baxter

from random import random


SCENE_FILE = P.join(P.dirname(P.abspath(__file__)), "simulation.ttt")


class Simulation:
    def __init__(self):
        self.sim = PyRep()
        self.sim.launch(SCENE_FILE)
        self.sim.start()

        self.Baxter = Baxter(self)

        Gin = Shape("Gin")
        Vermut = Shape("Vermut")
        # TODO other ingredients...

        self.ingredients = {"gin": [7, 9, 11, Gin],
                            "vermut": [8, 12, 13, Vermut]
                            }
        self.cup = Shape('Cup')

        self.waypoints = [Dummy(f"waypoint{i}") for i in range(14)]

        for i in range(20):
            self.sim.step()

    # TODO, to write labels on cylinders or on the table?
    # probably doing this with textures or colors

    """
    def start(self):
        self.sim.start()
        self.sim.step()

        # just for initialization calm I suppose
        for i in range(10):
            self.sim.step()
    """

    def stop(self):
        self.sim.stop()
        self.sim.shutdown()
