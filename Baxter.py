import time

import numpy as np
import math
from time import sleep
from pyrep.robots.arms.baxter import BaxterLeft, BaxterRight
from pyrep.robots.end_effectors.baxter_gripper import BaxterGripper


class Baxter:
    def __init__(self, sim):
        # TODO
        self.sim = sim

        self.baxter_left = BaxterLeft()
        self.baxter_right = BaxterRight()
        self.baxter_gripper_left = BaxterGripper(0)
        self.baxter_gripper_right = BaxterGripper(1)

        self.baxter_left.set_joint_target_positions([0.12206578254699707, -0.43517088890075684, -0.16766047477722168,
                                                     2.0112273693084717, 0.8295693397521973, -1.4581592082977295,
                                                     0.10328960418701172])
        # TODO
        """
        self.rest = {
                'position': self.arm.get_tip().get_position(),
                'quaternion': self.arm.get_tip().get_quaternion()
                }
        """
    def move(self, location, ignore_collision=False):
        try:
            if location.get_position()[1] < 0:
                path = self.baxter_right.get_path(position=location.get_position(), quaternion=location.get_quaternion(), max_configs=10, ignore_collisions=ignore_collision)
            else:
                path = self.baxter_left.get_path(position=location.get_position(), quaternion=location.get_quaternion(), max_configs=10, ignore_collisions=ignore_collision)
            done = False
            path.visualize()
            while not done:
                done = path.step()
                self.sim.sim.step()
            path.clear_visualization()
            return True
        except Exception:
            print(f'Could not find a path using get_path(), solving iteratively trough jacobian ik...')

        if location.get_position()[1] < 0:
            pos = self.baxter_right.get_tip().get_position()
            quat = self.baxter_right.get_tip().get_quaternion()
            arm = self.baxter_right
        else:
            pos = self.baxter_left.get_tip().get_position()
            quat = self.baxter_left.get_tip().get_quaternion()
            arm = self.baxter_left

        STEPS = 50
        orientation = np.array(location.get_quaternion())
        location = np.array(location.get_position())

        pos = np.array(pos)
        quat = np.array(quat)

        for i in range(STEPS):
            delta_pos = pos + i*(location - pos)/STEPS
            delta_quat = quat + i*(orientation - quat)/STEPS

            try:
                ik = arm.solve_ik_via_jacobian(delta_pos, quaternion=delta_quat)
            except Exception:
                print(f'Could not get to {location}, stopped at {delta_pos}...')
                ik = arm.solve_ik_via_sampling(position=delta_pos, quaternion=delta_quat, max_configs=10)

            arm.set_joint_target_positions(ik)
            self.sim.sim.step()
        return True

    def reset_pos(self):
        self.baxter_left.set_joint_target_positions([0.12206578254699707, -0.43517088890075684, -0.16766047477722168,
                                                     2.0112273693084717, 0.8295693397521973, -1.4581592082977295,
                                                     0.10328960418701172])
        self.sim.sim.step()

    def grasp(self, obj):
        if obj.get_position()[1] < 0:
            while not self.baxter_gripper_right.actuate(0.0, 0.4):
                self.sim.sim.step()
            self.baxter_gripper_right.grasp(obj)
        else:
            while not self.baxter_gripper_left.actuate(0.0, 0.4):
                self.sim.sim.step()
            self.baxter_gripper_left.grasp(obj)
        return True

    def release(self, obj):
        if obj.get_position()[1] < 0:
            self.baxter_gripper_right.release()
            while not self.baxter_gripper_right.actuate(1.0, 0.4):
                self.sim.sim.step()
        else:
            self.baxter_gripper_left.release()
            while not self.baxter_gripper_left.actuate(1.0, 0.4):
                self.sim.sim.step()

    def pour(self, left):
        if left:
            joints = self.baxter_left.get_joint_target_positions()
            joints[6] = joints[6] - math.pi

            self.baxter_left.set_joint_target_positions(joints)
            for i in range(30):
                self.sim.sim.step()
            sleep(1.5)

            joints[6] = joints[6] + math.pi
            self.baxter_left.set_joint_target_positions(joints)
            for i in range(30):
                self.sim.sim.step()

        else:
            joints = self.baxter_right.get_joint_target_positions()
            joints[6] = joints[6] - math.pi

            self.baxter_right.set_joint_target_positions(joints)
            for i in range(30):
                self.sim.sim.step()
            sleep(1.5)

            joints[6] = joints[6] + math.pi
            self.baxter_right.set_joint_target_positions(joints)
            for i in range(30):
                self.sim.sim.step()

    def pick_and_pour(self, ingredient):
        # Some comment to explain here
        ingr = self.sim.ingredients[ingredient]
        # print(ingr)
        if ingr is None:
            print("Error: missing ingredient requested...")
            return -1
        if ingredient == "gin" or ingredient == "vermut":
            left = True
        else:
            left = False
        # self.move(self.sim.waypoints[10])

        # print(self.baxter_left.get_joint_positions())
        print(self.baxter_right.get_joint_positions())

        self.move(self.sim.waypoints[ingr[0]])
        self.move(self.sim.waypoints[ingr[1]], ignore_collision=True)

        self.grasp(ingr[3])

        # print("Grasping done!")

        self.move(self.sim.waypoints[ingr[2]], ignore_collision=True)
        if left:
            self.move(self.sim.waypoints[2])
        else:
            pass    # TODO

        # TODO
        self.pour(left)

        self.move(self.sim.waypoints[ingr[2]])
        # self.move(self.sim.waypoints[ingr[0]])
        self.move(self.sim.waypoints[ingr[1]], ignore_collision=True)

        self.release(ingr[3])

        # TODO
        self.reset_pos()
