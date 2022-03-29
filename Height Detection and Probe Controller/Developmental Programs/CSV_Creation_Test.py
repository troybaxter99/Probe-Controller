import os
from time import sleep, strftime, time
from datetime import datetime

path = r"/media/pi/89F7-D25A" # Path to external flash drive
extension = ".csv"

# Get current year, month, day, hour, and minute
now = datetime.now()
time = now.strftime("%Y%m%d-%H%M")

# Create File Name
file_name = "test-"+time+extension
file_path = os.path.join(path, file_name)

# Check to see if a file already exists

# If File Doesn't Exists
if (not os.path.exists(file_path)): 
    with open(file_path, 'x') as log:
        log.write("Time(HR:MM:SS), Number, Odd/Even\n")
        print("Header Added")
        sleep(1) # Delay 1 Second
        log.close()

with open(file_path, 'a') as log:
    for i in range (0, 5, 1):
        oddEven = i%2
        log.write("{0}, {1}, {2}\n".format(strftime("%H:%M:%S"), str(i), str(oddEven)))
        print("Log", i)
        sleep(10) # Sleep 10 Seconds
    log.close()
