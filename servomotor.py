import serial
import time


def activatemotor():
    #this function id to activate the motors on the arduin
    arduino =  serial.Serial('/dev/ttyACM0',9600)
    arduino.write('q'.encode())#sends h to arduino
    print("seed")
    


for i in range(2):
    activatemotor()
    time.sleep(3)