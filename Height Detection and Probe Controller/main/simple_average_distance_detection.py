# Imports
import board
import busio
import digitalio
import sys
import time
import tech_input as tech

# Import VL53L0X
sys.path.insert(1, "/usr/local/lib/python3.9/dist-packages")
import adafruit_vl53l0x

# Initialize Sensor
sensor = None

# Initialize ToF
def init_dist():
    global sensor
    
    tofExists = False
    
    # Set pin 7 to Digital High
    xshut = digitalio.DigitalInOut(board.D4) # [XSHUT] (Pin 7)
    xshut.direction = digitalio.Direction.OUTPUT
    xshut.value = True
    
    # Create I2C and Sensor
    while (tofExists == False):
    # Check to see if Distance Sensor is installed properly
        try:
            # Setup Distance Sensor
            i2c = busio.I2C(board.SCL, board.SDA)
            sensor = adafruit_vl53l0x.VL53L0X(i2c)
            
            # If No Error, Set tofExists to True
            tofExists = True
        
        # If Error exists, Flash All LEDs
        except:
            # Send Error to LEDs
            error()
        
    # Set Timing Budget
    sensor.measurement_timing_budget = 200000 # 200 ms
    
def measure():
    global sensor
    
    dist = sensor.distance
    # print("Reading: {0} cm".format(dist))
    
    # Return distance in cm
    return dist

def average_distance(): #Average 3 to 5 distances
    measurementsPerAvg = 5 # Number of measurements before taking an average
    averageDist = 0
    
    # Loop measurementsPerAvg amount of times 
    for i in range(0, measurementsPerAvg, 1):
        averageDist += measure()
    
    averageDist = averageDist/measurementsPerAvg
    
    # Return average distance in cm
    return averageDist

def cm2in(dist):
    return dist/2.54 # 1 in = 2.54 cm

# Calibrated Equation based on most recent test
def calibration(dist):
    offset = -0.0093 * dist**2 + 0.2093 * dist + 0.0523 # Calculates Offset in inches
    # print("Offset: {0} in".format(offset))
    
    calibrated = dist - offset
    
    return calibrated

# Calibration based on Tested Average Offset Equation
def calibration_avg(dist):
    offset = -0.0071 * dist**2 + 0.1914 * dist - 0.9006 # Calculates Offset in inches
    # print("Average Offset Equation: {0} in".format(offset))
    
    calibrated = dist - offset
    
    return calibrated

def error():
    # print("No ToF Sensor Connection")
        
    # Turn on all LEDs
    tech.extractionLED.value = True
    tech.startLED.value = True
    tech.idleLED.value = True
    tech.stopLED.value = True
    
    time.sleep(0.2)
    
    # Turn off all LEDs
    tech.extractionLED.value = False
    tech.startLED.value = False
    tech.idleLED.value = False
    tech.stopLED.value = False
    
    time.sleep(0.2)

def main():
    rawAverage = average_distance()
    rawAverage_in = cm2in(rawAverage)
    distance_in = calibration(rawAverage_in)
    avg_cal_in = calibration_avg(rawAverage_in)

    print("\nRaw Average: {0} cm".format(rawAverage))
    print("Raw Average: {0} in".format(rawAverage_in))
    print("\nCalibrated Range Average: {0} in".format(distance_in))
    print("Avg. Calibrated: {0} in". format(avg_cal_in))

'''
if __name__ == "__main__":
    init_dist()
    main()
'''
