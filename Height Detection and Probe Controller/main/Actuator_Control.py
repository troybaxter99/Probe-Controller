# Imports
import board
import pwmio
import time
import math
import sys
import tech_input as tech

sys.path.insert(1, "/home/pi/Probe-Controller/Height Detection and Probe Controller/actuonix-lac/actuonix_lac")
import lac

# Set Known Constants
CASE_LENGTH = 5 #in
IDEAL_PROBE_DISTANCE = 9 #in
EXPOSED_PROBE_LENGTH = 4.5 #in
INITIAL_ACTUATOR_LENGTH = 3 #in
MAX_LENGTH = 196.75 # mm

mm2in = 25.4

PWM_FREQ = 65535

actuatorPWM = None

p16 = None 

'''
PWM Mode Functions
    These 3 functions are used if you want to connect the Raspberry Pi to the Actuonix LAC via RC Connection
    
    *** Check README.md for RC setup
        Repository: https://github.com/troybaxter99/Probe-Controller ***
'''
def setPWMmode():
    global actuatorPWM
    
    # Setup Linear Actuator Controller PWM Control
    actuatorPWM = pwmio.PWMOut(board.D24, frequency = 1000, duty_cycle = 0) # Actuator PWM (Pin 18)
    
    actuatorPWM.duty_cycle = 0 # 0 inches

# Calculate Duty Cycle
def calculateDutyCycle(distance):
    distMM = in2mm(distance)
    dc = int(distMM/MAX_LENGTH * PWM_FREQ) # Distance/Max distance * (2^16-1) to get PWM based on values between 0 and 65535 
    print (dc)
    return dc

def pwmOutput(distance):
    global my_pwm
    
    actuatorDist = getActuatorLength(distance)
        
    dc = calculateDutyCycle(actuatorDist)
    # print("Duty Cycle: %.3f%%\n" % (dc/65535 * 100))
    actuatorPWM.duty_cycle = dc
    
    '''
    if (tech.statusExtract == True & tech.extractionChange == True):
        dc = calculateDutyCycle(0) # 0 inches
        print("Duty Cycle: %.3f%%" % dc)
        print("Distance: 3 in\n")
        my_pwm.ChangeDutyCycle(dc)
        
    elif (tech.extractionChange == True):
        dc = calculateDutyCycle(3) # 3 inches
        print("Duty Cycle: %.3f%%" % dc)
        print("Distance: 0 in\n")
        my_pwm.ChangeDutyCycle(0)    
    '''
'''
USB Mode Functions
    These 4 functions are used if you want to connect your Raspberry Pi to the Actuonix LAC via USB Connection
    
    *** Check README.md for USB Setup
        Repository: https://github.com/troybaxter99/Probe-Controller ***
    
'''
# This functions instantates p16 as an LAC object
def setUSBmode():
    global p16
    p16 = lac.LAC()
    print("LAC setup")
    p16.set_position(0)

# This function allows for the user to change the LAC's derivative and proprotional gains
def changeLACGains(proprotional_gain, derivative_gain):
    global p16
    p16.disable_manual()
    p16.set_proportional_gain(proportional_gain)
    p16.set_derivative_gain(derivative_gain)

# This functions receives a distance in inches and sends the desired actuator position to the LAC
def setActuatorPosition(distance):
    global p16
    
    actuatorLength = getActuatorLength(distance) # Returns in inches
    actuatorLength = in2mm(actuatorLength) # Converts actuator length from inches to mm
    
    # Calculate value to be sent to the lac
    lacValue = (actuatorLength*1023)/MAX_LENGTH
    lacValue = round(lacValue)
    
    # Set actuator position
    p16.set_position(lacValue)

# This function returns the actual actuator position at the time it was called.
def getActualActuatorPosition():
    global p16
    distance = p16.get_feedback()
    return metric2in(distance)

'''
Direct Actuator Position Functions
    2 functions that eithe set the actuator to 0 inches or 3 inches depending upon whether the system is in:
        Install/Extraction Mode or Ready Mode
'''
# This function sets the actuaor to 0 inchesfor install/extraction
def setInstallPosition():
    global p16
    
    # Completely retracts the actuator
    p16.set_position(0)

def setReadyPosition():
    global p16
    
    actuatorLength = 3 # 3 inches
    actuatorLength = in2mm(actuatorLength)
    lacValue = (actuatorLength*1023)/MAX_LENGTH
    lacValue = round(lacValue)
    
    # Set actuator position
    p16.set_position(lacValue)
'''
Useful Functions for getting Actuator Length
'''
# Imperial to Metric Conversion
def in2mm(distance):
    return distance * mm2in

# Metric to Imperial Conversion
def metric2in(distance):
    return distance / mm2in

# Get Actuator Length in inches
def getActuatorLength(height):
    # Calculate Expected Actuator Length
    actuatorLen = height + ((CASE_LENGTH + INITIAL_ACTUATOR_LENGTH) - (EXPOSED_PROBE_LENGTH + IDEAL_PROBE_DISTANCE)) # A_e = d + ((C+I)-(e+L))
    
    # Dip in the ground exceeds actuator length
    if actuatorLen >= 5.5:
        actuatorLen = 5.5 #in
    
    # Obstacle or ground is closer to the probe than the actuator can handle
    elif actuatorLen <= 0.5:
        actuatorLen = 0.5 #in
    
    return actuatorLen

def getProbePosition(distance):
    A_a = getActuatorLength(distance) # Actual Actuator Length
    A_e = distance + ((CASE_LENGTH + INITIAL_ACTUATOR_LENGTH) - (EXPOSED_PROBE_LENGTH + IDEAL_PROBE_DISTANCE)) # Expected Actuator Length
    
    delta = A_a - A_e # Difference between actual and expected
    
    probe_pos = IDEAL_PROBE_DISTANCE - delta
    
    # Return Probe Position
    return probe_pos

'''
def main():
    new_tech.init_tech()
    while True:
        tech.extraction_Status()
        tech.led_Status()
        pwmOutput()
        time.sleep(0.1)
        
if __name__ == "__main__":
    main()
'''