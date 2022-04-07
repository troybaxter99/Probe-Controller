# Imports
import RPi.GPIO as GPIO
import time
import sys

sys.path.insert(1, "/home/pi/Height Detection and Probe Controller/actuonix-lac/actuonix_lac")
import lac

# Constants
MAX_LENGTH = 196.75 # mm
mm2in = 25.4

# Pin and PWM Initialization
actuatorPin = 18
button = 33

buttonStatus = False
buttonChange = False

GPIO.setmode(GPIO.BOARD)
GPIO.setup(button, GPIO.IN)
GPIO.setup(actuatorPin, GPIO.OUT)
    
my_pwm = GPIO.PWM(actuatorPin, 1000) # PWM operates at 1 kHz
my_pwm.start(0) # 0% Duty Cycle

p16 = lac.LAC()

# Imperial to Metric Conversion
def in2mm(distance):
    return distance * mm2in

# Calculate Duty Cycle
def calculateDutyCycle(distance):
    distMM = in2mm(distance)
    dc = distMM/MAX_LENGTH * 100 # Distance/Max distance * 100%
    return dc

def buttonPress():
    global buttonStatus
    global buttonChange
    
    if (GPIO.input(button) == 1):
        while(GPIO.input(button)):
            pass
        
        buttonStatus = not buttonStatus
        buttonChange = True
    
    else:
        buttonChange = False

def pwmOutput():
    if (buttonStatus == True & buttonChange == True):
        dc = calculateDutyCycle(5.0) # 5 inches
        print("Duty Cycle: %.3f%%" % dc)
        my_pwm.ChangeDutyCycle(dc)
        
    elif (buttonChange == True):
        dc = calculateDutyCycle(0) # 0 inches
        print("Duty Cycle: %.3f%%" % dc)
        my_pwm.ChangeDutyCycle(0)

def actuatorPos():
    if (buttonStatus == True & buttonChange == True):
        position = round(3 * mm2in * 1023/ 196.75) # 3 inches
        print("Position: %.3f%%" % position)
        p16.set_position(position)
        
    elif (buttonChange == True):
        position = 0 # 0 inches
        print("Position: %.3f" % position)
        p16.set_position(position)

while True:
    
    buttonPress()
    actuatorPos()
    time.sleep(0.1)

# my_pwm.ChangeDutyCycle(20)
# time.sleep(2)
# my_pwm.ChangeDutyCycle(80)
# time.sleep(2)
# my_pwm.ChangeDutyCycle(50)
# time.sleep(2)
# my_pwm.ChangeDutyCycle(0)