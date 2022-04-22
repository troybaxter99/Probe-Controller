# Imports
import board
import busio
import sys
import time

# Import VL53L0X
sys.path.insert(1, "/usr/local/lib/python3.9/dist-packages")
import adafruit_vl53l0x


i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl53l0x.VL53L0X(i2c)

# Set Timing Budget
sensor.measurement_timing_budget = 200000 # 200 ms

def average_distance(): #Average 3 to 5 distances
    dist1 = sensor.distance
    dist2 = sensor.distance
    dist3 = sensor.distance
    dist4 = sensor.distance
    dist5 = sensor.distance
    
    averageDist = (dist1 + dist2 + dist3 + dist4 + dist5)/5
    
    return averageDist

def cm2in(dist):
    return dist/2.54 # 1 in = 2.54 cm

def in2cm(dist):
    return dist*2.54 # 1 in = 2.54 cm

def calibration(dist):
    #offset = -0.0198 * dist**2 + 0.4127 * dist - 0.8486 # O = -0.0198*dm^2 + 0.4127*dm - 0.8486
    #offset = 0.0004 * dist**3 - 0.0208 * dist**2 + 0.3076 * dist - 0.3542
        #offset = -0.0055 * dist**2 + 0.125 * dist + 0.4277
    offset = -0.0093 * dist**2 + 0.2093 * dist + 0.0523
    print("Offset: {0} in".format(offset))
    
    calibrated = dist - offset
    
    return calibrated

# Calibration based on Tested Average Offset Equation
def calibration_avg(dist):
    offset = -0.0099 * dist**2 + 0.2182 * dist - 0.0171
    print("Average Offset Equation: {0} in".format(offset))
    
    calibrated = dist - offset
    
    return calibrated


while True:
    rawAverage = average_distance()
    rawAverage_in = cm2in(rawAverage)
    distance_in = calibration(rawAverage_in)
    distance_cm = in2cm(distance_in)
    
    cal_avg_in = calibration_avg(rawAverage_in)
    cal_avg_cm = in2cm(cal_avg_in)
    
    print("\nRaw Avereage: %.2f in (%.2f cm)" % (rawAverage_in, rawAverage))
    print("Calibrated: %.2f in (%.2f cm)" % (distance_in, distance_cm))
    print("Avg. Calibration: %.2f in (%.2f cm)" % (cal_avg_in, cal_avg_cm))