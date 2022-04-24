# Imports
import simple_average_distance_detection as hd
import Actuator_Control as p16
import tech_input as tech
import telemetry_file as telemetry


def main():
    # Initialization
    hd.init_dist()
    tech.init_tech()
    p16.setUSBmode()
    
    # Set actuator position to 0 inches
    p16.setInstallPosition()
    
    extraction = [None] * 2
    start = [None] * 2
    
    state = "Install"
    
    # Check Mode
    while True:
        inputs = tech.button_press()
        previousState = state
        state = tech.set_state(inputs)
        
        # Auto Mode
        if(state == "Auto"):
#             if(start[1] == True):
#                 print("Entering Distance Detection Mode")
            
            errorPass = False
            while (errorPass == False):
                try:
                    # Get Distance Measurement
                    distancecm = hd.average_distance()
                    distance = hd.cm2in(distancecm)
                    distCal = hd.calibration_avg(distance) # Calibrated Distance (in)
                    errorPass = True # Passes Error Check
                    
                    # Turn on Green LED in case it turned off from Error Check
                    tech.startLED.value = True
                    
                except:
                    hd.error()
             
            #print("Distance: %.2f in" % distCal)
            lacErrorPass = False
            
            # Try to set Actuator Position.
            #     If actuator position cannot be set due to LAC getting disconnected,
            #     whether inadvertently by the system or due to the battery dying,
            #     reinitialize LAC.
            #     Otherwise, set Actuator Position appropriately
            while (lacErrorPass == False):
                try:
                    p16.setActuatorPosition(distCal)
                    lacErrorPass = True
                except:
                    p16.lacError()
                    
            
            if (tech.usbExists == True):
                # Add Data to Telemetry
                probe_pos = p16.getProbePosition(distCal)
                expected_actuator_len = p16.getActuatorLength(distCal)
                actual_actuator_len = p16.getActualActuatorPosition()
                
                # Send calibrated distance measurement, probe position, expected actuator length,
                # and actual actuator length to a .csv telemetry file
                telemetry.logData(distCal, probe_pos, expected_actuator_len, actual_actuator_len)
        
        # Extraction Mode
        if(state == "Install" and (previousState != state)): # If change in extraction mode condition
            lacErrorPass = False
            while(lacErrorPass == False):
                try:
                    p16.setInstallPosition() # 0 inches
                    #print("Distance: 0 in")
                    lacErrorPass = True
                except:
                    p16.lacError()
                
        elif(state == "Ready" and (previousState != state)): # If Extraction Mode is not enabled
            lacErrorPass = False
            while(lacErrorPass == False):
                try:
                    p16.setReadyPosition() # 3 inches
                    #print("Distance: 3 in")
                    lacErrorPass = True
                except:
                    p16.lacError()
            
    '''
    # Get Height Detection
    measure = hd.average_distance() # Measured in centimeters
    imperial = hd.cm2in(measure)
    height = hd.calibration(imperial)
    print("Distance: %.2f" % height)
    '''
    
if __name__ == "__main__":
    main()

