import os
import subprocess
from time import sleep, strftime, time
from datetime import datetime

# path = r"/media/pi/89F7-D25A" # Path to external flash drive
extension = ".csv"
file_path = None

def getFilePath(devPath):
    # Command to get path to USB Drive
    cmd = "df -h " + devPath + " | awk '{print $6}'"
    
    # Get output from command
    x = subprocess.Popen(cmd,
                         shell = True,
                         stdout = subprocess.PIPE,
                         stderr = subprocess.PIPE).communicate()[0]
    
    # Decode output from bytes to a string
    x = repr(x.decode('utf-8'))
    
    # Return path to external drive
    return x.split("\\n")[1]

def pathExist():
    # Return 1 if USB is plugged
    try:
        getFilePath("/dev/sda1")
        return 1
    
    # Return 0 if USB is not plugged in
    except:
        return 0

def createFile(path):
    # Get current year, month, day, hour, and minute
    now = datetime.now()
    time = now.strftime("%Y%m%d-%H%M")

    # Create File Name
    file_name = "probe-height-telemetry-"+time+extension
    global file_path
    file_path = os.path.join(path, file_name)

    # Check to see if file doesn't exist
    # If File Doesn't Exists
    if (not os.path.exists(file_path)): 
        with open(file_path, 'x') as log:
            log.write("Time(HR:MM:SS), Time of Flight Sensor Distance (in), Probe Distance (in), Expected Actuator Length (in), Actual Actuator Length (in)\n")        
        log.close()

def logData(tof_dist, probe_dist, expected_actuator_len, actual_actuator_len):
    global file_path
    with open(file_path, 'a') as log:
        log.write("{0}, {1}, {2}, {3}, {4}\n".format(strftime("%H:%M:%S"), str(tof_dist), str(probe_dist), str(expected_actuator_len), str(actual_actuator_len)))
        log.close()

def ejectUSB():
    cmd = "sudo eject /dev/sda1"
    os.system(cmd)


'''
try:
    path = getFilePath("/dev/sda1")
    createFile(path)
    logData(12, 9, 6)
    print("Data Sent")
    ejectUSB()
except:
    print("No USB!")
'''