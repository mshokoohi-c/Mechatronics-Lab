from pyb import Pin, Timer, ExtInt
from Motor import Motor 
from Encoder import Encoder 
from utime import ticks_us, ticks_add, ticks_diff



#SETUP

# Defining Timer object that is used for both Motors
MotorTim= Timer(3,freq=20000)


# Defining Timer objects for each encoder to use
LEncTim= Timer(1,prescaler=0,period=0xFFFF)
REncTim= Timer(2,prescaler=0,period=0xFFFF)


# Setup Motor and Encoder Objects
RightMotor=Motor(Pin.cpu.A7,Pin.cpu.B14,Pin.cpu.B13,MotorTim,2)
RightEncoder=Encoder(REncTim,Pin.cpu.A0,Pin.cpu.A1,'Right')

LeftMotor=Motor(Pin.cpu.A6,Pin.cpu.B3,Pin.cpu.A10,MotorTim,1)
LeftEncoder=Encoder(LEncTim,Pin.cpu.A8,Pin.cpu.A9, 'Left')




#Set interval to 20Hz
interval= 5_000 #us
start= ticks_us()

deadline= ticks_add(start,interval)
RightEncoder.zero()
LeftEncoder.zero()


LoopCounter=0
RightMotor.enable()
RightMotor.set_effort(100)
#RightMotor.set_direction('Reverse')

while True:

    now= ticks_us()

    if ticks_diff(deadline,now) <=0:
        
        RightEncoder.update()
        LeftEncoder.update()

        LoopCounter+=1
        if LoopCounter%10==0:
            print(f'Right Encoder Count is {RightEncoder.CurrentCount}')
            print(f'Right Encoder Traveled {RightEncoder.get_position()} mm')
            RightEncoder.get_velocity()
        #Make the next deadline
        deadline= ticks_add(deadline, interval)




