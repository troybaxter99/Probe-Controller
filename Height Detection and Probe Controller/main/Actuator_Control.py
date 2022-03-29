# Imports
import board
import pwmio
import time
# import tech_input as tech

#sys.path.insert(1, "/home/pi/Height Detection and Probe Controller")

# Set Known Constants
CASE_LENGTH = 5 #in
IDEAL_PROBE_DISTANCE = 9 #in
EXPOSED_PROBE_LENGTH = 4.5 #in

INITIAL_ACTUATOR_LENGTH = 3 #in
MAX_LENGTH = 196.75 # mm

mm2in = 25.4

PWM_FREQ = 65535

actuatorPWM = None

def init_act():
    global actuatorPWM
    
    # Setup Linear
    actuatorPWM = pwmio.PWMOut(board.D24, frequency = 1000, duty_cycle = 0) # Actuator PWM (Pin 18)
    
    actuatorPWM.duty_cycle = 0 # 0 inches

# Imperial to Metric Conversion
def in2mm(distance):
    return distance * mm2in

# Get Actuator Length
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

def main():
    init()
    while True:
        tech.extraction_Status()
        tech.led_Status()
        pwmOutput()
        time.sleep(0.1)
