from pyb import Pin, Timer, USB_VCP, UART, delay
from motor import Motor 
from encoder import Encoder
from utime import ticks_us, ticks_add, ticks_diff
import task_share


"""
    When I run here 
    how do I time stamp the data? 
    How do I make sure I run for 2 seconds without blocking? 
    (we can make element 0 equal to t=0)
    is the indexing used for Queues already done for me. (yes)
    (use full queu as stop indicator)

    Can anyone put into shars or is it "owned by anyone" (yes)      
"""


class CollectionTask:
    def __init__(self):

        self.desired_effort: int =20
        self.collection_task_state:str= "SetUp"

    def test_cycle(self, shares):


        (good_to_publish,
         start_test, 
         collecting_data, 
         time,
         right_side_position, 
         left_side_position, 
         right_side_velocity,
         left_side_velocity)= shares
        
        while(True):
            
            if (self.collection_task_state=="SetUp"):

                
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

                RightEncoder.zero()
                LeftEncoder.zero()


                RightMotor.set_effort(0)
                LeftMotor.set_effort(0)

                RightMotor.enable()
                LeftMotor.enable()

                self.collection_task_state="Idle"


                    
            elif (self.collection_task_state=="Idle"):
                """
                Checking for Share Labeled start_test to move to run case
                """
                if start_test.get()==1:
                    start_test.put(0)
                    self.collection_task_state= "Run"

                else:
                    self.collection_task_state= "Idle"
                    RightMotor.set_effort(0)
                    LeftMotor.set_effort(0)

            elif (self.collection_task_state=="Run"):

                #Raise flag that data collection has started
                collecting_data.put(1)
                

                #Start motors and encoders to get step response
                RightMotor.set_effort(self.desired_effort)
                LeftMotor.set_effort(self.desired_effort)
                RightEncoder.update()
                LeftEncoder.update()


                #Start Recording data into the arrays 
                
                right_side_position.put(int(RightEncoder.get_position()))
                left_side_position.put(int(LeftEncoder.get_position()))

                right_velocity, delta_time = RightEncoder.get_velocity()
                left_velocity, _ = LeftEncoder.get_velocity()

                delta_time=1000000*delta_time
                #Returning in Microseconds
                time.put(int(delta_time))

                right_side_velocity.put(int(right_velocity))
                left_side_velocity.put(int(left_velocity))

                #Keep running and set effort to 0 after X seconds
                if time.full():
                    collecting_data.put(0)
                    good_to_publish.put(1)
                    self.collection_task_state= 'Idle'
                    

            

            print(f'Collection Task State is: {self.collection_task_state}')
            print(f"Number of items in Time Queue is: {time.num_in()}")
            yield self.collection_task_state







class SerialTask:
    def __init__(self):
        self.serial_task_state= "Idle"
        self.ser=USB_VCP()

        self.uart= UART(3, 115200, bits=8, parity=None, stop=1, timeout=100, timeout_char=10)

        self.number=0

    def publish(self,shares):

        (good_to_publish,
         start_test, 
        collecting_data, 
        time,
        right_side_position, 
        left_side_position, 
        right_side_velocity,
        left_side_velocity)= shares

        data=[]
        


        while (True):


            if (self.serial_task_state=="Idle"):
                
                "This task is monitoring for input from putty to start data collection cycle "

                # This code snip was used for interacting with putty to start data collection cycle
                """
                if self.ser.any():
                    user_input=self.ser.read(1).decode()
                    if user_input=="S":
                        start_test.put(1)
                        self.serial_task_state="Publishing"
                """

                #Monitoring UART incoming serial to detect start condition for data collection cycle
                if self.uart.any() !=0:
                    message=self.uart.read()

                    if message== b'U\r\n':
                        start_test.put(1)
                        self.serial_task_state="Publishing"


                    
            elif (self.serial_task_state=="Publishing"):
                "This step is printing data to serial monitor "

                if collecting_data.get()==0 and good_to_publish.get()==1: 
                    print('Entering Print Loop')

                    #Code used for printing to putty 
                    """
                    time_data=[]
                    right_side_position_data=[]
                    left_side_position_data =[]
                    right_side_velocity_data=[]
                    left_side_velocity_data=[]

                    while time.any():
                        time_data.append(time.get())
                        right_side_position_data.append(right_side_position.get())
                        left_side_position_data.append(left_side_position.get())
                        right_side_velocity_data.append(right_side_velocity.get())
                        left_side_velocity_data.append(left_side_velocity.get())

                    
                    print(f"time_data:{time_data}")
                    print(f"right_side_position_data:{right_side_position_data}")
                    print(f"left_side_position_data:{left_side_position_data}")
                    print(f"right_side_velocity_data:{right_side_velocity_data}")
                    print(f"left_side_velocity_data:{left_side_velocity_data}")
                    """

                    #Blutooth code 
                    
                    while time.any():
                        self.number=self.number+1
                        data= f"{self.number},{time.get()}, {right_side_position.get()},{left_side_position.get()}, {right_side_velocity.get()},{left_side_velocity.get()} \n"
                        self.uart.write(data.encode())
                        delay(5)


                    if time.empty():
                        good_to_publish.put(0)
                        self.serial_task_state='Idle'
                        self.number=0


            print(f'SerialTask Task State is: {self.serial_task_state}')
            yield self.serial_task_state
