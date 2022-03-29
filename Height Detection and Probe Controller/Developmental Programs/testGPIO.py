import board
import digitalio
import pwmio
import time

extractionLED = digitalio.DigitalInOut(board.D17)
extractionLED.direction = digitalio.Direction.OUTPUT

pwmLED = pwmio.PWMOut(board.D24, frequency = 1000, duty_cycle = 0)

buttonRed = digitalio.DigitalInOut(board.D13)
buttonRed.direction = digitalio.Direction.INPUT

count = 0

while True:
    if (buttonRed.value):
        while buttonRed.value:
            pass
        extractionLED.value = not extractionLED.value
        
        count = count + 1
        
        if (count % 2 == 1):
            pwmLED.duty_cycle = 50762
            print(count)
        
        else:
            pwmLED.duty_cycle = 0
            print(count)
        

