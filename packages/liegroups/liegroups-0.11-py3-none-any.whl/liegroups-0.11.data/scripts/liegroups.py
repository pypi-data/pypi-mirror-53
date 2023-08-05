import numpy as np
import copy
from math import isclose


class SE2:

    def __init__(self, *args, **kwargs):
        try:
            if len(args) == 3:
                self.translation = [float(args[0]), float(args[1])]
                self.angle = self.normalizeYaw(float(args[2]))
            elif len(args) == 2:
                self.translation = [float(args[0]), float(args[1])]
            elif len(args) == 1:
                self = copy.deepcopy(args[0])

            else:
                self.translation = [0., 0.]
                self.angle = 0.

        except:
            print("Argument error! ", args)


    def copy(self):
        return copy.deepcopy(self)


    def __mul__(self, other):
        se2 = self.copy()
        se2.translation += np.dot(se2.rotationMatrix(), other.translation)
        se2.angle = se2.normalizeYaw(se2.angle + other.angle)
        return se2


    def __eq__(self, other):
        return (isclose(self.x(), other.x(), abs_tol=1e-6) and isclose(self.y(), other.y(), abs_tol=1e-6) and isclose(
            self.yaw(), other.yaw(), abs_tol=1e-6))


    def x(self):
        return self.translation[0]


    def y(self):
        return self.translation[1]


    def yaw(self):
        return self.angle


    def rotationMatrix(self):
        '''
        Create 2D rotation matrix from given angle
        '''
        return np.array([[np.cos(self.angle), -np.sin(self.angle)],
                         [np.sin(self.angle), np.cos(self.angle)]])


    def normalizeYaw(self, y):
        '''
        Normalizes the given angle to the interval [-pi, +pi]
        '''
        while y > np.pi:
            y -= 2. * np.pi
        while y < -np.pi:
            y += 2. * np.pi
        return y


    def inv(self):
        '''
        Return inverse SE2
        '''
        se2 = self.copy()
        se2.angle = self.normalizeYaw(-self.angle)
        print("angle ", se2.angle)
        print("rot ", se2.rotationMatrix())
        se2.translation = np.dot(se2.rotationMatrix(), np.dot(self.translation, -1))
        return se2


    def print(self):
        return "SE2: {0:.2f}".format(self.x()) + " {0:.2f}".format(self.y()) + " {0:.2f}".format(
            np.rad2deg(self.yaw()))


    def test(self):
        '''
        Move me to test...
        '''
        degree = 10

        pose = SE2(0, 1, np.deg2rad(degree))
        pose2 = SE2(10, 1, np.deg2rad(degree + 100))

        print("pose1", pose.print())
        pose3 = pose * pose2
        print("pose11", pose.print())

        new_pose = pose.copy()
        new_pose.translation[0] = 100
        print("new_pose", new_pose.print())

        print(pose3 == SE2(9.6744294, 3.7212895, np.deg2rad(120.)))
        delta_se2 = pose.inv() * pose2
        inverse = pose.inv()
        print("pose", pose.print())
        print("inverse: ", inverse.print())
        print(delta_se2 == SE2(9.8480775, -1.7364818, np.deg2rad(100.)))

