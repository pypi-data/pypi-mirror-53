# import CarConf
from ddcmaker import CarMotor
import time
carM = CarMotor.CarMotor()

class car(object):
    def right(self, step):
        carM.SetSpeed(50, -50)
        time.sleep(step)
        self.stop()
        print("小车右转" + str(step) + "步")
    def left(self, step):
        carM.SetSpeed(-50, 50)
        time.sleep(step)
        self.stop()
        print("小车左转"+str(step)+"步")

    def forward(self, step):
        carM.SetSpeed(50, 50)
        time.sleep(step)
        self.stop()
        print("小车前进" + str(step) + "步")

    def stop(self):
        carM.SetSpeed(0, 0)


    def backward(self, step):
        carM.SetSpeed(-50, -50)
        time.sleep(step)
        self.stop()
        print("小车后退" + str(step) + "步")



