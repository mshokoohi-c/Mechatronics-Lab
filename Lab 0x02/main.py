from tasks import CollectionTask, SerialTask
import task_share
import cotask
import gc
from pyb import Pin, Timer, ExtInt
from utime import ticks_us, ticks_add, ticks_diff




if __name__ == '__main__':

    Collector= CollectionTask()
    SerialHandler=SerialTask()


    #Create Share and queue objects 
    good_to_publish= task_share.Share('b',thread_protect=False,name="Good To Publish")
    start_test=task_share.Share('b',thread_protect=False,name="Start Test")
    collecting_data= task_share.Share('b',thread_protect=False,name="Collecting Data")
    done_collecting= task_share.Share('b',thread_protect=False,name="Done Collecting")

    time= task_share.Queue('h', 100, thread_protect=False, overwrite=False,
                          name="time")
    
    right_side_position= task_share.Queue('h', 100, thread_protect=False, overwrite=False,
                          name="Right Position")
    left_side_position= task_share.Queue('h', 100, thread_protect=False, overwrite=False,
                          name="Left Position")
    right_side_velocity= task_share.Queue('h', 100, thread_protect=False, overwrite=False,
                          name="Right Velocity")
    left_side_velocity= task_share.Queue('h', 100, thread_protect=False, overwrite=False,
                          name="Left Velocity")


    #Create Task objects
    collection_task = cotask.Task(Collector.test_cycle, name="Collection_Task", priority=2, period=50,
                            profile=True, trace=False, shares=(good_to_publish,start_test, 
         collecting_data, 
         time,
         right_side_position, 
         left_side_position, 
         right_side_velocity,
         left_side_velocity))
    

    serial_task= cotask.Task(SerialHandler.publish, name="Serial_Task", priority=1, period=100,
                            profile=True, trace=False, shares=(good_to_publish,start_test, 
         collecting_data, 
         time,
         right_side_position, 
         left_side_position, 
         right_side_velocity,
         left_side_velocity))
                        
    

    cotask.task_list.append(collection_task)
    cotask.task_list.append(serial_task)


    # Run Garbage collector, to defragment memory 
    gc.collect()


    # Run Scheduler and Quit if (crtl + c) is pressed
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
             #Print information
            print('\n' + str (cotask.task_list))
            print(task_share.show_all())
            #print(task1.get_trace())
            print('') 
            break

        
       
        