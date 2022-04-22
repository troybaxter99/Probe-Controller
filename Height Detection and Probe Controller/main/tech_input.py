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

'Global Variables'
# Button Status
statusExtract = True
extractionChange = False

statusStart = False
startChange = False

# USB Install Status
usbExists = False
debugMode = True
ejectionStatus = False

# Setup LEDs
extractionLED = digitalio.DigitalInOut(board.D23) # [Blue LED] (Pin 16)
startLED = digitalio.DigitalInOut(board.D22) # [Green LED] (Pin 15)
idleLED = digitalio.DigitalInOut(board.D27) # [Yellow LED] (Pin 13)
stopLED = digitalio.DigitalInOut(board.D17) # [Red LED] (Pin 11)
    
extractionLED.direction = digitalio.Direction.OUTPUT
startLED.direction = digitalio.Direction.OUTPUT
idleLED.direction = digitalio.Direction.OUTPUT
stopLED.direction = digitalio.Direction.OUTPUT
    
# Setup Buttons
extractionButton = digitalio.DigitalInOut(board.D13) # [Red Button] (Pin 33)
startButton = digitalio.DigitalInOut(board.D6) # [Yellow Button] (Pin 31)
    
extractionButton.direction = digitalio.Direction.INPUT
startButton.direction = digitalio.Direction.INPUT

# Instantiate techAudio as a global variable
global techAudio

# Initialization
def init_tech():
    global techAudio
    
    # Turn off start and idle LEDs. Turn on extraction and stop LEDs
    extractionLED.value = True
    startLED.value = False
    idleLED.value = False
    stopLED.value = True
    
    # Initialize techAudio and Setup Path to Audio File Location
    techAudio = audio.AUDIO("/home/pi/Audio-Alert-System/Audio-Files/Tech-Interface-Audio/")
    
# Extract/Install Probe Button
def extraction_Status():
    global statusExtract
    global extractionChange
    
    # Check to see if Probe is inactive
    if (statusStart == False):
        # Probe Extraction/Install Button Press
        if (extractionButton.value == 1):
        
            # Wait until button is no longer being pressed
            while (extractionButton.value):
                pass
        
            statusExtract = not statusExtract # Invert activation status
            extractionChange = True # change in activation status is true
            
            ''' Play Audio '''
            techAudio.set_volume(15) # Set Volume to 15%
            techAudio.play_audio("button_press.wav")
    
        else:
            extractionChange = False
        
    return [statusExtract, extractionChange]

def start_Status():
    global statusStart
    global startChange
    
    # Check to see if actuator has been activated
    if (statusExtract == False):
        
        '''
        Entering or Leaving Auto Mode
        '''
        # Check to see if start button has been pressed
        if (startButton.value == 1):
            
            # Check to see if button is still being pressed
            while(startButton.value):
                pass
            
            statusStart = not statusStart # invert statusStart
            startChange = True # True if there has been a change in start/stop status
            
            ''' Play Audio '''
            techAudio.set_volume(15) # Set Audio to 15%
            
            # Starting Up
            if (statusStart):
                techAudio.play_audio("button_press.wav")
                                
                time.sleep(0.1)
                techAudio.play_audio("startup.wav")
            
            # Shutting Down
            else:
                techAudio.play_audio("button_press.wav")
                                
                time.sleep(0.2)
                techAudio.play_audio("shutdown.wav")
                
        else:
            startChange = False
        
    return [statusStart, startChange]

def led_Status():
    global statusExtract
    global statusStart
    global usbExists
    global debugMode
    global ejectionStatus
    
    # Probe Extraction LED
    if (statusExtract == True & extractionChange == True):
        extractionLED.value = True
        #print("Probe Extraction Mode: Active")
        
        # Check to see if USB is plugged in
        if (telemetry.pathExist()):
            telemetry.ejectUSB()
            #print("Ejecting")
            
            # Flash LED 10 Times
            for i in range (0,20,1):
                extractionLED.value = not extractionLED.value # Toggle LED
                time.sleep(0.2) # 0.2 seconds
        
        
    elif (extractionChange == True):
        extractionLED.value = False
        #print("Probe Extraction Mode: Inactive")
    
    # Start LED Set
    if (statusStart == True & startChange == True):
        stopLED.value = False # Turn off Red LED
        idleLED.value = True # Turn on Yellow LED
        #print("STARTING")
        
        # Assume USB doesn't exist
        usbExists = False
        
        # Set debugMode to True
        debugMode = True
        
        while (usbExists == False and debugMode == True):
            
            # Check to see if USB Drive exists and create telemetry file if it does
            try:
                path = telemetry.getFilePath("/dev/sda1")
                telemetry.createFile(path) # Create Telemetry File
                #print("Creating Telemetry File")
                usbExists = True
                idleLED.value = True
        
            # Exception if no USB drive
            except:
                usbExists = False
                idleLED.value = not idleLED.value
            
            # Press Button to leave Debug Mode
            if (startButton.value):
                
                # Wait until button is no longer being pressed
                while(startButton.value):
                    pass
                
                ''' Audio '''
                techAudio.set_volume(100) # Set volume to 50%
                techAudio.play_audio("button_press.wav")
                
                # Set debugMode to false and turn on yellow LED
                debugMode = False
                idleLED.value = True
        
        # Delay 2 Seconds
        time.sleep(2)
        idleLED.value = False # Turn off Yellow LED
        startLED.value = True # Turn on Green LED
        
        #print("System Active")
    
    elif (startChange == True):
        startLED.value = False # Turn off Green LED
        stopLED.value = True # Turn on Red LED
        #print("System Inactive")


init_tech()


while True:
    extraction_Status()
    start_Status()
    led_Status()
    time.sleep (0.1)
    
    posit = 0 # 0 inches
    if (statusExtract == True):
        posit = 0 # 0 inches
    else:
        posit = 3 # 3 inches
        
    if (extractionChange == True):
        print("position:%.2f in" % posit)
