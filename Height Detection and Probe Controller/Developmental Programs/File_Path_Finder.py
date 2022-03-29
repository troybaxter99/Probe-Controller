import subprocess

def getPath(filepath):
    # Command to get path to USB Drive
    cmd = "df -h " + filepath + " | awk '{print $6}'"
    
    # Get output from command
    x = subprocess.Popen(cmd,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr = subprocess.PIPE).communicate()[0]
    
    # Decode output from bytes to a string
    x = repr(x.decode('utf-8'))
    
    # Return path to external drive
    return x.split("\\n")[1]
 
try:
    ID = getUUID_from_path('/dev/sda1')
    print(ID)
except:
    print("No USB")
