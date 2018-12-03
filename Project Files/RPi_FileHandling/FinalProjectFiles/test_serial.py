import json
import RPi.GPIO as GPIO
import array as arr
import sys
import glob
from time import sleep
import os
import time
import Adafruit_CharLCD as LCD
import indexNotes as indNotes
import threading
import serial
import os

# Raspberry Pi pin setup for LED Screen
lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 27
lcd_d6 = 18
lcd_d7 = 22
lcd_backlight = 2

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2

#Configures Adafruit LCD Screen
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

while os.system('ls /dev/ttyUSB0'):
    lcd.clear()
    lcd.message('Turn on NU32')
    print('Waiting for port')
    sleep(1)
    
#ser = serial.Serial('/dev/ttyS0', baudrate= 500,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,rtscts=False)
ser = serial.Serial('/dev/ttyUSB0', baudrate= 230400,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0.1,rtscts=True)

#Variables to control the extractation of the JSON files
global song
song = 0
notes_array = []
notes_time = []
files_arr = []
json_arr = []
count = 0
rep = 0

#Class to handle the switch debouncing 
class ButtonHandler(threading.Thread):
    def __init__(self, pin, func, edge='both', bouncetime=200):
        super().__init__(daemon=True)

        self.edge = edge
        self.func = func
        self.pin = pin
        self.bouncetime = float(bouncetime)/1000

        self.lastpinval = GPIO.input(self.pin)
        self.lock = threading.Lock()

    def __call__(self, *args):
        if not self.lock.acquire(blocking=False):
            return

        t = threading.Timer(self.bouncetime, self.read, args=args)
        t.start()

    def read(self, *args):
        pinval = GPIO.input(self.pin)

        if (
                ((pinval == 0 and self.lastpinval == 1) and
                 (self.edge in ['falling', 'both'])) or
                ((pinval == 1 and self.lastpinval == 0) and
                 (self.edge in ['rising', 'both']))
        ):
            self.func(*args)

        self.lastpinval = pinval
        self.lock.release()

#Function that controls play/pause key on board
#Song - index is the number of the song in the  list
def play(pin):
    global rep
    #Checks if it's playing or pause
    if ((song) < len(json_arr)) and (rep==1):
        ser.write(b'\xFF\xFF\xFF\xFD')
        print('Playing')
        rep =0
        onplay = getsong(song, count)
    elif ((song) < len(json_arr)) and (rep==0):
        print('Pause')
        ser.write(b'\xFF\xFF\xFF\xFD')
        rep = 1
        lcd.clear()
        lcd.message('Paused')

    else:
        lcd.clear()
        lcd.message('NO MORE SONGS')
        print("No more songs.")

#Function that sends the next dara
def next(pin):
    print('Next')
    #this  tells the  microcontroller that a  next song is  gonna be played
    ser.write(b'\xFF\xFF\xFF\xFC')

    
    global rep, song
    rep = 0
    #Send the next song in the list
    if((song + 1) < len(json_arr)): 
        print(song)
        song =  song + 1
        #on play get the time and notes array
        onplay = getsong(song,count)
        sleep(3)
        indNotes.senddata(onplay[0],onplay[1])
    else: #if reaches end of the list go back to the  beginning
        print(song)
        song = 0
        onplay = getsong(song,count)
        sleep(3)
        indNotes.senddata(onplay[0],onplay[1])

#Function that sends  the previous song data
def prev(pin):
    #Flag that indicates the previous song is going to play
    ser.write(b'\xFF\xFF\xFF\xFC')
    global rep, song
    rep = 0
    if(((song - 1) < len(json_arr)) and ((song-1) >= 0)):
        print(song)
        song =  song - 1
        onplay = getsong(song,count)
        sleep(3)
        indNotes.senddata(onplay[0],onplay[1])
    else:#if it goes back and reaches end of list, go to the last  song (Looping)
        print(song)
        song =  len(json_arr) - 1
        onplay = getsong(song,count)
        sleep(3)
        indNotes.senddata(onplay[0],onplay[1])

#NEW VARIABLES!!!
count = 0
notes_array=[]
notes_time = []
finalnotes_arr = []
newtime_arr = []
newnote = 0
matchingindex = []
lowestindex = 0
x = 0
#Path where all the jsons are at
#Path can change
nameofsong = ''
path = '/media/pi/SANDOVAL/Autospiel'
def getsong(songnum,count):
    count = 0
    print('Songnum')
    print(songnum)
    finalnotes_arr = []
    newtime_arr = []
    notes_time = []
    notes_array = []
    #This extracts information about the  json
    #Populates notes_time, and notes_array (Parallel arrays)
    with open(json_arr[songnum]) as data_file:
        data = json.load(data_file)
        for p in data['tracks']:
            for f in p['notes']:
                notes_time.append(f['time'])
                notes_array.append(f['name'])
                count = count + 1 #keeps count of number of notes
    #print(count)
    nameofsong= data['header']['name']
    lcd.clear()
    lcd.message(nameofsong)

    #FOR TESTING PURPOSES- tells which file you are on
    print("Playing: ")
    print(nameofsong)
    
    global x,lowestindex, newnote,matchingindex
#This while loops will tell you which  notes are being  played at the same time
#Needed to secure notes and time match
#THE MOST DIFFICULT PROCEDURE  IN THE PROGRAM!!!
    while (x != count):
    	while((x+1) < count) and  (notes_time[x] == notes_time[x+1]):  #checks all indexes
    		#print('match')
    		if x in matchingindex: #Checks if x/x+1 has been added:  you don't want repeating indexes
    			if (x+1 in matchingindex)  == False:
    				matchingindex.append(x + 1)
    		else:
    			matchingindex.append(x)
    			if (x+1 in matchingindex)  == False:
    				matchingindex.append(x + 1)
    		x = x+1	#increment x+1 for inner while loop, also for outside

    	if len(matchingindex) > 0: # Case that they are playing at same time
    		lowestindex = min(matchingindex)  # gets lowest index of  array to get time
    		for u in matchingindex: #this will OR the notes to get 32 bit
    			newnote = newnote | indNotes.indexing(notes_array[u])
    		newtime_arr.append(hex(indNotes.timerconv(notes_time[lowestindex])))
    		finalnotes_arr.append(hex(newnote))
    		newnote =  0 #resets new note after being added
    	else: #case that only one note  plays at same time
    		newtime_arr.append(hex(indNotes.timerconv(notes_time[x])))
    		newnote = newnote | indNotes.indexing(notes_array[x])
    		finalnotes_arr.append(hex(newnote))
    		newnote =  0
    	newnote =  0  #in case it did not change
    	#print (matchingindex)
    	matchingindex = [] #matching index array resets to start big while loop
    	x = x+1 #updates x in case only a  single note is played
        #print (notes_array)
    x=0
    count=0
    print(newtime_arr)
    print(len(newtime_arr))
    print(finalnotes_arr)
    print(len(finalnotes_arr))
    return finalnotes_arr, newtime_arr

def main():
    lcd.clear()
    sleep(2)
    #Get path
    #Create array of all files, and array of only json files
    dirs = os.listdir( path )
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(13, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(19, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(5, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)


    # Creates array of files
    for file in dirs:
        files_arr.append(file)

    # This would print all the files and directories for testing.
    #print("List of files:")
    #for f in files_arr:
    #    print (f)

    #This adds only json fil es to array (Need this for the actual playing"
    for g in files_arr:
        if g[-4:] == 'json':
            json_arr.append(g)
    print("List of jsons:")
    print(json_arr)

    #Plays first song
    onplay = getsong(song, count)
    indNotes.senddata(onplay[0],onplay[1])
    
    cb = ButtonHandler(13, play, edge='falling', bouncetime=100)
    cb.start()
    GPIO.add_event_detect(13, GPIO.FALLING, callback=cb)

    cx = ButtonHandler(19, next, edge='falling', bouncetime=100)
    cx.start()
    GPIO.add_event_detect(19, GPIO.FALLING, callback=cx)
    
    cv = ButtonHandler(5, prev, edge='falling', bouncetime=100)
    cv.start()
    GPIO.add_event_detect(5, GPIO.FALLING, callback=cv)

    while True:
        try:
            #When song ends playing, reads message from microcontroller telling it to play the next song
            x = ser.read()
            if x == b'\xff':
                next(19)
        except:
            pass

if __name__=="__main__":
    main()



