from pyb import Timer, Pin
from utime import ticks_us, ticks_add, ticks_diff

class Encoder: 

    # I want to pass in full timer objects and pin numbers for things

    def __init__(self,tim, chA_pin, chB_pin, SideOfRobot:str):
        
        #Refers to the side of the chassis that the particular 
        # encoder object is referring to
        self.SideOfRobot=SideOfRobot
        self.position=0
        
        self.previous_count=0
        self.delta_count=0
        self.CorrectedDelta=0
        self.CurrentCount=0


        self.DeltaTime=0
        self.Velocity=0


        #Passing timer object 
        self.Tim=tim

        # Put the timer in encoder mode
        self.ch1 = tim.channel(1, Timer.ENC_AB, pin=chA_pin)
        self.ch2 = tim.channel(2, Timer.ENC_AB, pin=chB_pin)

        self.ARCutOff=(65535+1)/2
        self.AR=(65535+1)

    def update(self):
        """
        This function needs to run at a high enough frequency to that the encoder count 
        cant go more than .5AR

        Read the count to calc the delta count

        Detect Over/Under flow 

        Add the adjusted delta count to the Real count which is used for 
        position and velocity
        """
        #Calc the delta Count

        self.delta_count= self.Tim.counter()-self.previous_count

        if self.delta_count<=-self.ARCutOff:
            # overflow occured
            print(f'{self.SideOfRobot} Encoder Overflowed')
            self.CorrectedDelta=self.delta_count+self.AR

        elif self.delta_count>=self.ARCutOff:
            #Underflow occured
            print(f'{self.SideOfRobot} Encoder Underflowed')
            self.CorrectedDelta=self.delta_count-self.AR

        else:
            self.CorrectedDelta=self.delta_count
        

        
        self.CurrentCount=self.CurrentCount+self.CorrectedDelta


        #Update the previous count for next run
        self.previous_count=self.Tim.counter()
        #Time Stamping the Previous encoder count
        self.PreviousCountStamp=ticks_us()

    def get_position(self):

        self.position= self.CurrentCount*(1/12)*(1/119.76)*(2*3.14159*35)

        return self.position

    def get_velocity(self):
        
        #calc the velocity in mm/s
        now=ticks_us()
        self.Deltatime=abs(ticks_diff(self.PreviousCountStamp,now))/(1E6)

        #Converting from ticks to mm 
        distance_delta= self.CorrectedDelta*(1/12)*(1/119.76)*(2*3.14159*35)

        #print(f"Delta Time is {self.Deltatime}")
        self.Velocity= distance_delta/self.Deltatime

        #print(f'Speed of {self.SideOfRobot} Wheel is {self.Velocity}mm/s')
        return self.Velocity, self.Deltatime
        

    def zero(self):
        self.position=0
        self.CurrentCount=0
        self.previous_count=0







