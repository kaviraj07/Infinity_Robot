# -*- coding:UTF-8 -*-
import serial
from lib import al5_2D_IK, al5_moveMotors



# Create and open a serial port
sp = serial.Serial(
    "/dev/ttyUSB0", 9600
)  # First, open serial connection, you do it once, ONLY ONCE


# def move(sp, x, y, z, disarm=False, setDefaultPosition=False):
import time


def move(sp, x, y, z, g, wa, wr, disarm=False, setDefaultPosition=False):
    # move(sp, 2.0, 6.0, 70, 10, 45, 45, False, False)

    # Constants - Speed in µs/s, 4000 is roughly equal to 360°/s or 60 RPM
    #           - A lower speed will most likely be more useful in real use, such as 100 µs/s (~9°/s)

    CST_SPEED_MAX = 4000
    CST_SPEED_DEFAULT = 200

    # Set default values
    AL5_DefaultPos = 1500
    cont = True
    defaultTargetX = 4
    defaultTargetY = 4
    defaultTargetZ = 90
    defaultTargetG = 90
    defaultTargetWA = 0
    defaultTargetWR = 90

    defaultTargetShoulder = 90
    defaultTargetElbow = 90
    targetX = defaultTargetX
    targetY = defaultTargetY
    targetZ = defaultTargetZ
    targetG = defaultTargetG
    targetWA = defaultTargetWA
    targetWR = defaultTargetWR

    index_X = 0
    index_Y = 1
    index_Z = 2
    index_G = 3
    index_WA = 4
    index_WR = 5

    targetXYZGWAWR = (targetX, targetY, targetZ, targetG, targetWA, targetWR)
    targetQ = "y"
    motors_SEWBZWrG = (90, 90, 90, 90, 90, 90)
    speed_SEWBZWrG = (
        CST_SPEED_DEFAULT,
        CST_SPEED_DEFAULT,
        CST_SPEED_DEFAULT,
        CST_SPEED_DEFAULT,
        CST_SPEED_DEFAULT,
        CST_SPEED_DEFAULT,
    )

    # Get X position
    targetInput = x
    if targetInput == "":
        targetX = targetXYZGWAWR[index_X]
    else:
        targetX = float(targetInput)
    targetXYZGWAWR = (
        targetX,
        targetXYZGWAWR[1],
        targetXYZGWAWR[2],
        targetXYZGWAWR[3],
        targetXYZGWAWR[4],
        targetXYZGWAWR[5],
    )

    # Get Y position
    targetInput = y
    if targetInput == "":
        targetY = targetXYZGWAWR[index_Y]
    else:
        targetY = float(targetInput)
    targetXYZGWAWR = (
        targetXYZGWAWR[0],
        targetY,
        targetXYZGWAWR[2],
        targetXYZGWAWR[3],
        targetXYZGWAWR[4],
        targetXYZGWAWR[5],
    )

    # Get Z position
    targetInput = z
    if targetInput == "":
        targetZ = targetXYZGWAWR[index_Z]
    else:
        targetZ = float(targetInput)
    targetXYZGWAWR = (
        targetXYZGWAWR[0],
        targetXYZGWAWR[1],
        targetZ,
        targetXYZGWAWR[3],
        targetXYZGWAWR[4],
        targetXYZGWAWR[5],
    )

    # Get g position
    targetInput = g
    if targetInput == "":
        targetG = targetXYZGWAWR[index_G]
    else:
        targetG = float(targetInput)
    targetXYZGWAWR = (
        targetXYZGWAWR[0],
        targetXYZGWAWR[1],
        targetXYZGWAWR[2],
        targetG,
        targetXYZGWAWR[4],
        targetXYZGWAWR[5],
    )

    # Get wa position
    targetInput = wa
    if targetInput == "":
        targetWA = targetXYZGWAWR[index_WA]
    else:
        targetWA = float(targetInput)
    targetXYZGWAWR = (
        targetXYZGWAWR[0],
        targetXYZGWAWR[1],
        targetXYZGWAWR[2],
        targetXYZGWAWR[3],
        targetWA,
        targetXYZGWAWR[5],
    )

    # Get wa position
    targetInput = wr
    if targetInput == "":
        targetWR = targetXYZGWAWR[index_WR]
    else:
        targetWR = float(targetInput)
    targetXYZGWAWR = (
        targetXYZGWAWR[0],
        targetXYZGWAWR[1],
        targetXYZGWAWR[2],
        targetXYZGWAWR[3],
        targetXYZGWAWR[4],
        targetWR,
    )

    # Perform IK
    errorValue = al5_2D_IK(targetXYZGWAWR)
    if isinstance(errorValue, tuple):
        motors_SEWBZWrG = errorValue
    else:
        print(errorValue)
        motors_SEWBZWrG = (
            defaultTargetShoulder,
            defaultTargetElbow,
            defualtTargetWA,
            defaultTargetZ,
            defaultTargetG,
            defaultTargetWR,
        )

    # Move motors
    print("< Moving motors >")
    errorValue = al5_moveMotors(motors_SEWBZWrG, speed_SEWBZWrG, sp)
    print("< Done >")

    if setDefaultPosition:
        print("< Moving back to default position... >")
        for i in range(0, 6):
            sp.write(("#" + str(i) + " P" + str(AL5_DefaultPos) + "\r").encode())
        print("< Done >")

    if disarm:
        print("< Idling motors... >")
        for i in range(0, 6):
            sp.write(("#" + str(i) + " P" + str(0) + "\r").encode())
        print("< Done >")
    print("< operation Done >")


def default():
    # this is the default position
    move(sp, 3.0, 8.0, 90, 155, -70, 90, False, False)
    
def activatemotor():
    #this function id to activate the motors on the arduino
    arduino.write('q'.encode())#sends h to arduino
    print("seed")


# 1.0 in y move 2cm in real
def seeding():
    numofrows = 7
    numplants = 4
    xposition = 5.0
    yposition = 7.0
    for x in range(numplants):
        xposition = xposition + 1.5
        move(sp, xposition, yposition, 90, 155, -75, 90, False, False)  # close#lahuat
        yposition = 1.5
        time.sleep(2)
        move(sp, xposition, yposition, 90, 155, -75, 90, False, False)  # close#lahuat
        time.sleep(3)
        move(sp, xposition, yposition, 90, 155, -75, 90, False, False)  # close#lahuat
        time.sleep(3)
        arduino =  serial.Serial('/dev/ttyACM0',9600)
        
        #this function id to activate the motors on the arduino
        move(sp, xposition, yposition, 90, 90, -75, 90, False, False)  # close#lahuat
        time.sleep(4)
        #code to arduino
        #ser = serial.Serial('dev/
        #serial.write(("#10 P" +"1" + " S" + "1" + "\r").encode())
        #serial.write(("#10 p" + "1"))
        #Serial.begin(9600)
        #end arduino code
        yposition = 7.0
        move(sp, xposition, yposition, 90, 90, -75, 90, False, False)  # close#lahuat
        time.sleep(2)
        move(sp, xposition, yposition, 90, 155, -75, 90, False, False)  # close#lahuat
        time.sleep(2)
        arduino = 0
    default()
    # yposition = 7.0
    # time.sleep(2)
    # default()


# resting position on car
def resting():
    default()
    time.sleep(1)
    move(sp, 1.0, 8.0, 90, 155, -75, 90, False, False)


##functions for seeding
# default()
# seeding()
# resting()
#seeding()

