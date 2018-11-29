
import serial


ser = serial.Serial( port='/dev/ttyUSB0', baudrate = 9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)


ser.write(chr(0xAA).encode())
