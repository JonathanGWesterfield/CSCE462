import serial
#This function gives values (that the NU understands)  to the NOTES
#This can be interchangable to the scale of notes preferred by the user
#Needs to match the json files
def indexing(N):
    if N == 'B4':
        return 0b00000000000000000000000000000001
    elif N == 'C5':
        return 0b00000000000000000000000000000010
    elif N == 'G4':
        return 0b00000000000000000000000000000100
    elif N == 'G#4':
        return 0b00000000000000000000000000001000
    elif N == 'A4':
        return 0b00000000000000000000000000010000
    elif N == 'A#4':
        return 0b00000000000000000000000000100000
    elif N == 'F#4':
        return 0b00000000000000000000000001000000
    elif N == 'F4':
        return 0b00000000000000000000000010000000
    elif N == 'E4':
        return 0b00000000000000000000000100000000
    elif N == 'D#4':
        return 0b00000000000000000000001000000000
    elif N == 'D4':
        return 0b00000000000000000000010000000000
    elif N == 'C#4':
        return 0b00000000000000000000100000000000
    elif N == 'C4':
        return 0b00000000000000000001000000000000
    elif N == 'B3':
        return 0b00000000000000000010000000000000
    elif N == 'A#3':
        return 0b00000000000000000100000000000000
    elif N == 'A3':
        return 0b00000000000000001000000000000000
    elif N == 'A2':
        return 0b00000000000000010000000000000000
    elif N == 'A#2':
        return 0b00000000000000100000000000000000
    elif N == 'B2':
        return 0b00000000000001000000000000000000
    elif N == 'C3':
        return 0b00000000000010000000000000000000
    elif N == 'C#3':
        return 0b00000000000100000000000000000000
    elif N == 'D3':
        return 0b00000000001000000000000000000000
    elif N == 'D#3':
        return 0b00000000010000000000000000000000
    elif N == 'E3':
        return 0b00000000100000000000000000000000
    elif N == 'F3':
        return 0b00000001000000000000000000000000
    elif N == 'F#3':
        return 0b00000010000000000000000000000000
    elif N == 'G3':
        return 0b00000100000000000000000000000000
    elif N == 'G#3':
        return 0b00001000000000000000000000000000
    elif N == 'F2':
        return 0b00010000000000000000000000000000
    elif N == 'F#2':
        return 0b00100000000000000000000000000000
    elif N == 'G2':
        return 0b01000000000000000000000000000000
    elif N == 'G#2':
        return 0b10000000000000000000000000000000



def timerconv(S):  #Converts time into counter values understood by the NU32  (time in seconds)
    x= int((S / (12.5e-9 * 256)) - 1)
    if x < 0:
        return 0
    else:
        return x


#Sends data to microcontroller (NU32)
def senddata(notes,time):
    #Connection with NU32 through USB (/dev/ttyUSB0)
    #Baud rate MATCHES the receivers microcontroller baud rate  (OR IT WILL NOT WORK!!!)
    
    ser = serial.Serial('/dev/ttyUSB0', baudrate= 230400,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,rtscts=True)

    notesarr = notes
    timesarr = time
    #Needs to convert note/time values into bytes
    #Since you can only send 1 byte at a time and our data is in 4 bytes
    #Send 1 byte  at  a time AND receiver microcontroller needs to join data after every byte received
    
    for x in notesarr:
        #Takes 0x from Hex value from array
        hex_string = x[2:]
        #Populates the 32 bits with  0s if needed to be able to split them correctly
        while (len(hex_string) != 8):
            hex_string = '0' + hex_string
        #print(hex_string)
        #converts them into a string
        hex_string = str(hex_string)
        #string into byte
        hex_data = bytes.fromhex(hex_string)
        #print(hex_data)
        #FOLLOWING LINE SENDS THE DATA
        ser.write(hex_data)
#Following line is a flag that tells microncontroller notes data has been sent
    ser.write(b'\xFF\xFF\xFF\xFE')
    print('Notes array sent')
    #Following loop does like above but with time values
    for x in timesarr:
        hex_string = x[2:]
        while (len(hex_string) != 8):
            hex_string = '0' + hex_string
        #print(hex_string)
        hex_string = str(hex_string)
        hex_data = bytes.fromhex(hex_string)
        #print(hex_data)
        ser.write(hex_data)
#Following line is a flag that tells microncontroller time data has been sent
    ser.write(b'\xFF\xFF\xFF\xFF')
    print('Times array sent')
