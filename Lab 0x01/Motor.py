from pyb import Pin, Timer

class Motor:
    '''A motor driver interface encapsulated in a Python class. Works with
       motor drivers using separate PWM and direction inputs such as the DRV8838
       drivers present on the Romi chassis from Pololu.'''
    
    def __init__ (self, PWM_PIN: Pin, DIR_PIN: Pin, nSLP_PIN: Pin,
                  Tim: Timer, Channel: int):
        

        self.Direction= Pin(DIR_PIN, mode=Pin.OUT_PP)
        self.nSLP= Pin(nSLP_PIN, mode=Pin.OUT_PP)
        self.PWM= Tim.channel(Channel,pin=PWM_PIN,mode=Timer.PWM)
    
    def set_effort(self, effort:float):
        '''Sets the present effort requested from the motor based on an input value
           between -100 and 100'''
        self.PWM.pulse_width_percent(effort)

    
    def set_direction(self,Direction: str):
        if Direction == 'Forward':
            self.Direction.low()
        elif Direction == 'Reverse':   
            self.Direction.high() 

    def enable(self):
        '''Enables the motor driver by taking it out of sleep mode into brake mode'''
        self.nSLP.high()
            
    def disable(self):
        '''Disables the motor driver by taking it into sleep mode'''
        self.nSLP.low()

