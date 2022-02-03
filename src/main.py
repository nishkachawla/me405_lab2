"""!
@file main.py
This file contains code used to operate the ME405 motor.

@details The main script calls the MotorDriver class and EncoderDriver class,
imported as modules, to operate the motor and encoders.
    
@author Nishka Chawla
@author Ronan Shaffer
@date   26-Jan-2022
@copyright (c) Released under GNU Public License
"""

import pyb
import utime
import motor_chawla_shaffer
import encoder_chawla_shaffer
import closedloopcontrol
import array as array
import shares

def main():
    """!
    This method is used to generate a step response for a motor.
    """   
    ## Input pin configuration
    inn = pyb.Pin.IN
    
    ## Output with push-pull control pin configuration
    out = pyb.Pin.OUT_PP
    
    # Define motor pins
    ## The enable pin for the motor. 
    pinEN = pyb.Pin(pyb.Pin.cpu.A10, out)
    ## Pin variable for channel A of the motor.
    pinB4 = pyb.Pin(pyb.Pin.cpu.B4, out)
    ## Pin variable for channel B of the motor.
    pinB5 = pyb.Pin(pyb.Pin.cpu.B5, out)
    
    # Define encoder pins
    ## Pin variable for channel 1 of the encoder A.
    pinB6 = pyb.Pin(pyb.Pin.cpu.B6, out)
    ## Pin variable for channel 2 of the encoder A.
    pinB7 = pyb.Pin(pyb.Pin.cpu.B7, out)
    ## Pin variable for channel 1 of the encoder B.
    pinC6 = pyb.Pin(pyb.Pin.cpu.C6, out)
    ## Pin variable for channel 2 of the encoder B.
    pinC7 = pyb.Pin(pyb.Pin.cpu.C7, out)
    
    ## Index to iterate through arrays
    runs = 0
    
    ## Array size
    array_size = int((2000/10)+1)
    
    ## Array storing time data.
    time_list = array.array("f", [0] * array_size)
    ## Array storing position data.
    pos_list = array.array("f", [0] * array_size)
    
    ## Instantiation of motor object.
    moe = motor_chawla_shaffer.MotorDriver(pinEN, pinB4, pinB5, 3)
    # ## Instantiation of encoder 1 object.
    # encoder1 = encoder_chawla_shaffer.EncoderDriver(pinB6, pinB7, 4)
    ## Instantiation of encoder 2 object.
    encoder2 = encoder_chawla_shaffer.EncoderDriver(pinC6, pinC7, 8)
    encoder2.zero()
    ## Instantiation of controller object.
    controller = closedloopcontrol.ClosedLoop(int(16384), float(0.1), int(100), int(-100))
    
    ## Input for Kp 
    Kp = input('Please enter a Kp: ')
    controller.set_Kp(float(Kp))

    ## Start time variable.
    start_time = utime.ticks_ms()
    ## Next time variable.
    next_time = utime.ticks_add(utime.ticks_ms, 10)
    

    while runs <= 200:
#         print('runs: ', runs)
        # Sets motor duty cycle to actuation level
        encoder2.update()
        ## Variable storing Encoder 2 position.
        count_B = encoder2.read()
        moe.set_duty_cycle(controller.run(count_B))
        
        ## Position data list
        pos_list[runs] = count_B
        utime.sleep_ms(10)
        # print('ENCA:',count_A,'ENCB:',count_B)
        ## Index time variable
        g_time = utime.ticks_ms()
        
        ## Time data list
        time_list[runs] = utime.ticks_diff(g_time, start_time)
        
        ## Index time variable
        next_time = utime.ticks_add(next_time, 10)
        runs += 1
        
        
    controller.get_stepresponse(time_list, pos_list)

if __name__ == '__main__':
    main()
    