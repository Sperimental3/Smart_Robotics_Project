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
"""
Brain = Understander()

prova = input("Give me an english request for a cocktail order/s to feed to the understander: ")

print(Brain.understand(prova))
"""
"""
"""
# Let's do some tests
sim = Simulation()
# sim.start()
"""
# print(sim.waypoints[20].get_quaternion(), sim.waypoints[2].get_quaternion(), sim.waypoints[20])
#sim.Baxter.pick_and_pour("gin")
#sim.Baxter.pick_and_pour("vermut")

#sim.Baxter.pick_and_pour("lemon")
sim.Baxter.pick_and_pour("campari")

sim.Baxter.pick_and_pour("vermut")
sim.Baxter.pick_and_pour("gin")

sim.Baxter.pick_and_pour("vermut")

sim.stop()
"""
"""
This procedure is related to the default behaviour of Baxter

print('Planning path for left arm to cup ...')
path = baxter_left.get_path(position=waypoints[0].get_position(),
                            quaternion=waypoints[0].get_quaternion())
path.visualize()  # Let's see what the path looks like
print('Executing plan ...')
done = False
while not done:
    done = path.step()
    pr.step()
path.clear_visualization()

print('Planning path closer to cup ...')
path = baxter_left.get_path(position=waypoints[1].get_position(),
                            quaternion=waypoints[1].get_quaternion())
print('Executing plan ...')
done = False
while not done:
    done = path.step()
    pr.step()

print('Closing left gripper ...')
while not baxter_gripper_left.actuate(0.0, 0.4):
    pr.step()
baxter_gripper_left.grasp(cup)

print('Planning path to lift cup ...')
path = baxter_left.get_path(position=waypoints[2].get_position(),
                            quaternion=waypoints[2].get_quaternion(),
                            ignore_collisions=True)
print('Executing plan ...')
done = False
while not done:
    done = path.step()
    pr.step()

print('Planning path for right arm to cup ...')
path = baxter_right.get_path(position=waypoints[3].get_position(),
                             quaternion=waypoints[3].get_quaternion())
print('Executing Plan ...')
done = False
while not done:
    done = path.step()
    pr.step()

print('Planning path closer to cup ...')
path = baxter_right.get_path(position=waypoints[4].get_position(),
                             quaternion=waypoints[4].get_quaternion())
print('Executing plan ...')
done = False
while not done:
    done = path.step()
    pr.step()

print('Closing right gripper ...')
while not baxter_gripper_right.actuate(0.0, 0.4):
    pr.step()

print('Opening left gripper ...')
while not baxter_gripper_left.actuate(1.0, 0.4):
    pr.step()

# Left gripper releases, right gripper grasps.
baxter_gripper_left.release()
baxter_gripper_right.grasp(cup)
pr.step()

print('Planning path for left arm to home position ...')
path_l = baxter_left.get_path(position=waypoints[5].get_position(),
                              quaternion=waypoints[5].get_quaternion())

print('Planning path for right arm to home position ...')
path_r = baxter_right.get_path(position=waypoints[6].get_position(),
                               quaternion=waypoints[6].get_quaternion())

print('Executing plan on both arms ...')
done_l = done_r = False
while not done_l or not done_r:
    if not done_l:
        done_l = path_l.step()
    if not done_r:
        done_r = path_r.step()
    pr.step()

print('Done ...')
input('Press enter to finish ...')
pr.stop()
pr.shutdown()
"""