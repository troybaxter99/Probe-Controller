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

def single_distance():
    return sensor.distance

# Convert distance from cm to inches
def cm2in(dist):
    return dist/2.54 # 1 in = 2.54 cm

# Calibration in Inches (5-20 inches)
def calibration(dist):
    offset = -0.0198 * dist**2 + 0.4127 * dist - 0.8486 # O = -0.0198*dm^2 + 0.4127*dm - 0.8486
    print("Offset: {0} in".format(offset))
    
    calibrated = dist - offset
    
    return calibrated

# Measurements
raw = single_distance()
raw_in = cm2in(raw)
distance_in = calibration(raw_in)

print("Raw: {0} cm".format(raw))
print("Raw: {0} in".format(raw_in))
print("Calibrated: {0} in".format(distance_in))