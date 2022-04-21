import time
import sys

sys.path.insert(1, "/home/pi/Probe-Controller/Height Detection and Probe Controller/actuonix-lac/actuonix_lac")
import lac

p16 = lac.LAC()

# Disable Potentiometers
p16.disable_manual()

# Set proportional and derivative gains
derivativeGain = 10
proportionalGain = 50

p16.set_derivative_gain(derivativeGain)
p16.set_proportional_gain(proportionalGain)

# Test distance reading and accuracy
p16.set_position(3)
time.sleep(3)
print(3)
print(p16.get_feedback())
time.sleep(1)
p16.set_position(0)
time.sleep(3)
print(0)
print(p16.get_feedback())
