# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import matplotlib.pyplot as plt


# Software SPI configuration:
CLK  = 11
MISO = 9
MOSI = 10
CS   = 8
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

"""Each element is a tuple. Each tuple contains 2 elements:
    * The voltage value
    * The time (in microseconds) the value was taken at
"""
voltCoordinates = [] #not using this anymore 
voltX = [] 
voltY = [] 
periodTimeStamps = []

# Hardware SPI configuration:
# SPI_PORT   = 0
# SPI_DEVICE = 0
# mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


"""
print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('-' * 57)
# Main program loop.
while True:
    # Read all the ADC channel values in a list.
    chan0 = mcp.read_adc(0)
    # Print the ADC values.
    # print('| {0:>4} |'.format(*values))
    print("Channel 0:\t%d\n" % chan0)
    # Pause for half a second.
"""

startTime = time.time()
elapsedTime = 0.0

# The Oscilloscope will run for 5 seconds
while elapsedTime <= 0.1:
    # read from channel 0
    chan0 = mcp.read_adc(0)
    
    # find out the time stamp of the reading and the elapsed time
    elapsedTime = time.time() - startTime
    coordinate = (chan0, elapsedTime)
    voltX.append(chan0)
    voltY.append(elapsedTime)
    print("Coordinates: \t%d, %f" % (coordinate[0], coordinate[1]))
    voltCoordinates.append(coordinate)

    # Boolean flags used to determine if the peak voltage has been hit
    above900 = False
    hasHit = False
    
    # to calculate our freqemcy, get timestamp of every pos clk edge
    # and store all time stamps in a list. From there, find the average
    # times between each time stamp in the list. This is the average period
    # Frequency is 1/Period

    # check to see if we should make a change since it is below 900
    # 900 is usually the high end of the signal
    if above900 == False:
        if chan0 >= 900:
            above900 = True
            # get the time elapsed
            timeStamp = time.time()
            periodTimeStamps.append(timeStamp)
    else: # is above 900
        if chan0 <= 900:
            above900 = False

def calculateAvePeriod():
    periodTimes = []

    # populate list of period times
    for i in range(0, len(periodTimeStamps) - 2):
        periodTime = periodTimeStamps[i + 1] - periodTimeStamps[i]
        periodTimes.append(periodTime)
        # print("period Time: \t%d\n" % periodTime)
        # print("Period Time list length: \t%d\n" % len(periodTimes))

    # sum up and average the period times
    periodSum = 0.0
    for time in periodTimes:
        periodSum += time

    avePeriod = periodSum / len(periodTimes)
    
    return avePeriod

def calcFreq(avePeriod):
    aveFreq = 1 / avePeriod
    return aveFreq
        
"""Plot the coordinates we found and display our frequency"""
avePeriod = calculateAvePeriod()
frequency = calcFreq(avePeriod)
print("Average Frequency: \t%f\n" % frequency)

plt.plot(voltY, voltX, 'o-')
plt.title("Hella Oscillate")
plt.ylabel('Voltage Value')
plt.xlabel('time')

plt.show()
























