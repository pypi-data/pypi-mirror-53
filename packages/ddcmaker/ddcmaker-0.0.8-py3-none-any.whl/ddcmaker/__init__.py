'''不要随意修改类名和参数名，谁改谁背锅！！！！'''
__version__ = '0.0.8'
__metaclass__ = type
__all__ = [
    'car', 'robot'
]
'''通过固定的文件夹判断设备的种类'''

import os

if os.path.exists('/home/pi/human') == True:
    from ddcmaker import robot
    from ddcmaker import showlib
    Rb = robot.robot()
    Sh = showlib.showlib()
if os.path.exists('/home/pi/Car') == True:
    from ddcmaker import car
    Ca = car.car()
else:
    print("当前目录没有找到小车的系统！")

class Robot(object):

    @staticmethod
    def left(step):
        Rb.left(step)

    @staticmethod
    def right(step):
        Rb.right(step)

    @staticmethod
    def left_slide(step):
        Rb.right_slide(step)

    @staticmethod
    def right_slide(step):
        Rb.right_slide(step)

    @staticmethod
    def forward(step):
        Rb.forward(step)

    @staticmethod
    def backward(step):
        Rb.backward(step)

    @staticmethod
    def up(step):
        Rb.up(step)

    @staticmethod
    def down(step):
        Rb.down(step)

    @staticmethod
    def check(step):
        Rb.check(step)

    @staticmethod
    def circle(step, radius):
        Rb.circle(step, radius)

    @staticmethod
    def nod(step):
        Rb.nod(step)

    @staticmethod
    def shaking_head(step):
        Rb.shaking_head(step)

    '''虚不实真，苦切一除能，咒等等无是，咒上无是，咒明大是'''

    @staticmethod
    def hiphop():
        Sh.hiphop()

    @staticmethod
    def smallapple():
        Sh.smallapple()

    @staticmethod
    def jiangnanstyle():
        Sh.jiangnanstyle()

    @staticmethod
    def lasong():
        Sh.lasong()

    @staticmethod
    def feelgood():
        Sh.feelgood()
    '''无法兼容白色机器人，在调用是进行机器人判断'''


class Car(object):

    @staticmethod
    def left(step):
        Ca.left(step)

    @staticmethod
    def right(step):
        Ca.right(step)

    @staticmethod
    def forward(step):
        Ca.forward(step)

    @staticmethod
    def backward(step):
        Ca.backward(step)
