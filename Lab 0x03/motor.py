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


        #Variables for motor PID control
        self.kp=.8
        self.ki=0
        self.kd=0
        self.last_proportional_term=0
    
    def set_effort(self, effort:float):
        '''Sets the present effort requested from the motor based on an input value
           between -100 and 100'''
        
        if effort>0:
            self.Direction.low()
            self.PWM.pulse_width_percent(effort)
        else:
            self.Direction.high() 
            self.PWM.pulse_width_percent(effort)
    
    """
    def set_direction(self,Direction: str):
        if Direction == 'Forward':
            
        elif Direction == 'Reverse':   
    """  

    def enable(self):
        '''Enables the motor driver by taking it out of sleep mode into brake mode'''
        self.nSLP.high()
            
    def disable(self):
        '''Disables the motor driver by taking it into sleep mode'''
        self.nSLP.low()

    def controlled_effort(self,set_point,current_velocity,delta_time,kp,ki,kd):
        """
        This function takes in the desired set point, and current velocity to modulate the motor output using the set_effort function
        """
        self.kp=kp
        self.ki=ki
        self.kd= kd
        
        #Define error terms 
        proportional_term=set_point-current_velocity
        integral_term= proportional_term*delta_time
        derivative_term= (proportional_term-self.last_proportional_term)/delta_time

        #PID equation
        new_effort= self.kp*proportional_term + self.ki*integral_term + self.kd*derivative_term


        #Update motor efforts
        self.set_effort(new_effort)


        # Update proportional term for use in next cycle 
        self.last_proportional_term=proportional_term

