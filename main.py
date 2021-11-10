#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
m1 = Motor(Port.B)
m2 = Motor(Port.C)

stopW = StopWatch()
data = DataLog('nr','runtime', name='PWlog10', timestamp=False, extension='txt')
cs = ColorSensor(Port.S4)  #place colorsensor in port 4 or change this value to match



# Write your program here.
ev3.speaker.beep()

#init buffer array for previous sensor readings
buf_index = 0
size = 3
buf_array = [100]*size
reset_array = [100]*size

state = 0                                           #init settings
i=0
col = 0

amb_val = 10                                        #change to set value for when a line is detected



# ------------------------main loop-----------------------------------
while i<30:
    m1.run(-180)                                    #set wheel speed
    m2.run(-180)

    col = cs.reflection()                              #Get sensor reading
    buf_array[buf_index]=col                        #Save reading
    buf_index = buf_index + 1                       #Increment index
    if buf_index == size:                           #make the index flip when end of buffer is reached 
        buf_index = 0

    avg_reading = sum(buf_array)/size               #find avg reading for sensor if the avg value is less than amb_val it means a line is detected

    #ev3.screen.clear()
    #ev3.screen.draw_text(50,60,state)   
  

    if avg_reading >= 45 and state == 1:            #Check if the line has been passed
        stopW.reset()                               #restet clock to 0
        state = 2                                   #change to state 2
        

    if avg_reading <= amb_val and state == 2:       #Check if line has been meet for a second time
        time = stopW.time()                         #Get time from clock
        data.log(i,time)                            #Log data info file
        i = i+1                                     #increment the run index number

        for x in range(size):                       #reset buf_array
            buf_array[x] = 100
        avg_reading = 100                       
        
        state = 0                                   #Change state to the begin new run
        ev3.screen.clear()
        ev3.screen.draw_text(50,60,"move me") 
        m1.stop()                                   #Stop the wheels
        m2.stop()
        wait(5000)                                  #Pause program so robot can be moved back to start
        ev3.screen.clear()
        ev3.screen.draw_text(50,60,i)
   

    if avg_reading <= amb_val and state == 0:                      #change state if black is detected
        #ev3.screen.clear()
       # ev3.screen.draw_text(50,60,"dog")
        state = 1

    
#----------------------------program end-------------------------------7
# program will end after 30 runs 
m1.stop()                                           #stop wheels
m2.stop()
ev3.speaker.beep()                                  #Single beep to mark end of test