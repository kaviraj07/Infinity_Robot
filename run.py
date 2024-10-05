# -*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time
import arm
import cv2
import pyrebase
import config

# Definition of  motor pins
IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26
ENA = 16
ENB = 13

# Definition of  button
key = 8

# TrackSensorLeftPin1 TrackSensorLeftPin2 TrackSensorRightPin1 TrackSensorRightPin2
#      3                 5                  4                   18
TrackSensorLeftPin1 = 3  # The first tracking infrared sensor pin on the left is connected to  BCM port 3 of Raspberry pi
TrackSensorLeftPin2 = 5  # The second tracking infrared sensor pin on the left is connected to  BCM port 5 of Raspberry pi
TrackSensorRightPin1 = 4  # The first tracking infrared sensor pin on the right is connected to  BCM port 4 of Raspberry pi
TrackSensorRightPin2 = 18  # The second tracking infrared sensor pin on the right is connected to  BCMport 18 of Raspberry pi

# Set the GPIO port to BCM encoding mode.
GPIO.setmode(GPIO.BCM)

# Ignore warning information
GPIO.setwarnings(False)

# Motor pins are initialized into output mode
# Key pin is initialized into input mode
# Track sensor module pins are initialized into input mode
def init():
    global pwm_ENA
    global pwm_ENB
    GPIO.setup(ENA, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(ENB, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(key, GPIO.IN)
    GPIO.setup(TrackSensorLeftPin1, GPIO.IN)
    GPIO.setup(TrackSensorLeftPin2, GPIO.IN)
    GPIO.setup(TrackSensorRightPin1, GPIO.IN)
    GPIO.setup(TrackSensorRightPin2, GPIO.IN)
    # Set the PWM pin and frequency is 2000hz
    pwm_ENA = GPIO.PWM(ENA, 2000)
    pwm_ENB = GPIO.PWM(ENB, 2000)
    pwm_ENA.start(0)
    print("start")
    pwm_ENB.start(0)


# advance
def run(leftspeed, rightspeed):
    ##this code runs straight on a black line
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)
    print("advance")


# back
def back(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    print("back")
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)


# turn left
def left(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(0)
    pwm_ENB.ChangeDutyCycle(rightspeed)
    print("left")


# turn right
def right(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(0)


# turn left in place
def spin_left(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    print("left in place")
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)


# turn right in place
def spin_right(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    print("right in place")
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)


# brake
def brake():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    print("brake")


# Button detection
def key_scan():
    while GPIO.input(key):
        pass
    while not GPIO.input(key):
        time.sleep(0.01)
        if not GPIO.input(key):
            time.sleep(0.01)
        while not GPIO.input(key):
            pass


# delay 2s
time.sleep(2)

move = 1
sTime = 0  # start time
cTime = 0  # current time


###################################
# Temporarily replace quote function
def noquote(s):
    return s

pyrebase.pyrebase.quote = noquote
###################################



# initialising pyrebase
firebase = pyrebase.initialize_app(config)

# initialising Database
db = firebase.database()

# Getting the values for planting
leng = []
width = []
keyval = []

plant = db.child("Plant").order_by_child("Completed").equal_to("False").get()

for i in plant.each():
    keyval.append(i.key())
    leng.append(i.val()["Length"])
    width.append(i.val()["Width"])

print(leng)
print(width)
print(keyval)

#######################################
counter = 0
rowCounter = 0

#check if there are values from firebase first, then compute number of rows for seeding
if len(leng) != 0:
    numRows = int(int(leng[counter]) / int(width[counter]))
    print("NUMBER OF ROWS FOR SEEDING : " + str(numRows))
else:
    numRows = 0


rightSp = 5
leftSp = 5
# The try/except statement is used to detect errors in the try block.
# the except statement catches the exception information and processes it.
try:
    init()
    key_scan()
    sTime = time.time()
    
    #while True:
    
    # If no rows to seed, rover will neither move nor seed
    while (numRows !=0):
        
        # Check if all rows completed and if no seeding(no rows) need to be performed
        if rowCounter >= numRows and numRows !=0:
            db.child("Plant").child(keyval[counter]).update({"Completed":"True"})
            move = 1
            #####################
            # Capture photo and save it to the folder using opencv

            cap = cv2.VideoCapture(0)

            while True:
                ret, frame = cap.read()
                if not ret:
                    continue
                if numRows != 0:
                    name = keyval[counter] + ".jpg"
                else:
                    name = "Empty.jpg"
                cv2.imwrite(name, frame)
                break
            cap.release()
            cv2.destroyAllWindows()
                
            #########################
            # Upload photo in Firebase Storage
            storage = firebase.storage()
            storage.child("myimg/" + name).put(name)

            ############################
            
            if len(leng) > counter + 1:
            
                print("Condition Satisfied ###############")
                counter = counter + 1
                rowCounter = 0
                numRows = int(int(leng[counter]) / int(width[counter]))
            sTime = time.time()

        # When the black line is detected, the corresponding indicator of the tracking module is on, and the port level is LOW.
        # When the black line is not detected, the corresponding indicator of the tracking module is off, and the port level is HIGH.
        TrackSensorLeftValue1 = GPIO.input(TrackSensorLeftPin1)
        TrackSensorLeftValue2 = GPIO.input(TrackSensorLeftPin2)
        TrackSensorRightValue1 = GPIO.input(TrackSensorRightPin1)
        TrackSensorRightValue2 = GPIO.input(TrackSensorRightPin2)

        if move == 1:
            
            # 4 tracking pins level status
            # 0 0 X 0
            # 1 0 X 0
            # 0 1 X 0
            # Turn right in place,speed is 50,delay 80ms
            # Handle right acute angle and right right angle
            if (TrackSensorLeftValue1 == False or TrackSensorLeftValue2 == False) and (
                TrackSensorRightValue2 == False
            ):
                # spin_right(leftSp, rightSp)
                brake()
                #numRows = 0
                print("spin right")

                time.sleep(2)

            # 4 tracking pins level status
            # 0 X 0 0
            # 0 X 0 1
            # 0 X 1 0
            # Turn right in place,speed is 50,delay 80ms
            # Handle left acute angle and left right angle
            elif TrackSensorLeftValue1 == False and (
                TrackSensorRightValue1 == False or TrackSensorRightValue2 == False
            ):
                # spin_left(leftSp, rightSp)
                brake()
                #numRows = 0
                print("spin left")

                time.sleep(2)

            # 0 X X X
            # Left_sensor1 detected black line
            elif TrackSensorLeftValue1 == False:
                # spin_left(leftSp, rightSp)
                brake()
                #numRows = 0
                print("spinleft")

            # X X X 0
            # Right_sensor2 detected black line
            elif TrackSensorRightValue2 == False:
                # spin_right(leftSp, rightSp)
                brake()
                #numRows = 0
                print("spinright")

            # 4 tracking pins level status
            # X 0 1 X
            elif TrackSensorLeftValue2 == False and TrackSensorRightValue1 == True:
                left(leftSp, rightSp)
                print("left")

            # 4 tracking pins level status
            # X 1 0 X
            elif TrackSensorLeftValue2 == True and TrackSensorRightValue1 == False:
                right(leftSp, rightSp)
                print("right")

            # 4 tracking pins level status
            # X 0 0 X
            elif TrackSensorLeftValue2 == False and TrackSensorRightValue1 == False:
                # run(leftSp, rightSp)
                print("line detected")
                run(leftSp, rightSp)

            elif (
                TrackSensorLeftValue1 == True
                and TrackSensorLeftValue2 == True
                and TrackSensorRightValue1 == True
                and TrackSensorRightValue2 == True
            ):
                brake()
                #numRows = 0
                print("Brake Called")

                ###here cv

            cTime = time.time()
            if (cTime - sTime) >= 5:
                move = 0
                # sTime = 0
                sTime = time.time()

        elif move == 0:
            brake()
            # code for arm robot for one row
            # when completed , move will be set to one
            print("stopped for seeding")

            if rowCounter < numRows: 
                print("waiting for seeding")
                arm.default()
                arm.seeding()
                arm.resting()
                print("SEEDING")
                # Increment rowCounter after seeding one complete row
                rowCounter = rowCounter + 1
                numRows = 0

            # time.sleep(10)
            sTime = time.time()

            move = 1

        # When the level of 4 pins are 1 1 1 1 , the car keeps the previous running state.

except KeyboardInterrupt:
    pass
pwm_ENA.stop()
pwm_ENB.stop()
GPIO.cleanup()

