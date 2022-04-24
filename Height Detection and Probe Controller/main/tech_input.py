# Imports
import board
import digitalio
import pwmio
import time

import telemetry_file as telemetry

# Import Audio
import sys
sys.path.insert(1, "/home/pi/Audio-Alert-System/Code")
import audio

'''
Outputs:
    Red LED
    Yellow LED
    Green LED
    Blue LED
'''
# Setup LEDs
extractionLED = digitalio.DigitalInOut(board.D23) # [Blue LED] (Pin 16)
startLED = digitalio.DigitalInOut(board.D22) # [Green LED] (Pin 15)
idleLED = digitalio.DigitalInOut(board.D27) # [Yellow LED] (Pin 13)
stopLED = digitalio.DigitalInOut(board.D17) # [Red LED] (Pin 11)
    
extractionLED.direction = digitalio.Direction.OUTPUT
startLED.direction = digitalio.Direction.OUTPUT
idleLED.direction = digitalio.Direction.OUTPUT
stopLED.direction = digitalio.Direction.OUTPUT

'''
INPUTS:
    Red Button (Extraction/Install Button)
    Yellow Button (Auto Mode Button)
'''
# Setup Buttons
extractionButton = digitalio.DigitalInOut(board.D13) # [Red Button] (Pin 33)
autoButton = digitalio.DigitalInOut(board.D6) # [Yellow Button] (Pin 31)
    
extractionButton.direction = digitalio.Direction.INPUT
autoButton.direction = digitalio.Direction.INPUT

'''
STATES: (rLED, yLED, gLED, bLED)
    Install/Extraction (1001)
    Ready (1000)
    Idle (0100)
    No USB (0T00), T: Toggle
    Start (0010)
'''


# Instantiate techAudio as a global variable
global sound
global currentState
global usbExists

# Initialization
def init_tech():
    global sound
    global currentState
    global usbExists
    
    # Initialize Current Status as Install
    currentState = "Install"
    # Set LEDs for Install Mode
    set_LED(currentState)
    # Initialize techAudio and Setup Path to Audio File Location
    sound = audio.AUDIO("/home/pi/Audio-Alert-System/Audio-Files/Tech-Interface-Audio/")
    # Set usbExists to false
    usbExists = False
    
# Button Press Function to check button presses
# Returns array with button press indicators [yellow button, red button]
def button_press():
    yellowPress = False
    redPress = False
    
    # Check to see if Red Button has been pressed
    if(extractionButton.value):
        # Wait until button is no longer being pressed
        while(extractionButton.value):
            pass
        # Change redPress to True
        redPress = True
    
    # If Red Button has not been pressed; Check to see if Yellow Button has been pressed
    elif(autoButton.value):
        # Wait until button is no longer being pressed
        while(autoButton.value):
            pass
        # Change yellowPress to True
        yellowPress = True
        
    return [yellowPress, redPress]


# This function serves to set and return the state given a button press
def set_state(buttons):
    global currentState
    global usbExists
    
    # Check Install State
    if (currentState == "Install"):
        # If extractionButton (Red Button) is pressed, enter Ready State
        if(buttons[1] == True and buttons[0] == False):
            currentState = "Ready"
            set_LED(currentState)
            print(currentState)
            sound.set_volume(25) # Set Volume to 25%
            sound.play_audio("button_press.wav")
    
    # Check Ready State
    elif (currentState == "Ready"):
        # If extractionButton (Red Button) is pressed, enter Install/Extraction State
        if(buttons[1] == True and buttons[0] == False):
            currentState  = "Install"
            set_LED(currentState)
            print(currentState)
            sound.set_volume(25) # Set Volume to 25%
            sound.play_audio("button_press.wav")
            
            # Eject USB if USB has been written to
            if (usbExists):
                # Set usbExists to False
                usbExists = False
                
                # Check to see if USB is plugged in
                if (telemetry.pathExist()):
                    telemetry.ejectUSB()
                    #print("Ejecting")
                    
                    # Flash LED 10 Times
                    for i in range (0,20,1):
                        extractionLED.value = not extractionLED.value # Toggle LED
                        time.sleep(0.2) # 0.2 seconds
        
        # If autoButton (Yellow Button) is pressed, enter Idle State
        if(buttons[1] == False and buttons[0] == True):
            currentState = "Idle"
            set_LED(currentState)
            print(currentState)
            sound.set_volume(25) # Set Volume to 25%
            sound.play_audio("button_press.wav")
    
    # Check Idle State
    elif(currentState == "Idle"):
        time.sleep(1) # Sleep for 1 second in Idle Mode
        # Check to see if USB exists; If it does, enter Auto State. If it doesn't enter No USB State
        try:
            path = telemetry.getFilePath("/dev/sda1")
            telemetry.createFile(path) # Create Telemetry File
            currentState =  "Auto"
            usbExists = True
            sound.set_volume(40) # Set Volume to 40%
            sound.play_audio("startup.wav")
        
        # If USB is no detected
        except:
            currentState = "No USB"
            
        set_LED(currentState)
        print(currentState)
    
    # Check No USB State
    elif(currentState == "No USB"):
        # Check to see if USB exists; If it does, enter Auto State. If it doesn't remain in USB State
        try:
            path = telemetry.getFilePath("/dev/sda1")
            telemetry.createFile(path) # Create Telemetry File
            currentState =  "Auto"
            usbExists = True
        except:
            currentState = "No USB"
        # Check to see if autoButton has been pressed to bypass the USB criteria
        if(buttons[1] == False and buttons[0] == True):
            currentState = "Auto"
            print(currentState)
            sound.set_volume(25) # Set Volume to 25%
            sound.play_audio("button_press.wav")
            
        # If current state has been changed from no USB to Auto, play startup audio
        if(currentState == "Auto"):
            sound.set_volume(40) # Set volume to 40%
            sound.play_audio("startup.wav")
        
        set_LED(currentState)
    
    # Check Auto State
    elif(currentState == "Auto"):
        # Check to see if autoButton has been pressed in order to leave Auto State and enter Ready State
        if(buttons[1] == False and buttons[0] == True):
            currentState = "Ready"
            set_LED(currentState)
            print(currentState)
            sound.set_volume(25) # Set Volume to 25%
            sound.play_audio("button_press.wav")
            sound.set_volume(40) # Set Volume to 40%
            sound.play_audio("shutdown.wav")
            
    # Return currentState
    return currentState
        
        

def set_LED(state):
    if(state == "Install"):
        stopLED.value = True # Red LED
        idleLED.value  = False # Yellow LED
        startLED.value = False # Green LED
        extractionLED.value = True # Blue LED
    
    elif(state == "Ready"):
        stopLED.value = True # Red LED
        idleLED.value  = False # Yellow LED
        startLED.value = False # Green LED
        extractionLED.value = False # Blue LED    
        
    elif(state == "Idle"):
        stopLED.value = False # Red LED
        idleLED.value  = True # Yellow LED
        startLED.value = False # Green LED
        extractionLED.value = False # Blue LED
        
    elif(state == "No USB"):
        stopLED.value = False # Red LED
        idleLED.value  = not idleLED.value # Yellow LED (toggle)
        startLED.value = False # Green LED
        extractionLED.value = False # Blue LED
    
    elif(state == "Auto"):
        stopLED.value = False # Red LED
        idleLED.value  = False # Yellow LED
        startLED.value = True # Green LED
        extractionLED.value = False # Blue LED
        

def main():
    state = button_press()
    set_state(state)
    time.sleep(0.1)

'''
if __name__ == "__main__":
    init_tech()
    while True:
        main()
'''
