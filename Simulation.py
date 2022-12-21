import os.path as P
import numpy as np
import cv2 as cv
from random import random

from pyrep import PyRep
from pyrep.objects.shape import Shape
from pyrep.objects.dummy import Dummy

from Baxter import Baxter

# from pyrep.objects.vision_sensor import VisionSensor

SCENE_FILE = P.join(P.dirname(P.abspath(__file__)), "simulation.ttt")
SCENE_FILE_DEBUG = "/home/sperimental3/Scrivania/simulation_debug.ttt"


class Simulation:
    def __init__(self):
        self.sim = PyRep()
        self.sim.launch(SCENE_FILE)
        # self.sim.start()

        # self.camera = VisionSensor("Camera")

        Gin = Shape("Gin")
        Vermut = Shape("Vermut")
        Lemon = Shape("Lemon")
        Campari = Shape("Campari")

        self.ingredients = {"gin": [7, 9, 11, Gin],
                            "vermut": [8, 12, 13, Vermut],
                            "lemon": [14, 15, 16, Lemon],
                            "campari": [17, 18, 19, Campari]
                            }

        self.cup = Shape("Cup")

        self.waypoints = [Dummy(f"waypoint{i}") for i in range(22)]

        self.Baxter = Baxter(self)

        """
        self.default_baxter_left_conf = self.Baxter.baxter_left.get_configuration_tree()
        self.default_baxter_right_conf = self.Baxter.baxter_right.get_configuration_tree()

        self.default_baxter_gripper_left_conf = self.Baxter.baxter_gripper_left.get_configuration_tree()
        self.default_baxter_gripper_right_conf = self.Baxter.baxter_gripper_right.get_configuration_tree()

        self.default_Gin_conf = Gin.get_configuration_tree()
        self.default_Vermut_conf = Vermut.get_configuration_tree()
        self.default_Lemon_conf = Lemon.get_configuration_tree()
        self.default_Campari_conf = Campari.get_configuration_tree()

        self.default_cup_conf = self.cup.get_configuration_tree()
        """

    def start(self):
        self.sim.start()
        # self.sim.step()

    """
    def restore(self):
        self.sim.set_configuration_tree(self.default_baxter_left_conf)
        self.sim.set_configuration_tree(self.default_baxter_right_conf)
        self.sim.set_configuration_tree(self.default_baxter_gripper_left_conf)
        self.sim.set_configuration_tree(self.default_baxter_gripper_right_conf)

        self.sim.set_configuration_tree(self.default_Gin_conf)
        self.sim.set_configuration_tree(self.default_Vermut_conf)
        self.sim.set_configuration_tree(self.default_Lemon_conf)
        self.sim.set_configuration_tree(self.default_Campari_conf)

        self.sim.set_configuration_tree(self.default_cup_conf)
    """

    def stop(self):
        self.sim.stop()

    def shutdown(self):
        self.sim.shutdown()
