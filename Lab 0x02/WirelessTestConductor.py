from serial import Serial
from time import sleep, perf_counter
from matplotlib import pyplot as plt
import numpy as np



time_data=[]
right_velocity=[]



right_side_position_data=[]
left_side_position_data =[]

right_side_velocity_data=[]
left_side_velocity_data=[]

 

with Serial("COM5", baudrate=115_200, timeout=1) as ser: 



    print("Opening serial port") 
    sleep(0.5) 
    print("Flushing serial port") 



    print("Sending command to start data collection") 
    ser.write("U\r\n".encode()) 

    start_time=perf_counter()
    while True:

        elapsed= perf_counter()-start_time
        if ser.in_waiting:
            data=ser.readline() 
            PROCESSED = data.decode('utf-8', errors='ignore').strip()  # now it's str, no b''
            parts = [p.strip() for p in PROCESSED.split(',')]

            print(parts)
            
            if '-' in parts[4]:
                continue

            time_data.append(parts[1])
            right_velocity.append(parts[4])
            
        else: 
            if elapsed > 10:
                break
            
times= list(map(float, time_data))
cumulative_time = np.cumsum(times)


velocities= list(map(float, right_velocity))
print(f"lenCum:{len(cumulative_time)}, lentimes: {len(times)}")

plt.plot(cumulative_time[:100],velocities[:100])
plt.xlabel("Time in ms")
plt.ylabel("Velocity in mm/s ")
plt.title("Velocity vs. Time")

plt.show()

 

 

