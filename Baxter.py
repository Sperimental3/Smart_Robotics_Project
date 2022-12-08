import numpy as np
import math
from time import sleep
from pyrep.robots.arms.baxter import BaxterLeft, BaxterRight
from pyrep.robots.end_effectors.baxter_gripper import BaxterGripper


class Baxter:
    def __init__(self, sim):

        self.sim = sim

        self.baxter_left = BaxterLeft()
        self.baxter_right = BaxterRight()
        self.baxter_gripper_left = BaxterGripper(0)
        self.baxter_gripper_right = BaxterGripper(1)

        """
        print(self.baxter_gripper_right.get_joint_target_positions(),
              self.baxter_gripper_right.get_joint_positions())
        
        print(self.baxter_left.get_joint_target_positions(), self.baxter_left.get_joint_positions())
        """

        self.rest_left = [0.12206578254699707, -0.43517088890075684, -0.16766047477722168,
                          2.0112273693084717, 0.8295693397521973, -1.4581592082977295,
                          0.10328960418701172]
        # self.rest_gripper_left = [0.05730545520782471, 0.05783754587173462]

        self.rest_right = [-0.40036916732788086, -0.2947428226470947, 0.5197999477386475,
                           2.0722572803497314, -0.9089522361755371, -1.249591588973999,
                           -0.4194943904876709]
        # In the constructor method I've decided to not initialize the position, and to let the pick_and_pour and
        # reset_pos method takes care of that, this to try to avoid at maximum possible interferences between arms

        """
        self.baxter_left.set_joint_target_positions(self.rest_left)
        # self.baxter_gripper_left.set_joint_positions(self.rest_gripper_left)
        # self.baxter_right.set_joint_target_positions(self.rest_right)
        for i in range(30):
            self.sim.sim.step()
        """
        # print(self.baxter_gripper_left.get_joint_target_positions(), self.baxter_gripper_left.get_joint_positions())

    def move(self, location, ignore_collision=False, left=True):
        try:
            if not left:
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
            print(f"Could not find a path using get_path(), solving iteratively trough jacobian ik...")

        # seeing all my tests the code below should never happen, also because is much slower than get_path,
        # due to the recursion

        if location.get_position()[1] < 0:
            pos = self.baxter_right.get_tip().get_position()
            quat = self.baxter_right.get_tip().get_quaternion()
            arm = self.baxter_right
        else:
            pos = self.baxter_left.get_tip().get_position()
            quat = self.baxter_left.get_tip().get_quaternion()
            arm = self.baxter_left

        orientation = np.array(location.get_quaternion())
        location = np.array(location.get_position())

        pos = np.array(pos)
        quat = np.array(quat)

        for i in range(50):
            delta_pos = pos + i*(location - pos)/50
            delta_quat = quat + i*(orientation - quat)/50

            try:
                ik = arm.solve_ik_via_jacobian(delta_pos, quaternion=delta_quat)
            except Exception:
                print(f"Could not get to {location}, stopped at {delta_pos}...")
                ik = arm.solve_ik_via_sampling(position=delta_pos, quaternion=delta_quat, max_configs=10)

            arm.set_joint_target_positions(ik)
            self.sim.sim.step()
        return True

    def reset_pos(self, left):
        if left:
            """
            self.baxter_left.set_joint_positions([0, 0, 0, 0, 0, 0, 0], disable_dynamics=True)
            self.baxter_gripper_left.set_joint_positions([0.05999999865889549, 0.05999999865889549], disable_dynamics=True)
            for i in range(30):
                self.sim.sim.step()
            """
            """
            print(self.baxter_gripper_left.get_joint_target_positions(),
                  self.baxter_gripper_left.get_joint_positions())
            print(self.baxter_left.get_joint_target_positions(), self.baxter_left.get_joint_positions())
            """

            self.baxter_left.set_joint_target_positions(self.rest_left)
            # self.baxter_gripper_left.set_joint_positions(self.rest_gripper_left)
            for i in range(30):
                self.sim.sim.step()

            """
            print(self.baxter_gripper_left.get_joint_target_positions(),
                  self.baxter_gripper_left.get_joint_positions())
            print(self.baxter_left.get_joint_target_positions(), self.baxter_left.get_joint_positions())
            """
        else:
            self.baxter_right.set_joint_target_positions(self.rest_right)
            for i in range(30):
                self.sim.sim.step()

    def grasp(self, obj):
        # Here it is absolutely crucial to put the grasp method before the actuation,
        # at the contrary on what the PyRep reference says
        if obj.get_position()[1] < 0:
            self.baxter_gripper_right.grasp(obj)
            while not self.baxter_gripper_right.actuate(0.0, 0.4):
                self.sim.sim.step()
        else:
            self.baxter_gripper_left.grasp(obj)
            while not self.baxter_gripper_left.actuate(0.0, 0.4):
                self.sim.sim.step()

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

        return True

    def pour(self, left):
        # This method wants to simply rotate the end effector of pi angle,
        # with some limitations due to the joints position
        if left:
            joints = self.baxter_left.get_joint_positions()
            joints[6] = joints[6] - math.pi

            self.baxter_left.set_joint_target_positions(joints)
            for i in range(30):
                self.sim.sim.step()

            sleep(1)    # To simulate the liquid pouring

            joints[6] = joints[6] + math.pi
            self.baxter_left.set_joint_target_positions(joints)
            for i in range(30):
                self.sim.sim.step()
        else:
            joints = self.baxter_right.get_joint_positions()
            joints[6] = joints[6] + math.pi

            self.baxter_right.set_joint_target_positions(joints)
            for i in range(30):
                self.sim.sim.step()

            sleep(1)

            joints[6] = joints[6] - math.pi
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
        # self.move(self.sim.waypoints[10], left=left)
        # self.move(self.sim.waypoints[21], left=left)

        # print(self.baxter_left.get_joint_positions())
        # print(self.baxter_right.get_joint_positions())
        if not left:
            self.baxter_right.set_joint_target_positions(self.rest_right)
            for i in range(30):
                self.sim.sim.step()
            while not self.baxter_gripper_right.actuate(1.0, 0.4):
                self.sim.sim.step()
        else:
            self.baxter_left.set_joint_target_positions(self.rest_left)
            for i in range(30):
                self.sim.sim.step()

        self.move(self.sim.waypoints[ingr[0]], left=left)
        self.move(self.sim.waypoints[ingr[1]], ignore_collision=True, left=left)

        self.grasp(ingr[3])

        # print("Grasping done!")

        self.move(self.sim.waypoints[ingr[2]], ignore_collision=True, left=left)
        if left:
            self.move(self.sim.waypoints[2], left=left)
        else:
            self.move(self.sim.waypoints[20], left=left)

        self.pour(left)

        self.move(self.sim.waypoints[ingr[2]], left=left)
        self.move(self.sim.waypoints[ingr[1]], ignore_collision=True, left=left)

        self.release(ingr[3])
        self.move(self.sim.waypoints[ingr[0]], left=left)

        self.reset_pos(left)
