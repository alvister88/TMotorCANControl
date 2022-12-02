from NeuroLocoMiddleware.SoftRealtimeLoop import SoftRealtimeLoop
# try:
#      from TMotorCANControl.TMotorManager import TMotorManager
# except ModuleNotFoundError:
from sys import path
path.append("/home/pi/TMotorCANControl/src/")
from TMotorCANControl.TMotorManager_servo_can import TMotorManager_servo_can
import time


with TMotorManager_servo_can(motor_type='AK80-9', motor_ID=0, CSV_file="log.csv") as dev:
    
    loop = SoftRealtimeLoop(dt=0.01, report=True, fade=0.0)
    dev.enter_current_control()
    dev.zero_position()
    for t in loop:
        dev.i = 0
        dev.update()
        print("\r" + str(dev),end='')