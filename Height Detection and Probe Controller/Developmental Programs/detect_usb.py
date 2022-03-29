#import os
import subprocess

def getUUID_from_path(filepath):
    # Command to get UUID
    cmd = "sudo blkid -o value $(\df --output=source " + filepath + "|tail -1)|head -1"
    
    # Get output from command
    x = subprocess.Popen(cmd,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr = subprocess.PIPE).communicate()[0]
    
    # Decode output from bytes to a string
    x = repr(x.decode('utf-8'))
    
    # Return ID while removing ', \n, and ' from decoded string
    return x.split("\\n")[0][1:]
 
ID = getUUID_from_path('/dev/sda1')
print(ID)