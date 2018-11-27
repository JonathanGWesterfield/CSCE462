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


# Raspberry Pi pin setup
lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 18
lcd_d7 = 22
lcd_backlight = 2

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

song = 0
notes_array = []
notes_time = []
files_arr = []
json_arr = []
count = 0
rep = 0

def play(pin):
    GPIO.output(26,True)
    GPIO.output(20,False)
    GPIO.output(21,False)
    global rep
    if ((song) < len(json_arr)) and (rep==0):
        onplay = getsong(song, count)
        rep =rep+1
    elif ((song) < len(json_arr)) and (rep==1):
        rep = 0
        onplay = ['']
        print('Pause')
        lcd.clear()
        lcd.message('PAUSE')
    else:
        lcd.clear()
        lcd.message('NO MORE SONGS')
        print("No more songs.")

def next(pin):
    GPIO.output(26,False)
    GPIO.output(20,True)
    GPIO.output(21,False)
    global song
    if(song + 1) < len(json_arr):
        song =  song + 1
        onplay = getsong(song,count)
    else:
        onplay = ['']
        print("No more songs.")
        lcd.clear()
        lcd.message('NO MORE SONGS')
def prev(pin):
    GPIO.output(26,False)
    GPIO.output(20,False)
    GPIO.output(21,True)
    global song
    if((song - 1) < len(json_arr)) and ((song-1) >= 0):
        song =  song - 1
        onplay = getsong(song,count)
    else:
        print("No more songs.")
        lcd.clear()
        lcd.message('NO MORE SONGS')

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

nameofsong = ''
path = '/home/pi/Desktop/project_1/'
def getsong(songnum,count):
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
    if(count == 1862):
        print ("test4")
    elif (count == 26):
        print("test5")
    elif count == 1954:
        print("test2")
    elif count == 17:
        print("test3")
    else:
        print("test")

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
    print(newtime_arr)
    print(len(newtime_arr))
    print(finalnotes_arr)
    print(len(finalnotes_arr))
    return finalnotes_array

def main():
    #Get path
    #Create array of all files, and array of only json files
    dirs = os.listdir( path )
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(20,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(21,GPIO.OUT,initial=GPIO.LOW)

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


    GPIO.add_event_detect(13,GPIO.FALLING,play)
    GPIO.add_event_detect(19,GPIO.FALLING,next)
    GPIO.add_event_detect(5,GPIO.FALLING,prev)

    while True:
        sleep(0.1)

if __name__=="__main__":
    main()


# Checks if array is with correct note
#for a in onplay:
#   print(a)
    #pprint(data) #prints all json file
#print(count) #print total number of notes
