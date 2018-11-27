import json
import array as arr
import sys
import glob
import errno
from time import sleep
import os
#import keyboard

nameofsong = ''
path = '/Users/alejandrasandoval/Desktop/usb/'
def getsong(songnum,count):
    with open(json_arr[songnum]) as data_file:
        data = json.load(data_file)
        for p in data['tracks']:
            for f in p['notes']:
                notes_array.append(f['time'])
                notes_array.append(f['name'])
                count = count + 1 #keeps count of number of notes
    #print(count)
    print("Filename: ")
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

    return notes_array

#Get path
#Create array of all files, and array of only json files
dirs = os.listdir( path )
files_arr = []
json_arr = []

# Creates array of files
for file in dirs:
    files_arr.append(file)

# This would print all the files and directories for testing.
print("List of files:")
for f in files_arr:
    print (f)

#This adds only json fil es to array (Need this for the actual playing"
for g in files_arr:
    if g[-4:] == 'json':
        json_arr.append(g)
print("List of jsons:")
print(json_arr)

song = 0
notes_array = []
play = True


while(play):
    x = input ('Play/Replay (P), Next(N) or Pause(X) \n')
    count = 0
    if x == 'P' or x == 'p':#if key 'q' is pressed
        if (song) < len(json_arr):
            onplay = getsong(song, count)
        else:
            print("No more songs.")
    
    if x == 'N' or x== 'n':
        if(song + 1) < len(json_arr):
            song =  song + 1
            onplay = getsong(song,count)
        else:
            onplay = ['']
            print("No more songs.")


    if x == 'X' or x == 'x':
        onplay = ['']
        print('Pause')
        sleep (1)
    for a in onplay:
        print(a)


# Checks if array is with correct note
for a in onplay:
   print(a)
    #pprint(data) #prints all json file
#print(count) #print total number of notes

