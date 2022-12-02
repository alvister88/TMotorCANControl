from sys import path
path.append("/home/pi/TMotorCANControl/src/")
from TMotorCANControl.TMotorManager_servo_can import *
from NeuroLocoMiddleware.SoftRealtimeLoop import SoftRealtimeLoop
from NeuroLocoMiddleware.StatProfiler import SSProfile
import numpy as np

Pdes = 0
Vdes = 0

P = 5
D = 0.0

with TMotorManager_servo_can(motor_type='AK80-9', motor_ID=0, CSV_file=None) as dev:
    loop = SoftRealtimeLoop(dt=0.005, report=True, fade=0.0)
    dev.zero_position()
    
    dev.update()
    dev.enter_current_control()
    time.sleep(1)
    
    for t in loop:
        Pdes = 2*np.sin(t)
        cmd =  P*(dev.θ - Pdes) + D*(Vdes - dev.θd)
        dev.i = cmd
        dev.update()

        