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
    
    # Set actuator position to 0
    p16.setActuatorPosition(0)
    
    extraction = [None] * 2
    start = [None] * 2
    
    # Check Mode
    while True:
        extraction = tech.extraction_Status() # Checks extraction mode status and sets extraction[] = [statusExtraction, extractionChange]
        start = tech.start_Status() # Checks start mode status and sets start[] = [statusStart, startChange]
        tech.led_Status()
        
        # Start Mode
        if(start[0] == True):
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
            
            # Set distance for actuator
            if (distCal > 5.5):
                p16.setActuatorPosition(5.5)
            elif (distCal < 0.5):
                p16.setActuatorPosition(0.5)
            else:
                p16.setActuatorPosition(distCal)
            
            
            if (tech.usbExists == True):
                # Add Data to Telemetry
                probe_pos = p16.getProbePosition(distCal)
                expected_actuator_len = p16.getExpectedActuatorLength(distCal)
                actual_actuator_len = p16.getActualActuatorLength()
                
                # Send calibrated distance measurement, probe position, expected actuator length,
                # and actual actuator length to a .csv telemetry file
                telemetry.logData(distCal, probe_pos, expected_actuator_len, actual_actuator_len)
            
        # Extraction Mode
        if(extraction[1] == True): # If change in extraction mode condition
            if(extraction[0] == True): # If Extraction Mode is enabled
                p16.setActuatorPosition(0) # 0 inches
                #print("Distance: 0 in")
                
            else: # If Extraction Mode is not enabled
                p16.setActuatorPosition(3) # 3 inches
                #print("Distance: 3 in")
            
    '''
    # Get Height Detection
    measure = hd.average_distance() # Measured in centimeters
    imperial = hd.cm2in(measure)
    height = hd.calibration(imperial)
    print("Distance: %.2f" % height)
    '''
    
if __name__ == "__main__":
    main()
