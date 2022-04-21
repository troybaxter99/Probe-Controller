import time
import sys

sys.path.insert(1, "/home/pi/Probe-Controller/Height Detection and Probe Controller/main")
sys.path.insert(2, "/home/pi/Audio-Alert-System/Code")

import tech_input as tech
import audio

sfx = audio.AUDIO("/home/pi/Audio-Alert-System/Audio-Files/Tech-Interface-Audio/")

#sfx.play_audio("oxp.wav")
print("Done")


def main():
    tech.init_tech()
    while True:
        tech.extraction_Status()
        tech.start_Status()
        tech.led_Status()
        time.sleep(0.1)
        
        posit = 0 # 0 inches
        if (tech.statusExtract == True):
            posit = 0 # 0 inches
        else:
            posit = 3 # 3 inches
        
        if (tech.extractionChange == True):
            print("position: %.2f in" % posit)
            sfx.play_audio("oxp.wav")

if __name__ == "__main__":
    main()