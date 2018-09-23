import RPi.GPIO as GPIO
import LEDLibrary
from SevSeg import SevSeg
from time import sleep

# Pin 20 is the button pin

LEDLibrary.setupLEDs()
Segment = SevSeg()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN, pull_up_down = GPIO.PUD_UP)

while True:
    LEDLibrary.LED1Green()
    LEDLibrary.LED2Red()
    
    inputState = GPIO.input(20)
    if(inputState == False):
        print("Button Has Been Pressed!!!!")
        LEDLibrary.LED1Blue()
        sleep(0.5)
        LEDLibrary.LED1Off()
        LEDLibrary.LED2Red()
        sleep(0.5)
        LEDLibrary.LED1Blue()
        LEDLibrary.LED2Red()
        sleep(0.5)
        LEDLibrary.LED1Off()
        LEDLibrary.LED2Red()
        sleep(0.5)
        LEDLibrary.LED1Blue()
        LEDLibrary.LED2Red()
        sleep(0.5)
        LEDLibrary.LED1Off()
        LEDLibrary.LED2Red()
        sleep(1)
        LEDLibrary.LED2Green()
        LEDLibrary.LED1Red()
        Segment.seg9()
        sleep(1)
        Segment.seg8()
        sleep(1)
        Segment.seg7()
        sleep(1)
        Segment.seg6()
        sleep(1)
        Segment.seg5()
        sleep(1)
        Segment.seg4()
        LEDLibrary.LED2Blue()
        LEDLibrary.LED1Red()
        sleep(1)
        Segment.seg3()
        sleep(1)
        Segment.seg2()
        sleep(1)
        Segment.seg1()
        sleep(1)
        LEDLibrary.LED1Green()
        LEDLibrary.LED2Red()
        sleep(4)
        LEDLibrary.LED1Off()
        LEDLibrary.LED2Off()
        sleep(15)


    


    


