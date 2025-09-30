from pyb import ADC, Pin, Timer
from array import array
import time
"""
Author: Michael Shokoohi
Term: Fall 2025
Course: Mechatronics ME 405
Assignment Description:  
Notes: Resistor: 20.13 k Ohm
       Capacitor: 3.72 uF
       Resistor to Nucleo input: 6.10 k Ohm
       Signal Goes to PC0
       Step output goes to PC1
"""


#Pre allocating array for data storage
# H is used to represent data type..... 
data = array('H', 1000*[0])

#Config PC1 as digital output 
PC1 = Pin(Pin.cpu.C1, mode=Pin.OUT_PP)
#Config PC0 as Analog pin
PC0= Pin(Pin.cpu.C0, mode=Pin.ANALOG)

#Config ADC to be attached to PC0
adc= ADC(PC0)




i=0


def tim_cb(tim):
    '''
    Call back func that triggers input to RC circut and collects data for 5X as long  as 
    Tau. 

    Trigger output on call back
    after that never drop it 
    record for 5Tau
    append data to array 
    '''
    global data
    global i

    #Activating the step response on second run through callback function. 
    if i==1:
        PC1.high()

    if i<1000:
        data[i]= adc.read()
        i=i+1
    else:
        tim.callback(None)
    


#Creating timer object for Timer number 7 
tim7 = Timer(7, freq=1000) 
# Assign the callback function 
tim7.callback(tim_cb)     


time.sleep_ms(1000)

#tim7.callback(None)     # disable the callback
PC1.low()



def Publish(data):
    '''
    loop through the data array and push it to the putty terminal
    '''
    idx=0
    print(data)
    for idx, value in enumerate(data):
        
        print(f"{idx}, {value}")
    
    
    

if __name__=='__main__':
    Publish(data)



