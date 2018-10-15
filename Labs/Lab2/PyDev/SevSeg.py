import RPi.GPIO as GPIO

"""This file is used to control a seven segment display"""

class SevSeg:

	def __init__(self):

	# The pins for each bar on the seven segment display
		self.gPinA = 13
		self.gPinB = 19
		self.gPinC = 18
		self.gPinD = 23
		self.gPinE = 24
		self.gPinF = 25
		self.gPinG = 12
		self.gPinH = 16

		# Setup which pins are which
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)

		GPIO.setup(self.gPinA, GPIO.OUT, initial=GPIO.LOW)
		GPIO.setup(self.gPinB, GPIO.OUT, initial=GPIO.LOW)
		GPIO.setup(self.gPinC, GPIO.OUT, initial=GPIO.LOW)
		GPIO.setup(self.gPinD, GPIO.OUT, initial=GPIO.LOW)
		GPIO.setup(self.gPinE, GPIO.OUT, initial=GPIO.LOW)
		GPIO.setup(self.gPinF, GPIO.OUT, initial=GPIO.LOW)
		GPIO.setup(self.gPinG, GPIO.OUT, initial=GPIO.LOW)
		GPIO.setup(self.gPinH, GPIO.OUT, initial=GPIO.LOW)		

	def pinA(self, turnOn=0):
		if turnOn:
			GPIO.output(self.gPinA, GPIO.HIGH)
		else:
			GPIO.output(self.gPinA, GPIO.LOW)

	def pinB(self, turnOn=0):
		if turnOn:
			GPIO.output(self.gPinB, GPIO.HIGH)
		else:
			GPIO.output(self.gPinB, GPIO.LOW)

	def pinC(self, turnOn=0):
		if turnOn:
			GPIO.output(self.gPinC, GPIO.HIGH)
		else:
			GPIO.output(self.gPinC, GPIO.LOW)

	def pinD(self, turnOn=0):
		if turnOn:
			GPIO.output(self.gPinD, GPIO.HIGH)
		else:
			GPIO.output(self.gPinD, GPIO.LOW)

	def pinE(self, turnOn=0):
		if turnOn:
			GPIO.output(self.gPinE, GPIO.HIGH)
		else:
			GPIO.output(self.gPinE, GPIO.LOW)

	def pinF(self, turnOn=0):
		if turnOn:
			GPIO.output(self.gPinF, GPIO.HIGH)
		else:
			GPIO.output(self.gPinF, GPIO.LOW)

	def pinG(self, turnOn=0):
		if turnOn:
			GPIO.output(self.gPinG, GPIO.HIGH)
		else:
			GPIO.output(self.gPinG, GPIO.LOW)

	def pinH(self, turnOn=0):
		if turnOn:
			GPIO.output(self.gPinH, GPIO.HIGH)
		else:
			GPIO.output(self.gPinH, GPIO.LOW)

	# Make the number 0
	def seg0(self):
		# 0 is: A, B, C, D, E, F
		self.pinA(1)
		self.pinB(1)
		self.pinC(1)
		self.pinD(1)
		self.pinE(1)
		self.pinF(1)
		self.pinG()
		self.pinH()

	def seg1(self):
		# 1 is: B, C
		self.pinA()
		self.pinB(1)
		self.pinC(1)
		self.pinD()
		self.pinE()
		self.pinF()
		self.pinG()
		self.pinH()

	def seg2(self):
		#2 is: A, B, D, E, G, H
		self.pinA(1)
		self.pinB(1)
		self.pinC()
		self.pinD(1)
		self.pinE(1)
		self.pinF()
		self.pinG(1)
		self.pinH(1)

	def seg3(self):
		#3 is: A, B, C, D, G, H
		self.pinA(1)
		self.pinB(1)
		self.pinC(1)
		self.pinD(1)
		self.pinE()
		self.pinF()
		self.pinG(1)
		self.pinH(1)

	def seg4(self):
		# 4 is: B, C, F, G, H
		self.pinA()
		self.pinB(1)
		self.pinC(1)
		self.pinD()
		self.pinE()
		self.pinF(1)
		self.pinG(1)
		self.pinH(1)

	def seg5(self):
		# 5 is: A, C, D, F, G, H
		self.pinA(1)
		self.pinB()
		self.pinC(1)
		self.pinD(1)
		self.pinE()
		self.pinF(1)
		self.pinG(1)
		self.pinH(1)

	def seg6(self):
		# 6 is: A, C, D, E, F, G, H
		self.pinA(1)
		self.pinB()
		self.pinC(1)
		self.pinD(1)
		self.pinE(1)
		self.pinF(1)
		self.pinG(1)
		self.pinH(1)

	def seg7(self):
		# 7 is: A, B, C
		self.pinA(1)
		self.pinB(1)
		self.pinC(1)
		self.pinD()
		self.pinE()
		self.pinF()
		self.pinG()
		self.pinH()

	def seg8(self):
		# 8 is: All of them
		self.pinA(1)
		self.pinB(1)
		self.pinC(1)
		self.pinD(1)
		self.pinE(1)
		self.pinF(1)
		self.pinG(1)
		self.pinH(1)

	def seg9(self):
		# 9 is: A, B, C, F, G, H
		self.pinA(1)
		self.pinB(1)
		self.pinC(1)
		self.pinD()
		self.pinE()
		self.pinF(1)
		self.pinG(1)
		self.pinH(1)




