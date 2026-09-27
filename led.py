#Small - gnd 
#Big - pin 
#Ground pins : 6,9,14,25,20,30,39,34



import RPi.GPIO as GPIO
import time
numTimes = int(input("Enter total number of times to blink: "))
speed = float(input("Enter length of each blink (seconds): "))
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # Using physical pin numbers
GPIO.setup(11, GPIO.OUT) # LED1
GPIO.setup(13, GPIO.OUT) # LED2
GPIO.setup(15, GPIO.OUT) # LED3
GPIO.setup(16, GPIO.OUT) # LED4
def Blink(numTimes, speed):
    for i in range(numTimes):
        print("Iteration", i + 1)
        GPIO.output(11, True) # LED1 ON
        GPIO.output(13, True) # LED2 ON
        GPIO.output(15, True) # LED3 ON
        GPIO.output(16, True) # LED4 ON
        time.sleep(speed)
        GPIO.output(11, False) # LED1 OFF
        GPIO.output(13, False) # LED2 OFF
        GPIO.output(15, False) # LED3 OFF
        GPIO.output(16, False) # LED4 OFF
        time.sleep(speed)
Blink(numTimes, speed)
GPIO.cleanup()

