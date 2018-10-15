import RPi.GPIO as GPIO

"""
LED 1 (NOT CONNECTED TO THE SEVEN SEGMENT DISPLAY): 
	#4 - red
	#17 - green
	#27 - blue

LED 2 (CONNECTED TO THE SEVEN SEGMENT DISPLAY)
	#22 - red
	#5 - green
	#6 - blue
"""

def setupLEDs():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)

	#LED 1
	GPIO.setup(4, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW)
	
	# LED 2
	GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(5, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(6, GPIO.OUT, initial=GPIO.LOW)

# Make LED 1 red 
def LED1Red():
	GPIO.output(4, GPIO.HIGH)
	GPIO.output(17, GPIO.LOW)
	GPIO.output(27, GPIO.LOW)

# Make LED 1 blue
def LED1Blue():
	GPIO.output(4, GPIO.LOW)
	GPIO.output(17, GPIO.LOW)
	GPIO.output(27, GPIO.HIGH)

# Make LED 1 green
def LED1Green():
	GPIO.output(4, GPIO.LOW)
	GPIO.output(17, GPIO.HIGH)
	GPIO.output(27, GPIO.LOW)

# Turn off LED 1
def LED1Off():
	GPIO.output(4, GPIO.LOW)
	GPIO.output(17, GPIO.LOW)
	GPIO.output(27, GPIO.LOW)

# Make LED 2 red 
def LED2Red():
	GPIO.output(22, GPIO.HIGH)
	GPIO.output(5, GPIO.LOW)
	GPIO.output(6, GPIO.LOW)

# Make LED 2 blue
def LED2Blue():
	GPIO.output(22, GPIO.LOW)
	GPIO.output(5, GPIO.LOW)
	GPIO.output(6, GPIO.HIGH)

# Make LED 2 green
def LED2Green():
	GPIO.output(22, GPIO.LOW)
	GPIO.output(5, GPIO.HIGH)
	GPIO.output(6, GPIO.LOW)

# Turn off LED 2
def LED2Off():
	GPIO.output(22, GPIO.LOW)
	GPIO.output(5, GPIO.LOW)
	GPIO.output(6, GPIO.LOW)