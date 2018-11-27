import json
import indexNotes as indNotes

count = 0
notes_array=[]
notes_time = []
finalnotes_arr = []
newtime_arr = []
newnote = 0

with open('test.json') as data_file:
	data = json.load(data_file)
	for p in data['tracks']:
		for f in p['notes']:
			notes_time.append(f['time'])
			notes_array.append(f['name'])
			count = count + 1 #keeps count of number of notes
print (notes_array)
print (notes_time)

print(count)
matchingindex = []
lowestindex = 0
x = 0
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



print(newtime_arr)
print(len(newtime_arr))
print(finalnotes_arr)
print(len(finalnotes_arr))
