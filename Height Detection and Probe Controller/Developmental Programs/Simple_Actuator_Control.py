'''
This code functions to test the Pololu G2 Motor Driver with the P16 Actuator

This program is an Open Loop System

Components:
    Raspberry Pi
    12V Battery Pack
    Pololu G2 24v13 Motor Driver
    Actuonix P16 200mm
'''

# Imports
import RPi.GPIO as GPIO
import time
import sys

# Constants
MAX_LENGTH = 196.75 # mm
mm2in = 25.4

# Pin and PWM Initialization
actuatorPin = 18 # GPIO 24 (Pin 18)

my_pwm = None

def init():
    global my_pwm
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(actuatorPin, GPIO.OUT)
    
    my_pwm = GPIO.PWM(actuatorPin, 1000) # PWM operates at 1 kHz
    my_pwm.start(0) # 0% Duty Cycle

# Imperial to Metric Conversion
def in2mm(distance):
    return distance * mm2in

# Calculate Duty Cycle
def calculateDutyCycle(distance):
    distMM = in2mm(distance)
    dc = distMM* 100 * 1023 # Distance/Max distance * 100%
    return dc

def pwmOutput():
    global my_pwm
    
    # 0 inches
    
    for i in range (0,101,1):
        #dc = calculateDutyCycle(i)
        print(i, "inches\n")
        my_pwm.ChangeDutyCycle(i)
        time.sleep(0.1) # Sleep for 10 seconds


init()
while True:
    pwmOutput()
    print("\nLoop Complete!\n\n")
    time.sleep(1)
