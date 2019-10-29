"""

#Function name : algo_1
#Author : 
#Function description : Count number of wandering traces n movement data
#Input parameters : 
	1. Dataframe with headers - 
	Frame 	Time 	X.1 	Z.1		vector 		theta 		rate 		distance 
#Return : 
Wandering trace count 

#Pre-Condition : 
	1. Dataframe has valid value 

"""

def algo_1(df):
	has_sharp = False # variable to keep track of sharp point encounter 
	segments = 0 #variable to keep track of segments between sharp points 
	wandering = 0 # variable to keep track of wandering trace 

	for row in range(0, len(df) - 1):	#for all rows in data frame 
		if df.iloc[row, 5] >= 90 : #if angle is equal or more than 90 degrees (5th column) (a sharp point)
			if has_sharp == False : # if this is the first sharp point 
				row1 = row # save the current row as first sharp point row 
				has_sharp = True # a sharp point has been encountered 
			else: # if there is a previous sharp point 
				row2 = row #save the current row as second sharp point row 
				distance = df.iloc[row1:row2, 7].sum() #sum of segment lengths between the last two sharp points 
				if distance < 10 : #if segment length smaller than threshold 
					segments += 1 # add to segment count 
					if segments == 4 : # if segment count is equal or more than 4 
					wandering += 1 # add to wandering trace count 
				else: 
					segments = 0 # re-initialize segment count to 0
				row1 = row2 #set previous sharp point by current sharp point 
	return wandering # return wandering trace counts 

