##WITHOUT LCD SCREEN
import json
import RPi.GPIO as GPIO
import array as arr
import sys
import glob
from time import sleep
import os

song = 0
notes_array = []
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
    else:
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





nameofsong = ''
path = '/home/pi/Desktop/usb'
def getsong(songnum,count):
    with open(json_arr[songnum]) as data_file:
        data = json.load(data_file)
        for p in data['tracks']:
            for f in p['notes']:
                notes_array.append(f['time'])
                notes_array.append(f['name'])
                count = count + 1 #keeps count of number of notes
    #print(count)
    nameofsong= data['header']['name']
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
    #print (notes_array)
    return notes_array

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
