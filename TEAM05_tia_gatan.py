import sys
sys.path.append('c:/users/supervisor/utilities/maestro/')

import maestro

"""
position_neutral = 7080
position_TIA = 6532
position_Gatan = 8000
"""

def set_TIA():
    with maestro.Controller(ttyStr='COM4') as servo:
        position = 6532
        # 10 is a good speed
        servo.setSpeed(1, 10)

        x = servo.getPosition(1) #get the current position of servo 1
        print('Starting position = {}'.format(x))
    
        servo.setTarget(1, position)
    
        y = servo.getPosition(1) #get the current position of servo 1
        print('new position = {}'.format(y))
        
def set_Gatan():
    with maestro.Controller(ttyStr='COM4') as servo:
        position = 8000

        # 10 is a good speed
        servo.setSpeed(1, 10)

        x = servo.getPosition(1) #get the current position of servo 1
        print('Starting position = {}'.format(x))
    
        servo.setTarget(1, position)
    
        y = servo.getPosition(1) #get the current position of servo 1
        print('new position = {}'.format(y))
        
def set_neutral():
    with maestro.Controller(ttyStr='COM4') as servo:
        position = 7080

        # 10 is a good speed
        servo.setSpeed(1, 10)

        x = servo.getPosition(1) #get the current position of servo 1
        print('Starting position = {}'.format(x))
    
        servo.setTarget(1, position)
    
        y = servo.getPosition(1) #get the current position of servo 1
        print('new position = {}'.format(y))