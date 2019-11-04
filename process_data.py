import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import math

"""

#Function name : preprocess
#Author : Arshia Zernab Hassan
#Function description : Apply pre-processing steps to time-stamp coordinate Data Frame 
#Input parameters : 
	1. Pandas Data Frame 
Sample header of input data frame : 
	Frame Time X.1	Z.1
Sample rows of input data frame 
	0	0.000000	-2.043234	1.983431
	1	0.008833	-2.041301	1.938320
#Return : 
1. Data frame after pre-processing 
#Pre-condition : 
	1. data frame has valid value

"""

def preprocess(df):
	#Average rolling window of 500 data points 
	df = df.rolling(window=100).mean().dropna()
	#Add index column : date time derived from time-stamp
	df.index = pd.to_datetime(df.index, unit ='s')
	# resample data
	r = df.resample(rule ='60S')
	df = r.mean()
	return df


"""

#Function name : vector_angle_global
#Author : Arshia Zernab Hassan 
#Function description : Calculate and add global vector angles to Data Frame to a dictionary 
#Input Parameters : 
	1. Pandas Data Frame with headers -
	Frame 	Time 	X.1		Z.1
#Return : 
	1.	Data frame with headers -
	frame 	Time 	X.1 	Z.1		vector 		theta 

#Pre-condition :
	1. data frame has valid value 
"""

def vector_angle_global(df):
	# create column of vector [X, Z] - 4th column 
	# ([X, Z]) is a vector from origin to data point L(X, Z)) )
	temp_vector = list()
	for row in range(0, len(df)):
		temp_vector.append(np.array([float(df.iloc[row, 2]), float(df.iloc[row, 3])]))
	df['vector'] = temp_vector	# add column under 'vector' heading 
	
	#calculate angle between vectors and add to list 
	temp_theta = list()

	for row in range(0, len(df) - 1, 1):
		# cos(theta) = dot_product(u, v)/length(u)/length(v); u and v are vectors
		cos_theta = np.dot(df.iloc[row, 4], df.iloc[row + 1, 4]) / np.linalg.norm(df.iloc[row, 4])/np.linalg.norm(df.iloc[row + 1, 4])
		# if cos(theta) is in velid range
		if cos_theta <= 1.0 and cos_theta >= -1.0 : 
			#theta = acos(.);
			theta = math.degrees(math.acos(cos_theta))
			# add value of theta
			temp_theta.append(theta)
		else:
			#add nan
			temp_theta.append(np.nan)

	#pad array to math length of dataframe 

	for pad in range(len(temp_theta), len(df)) : 
		temp_theta.append(np.nan)

	#add newly calculated angle list to dataframe under header 'theta' - 5th column 
	df['theta'] = temp_theta
	return df


"""

#Function name : vector_angle_relative
#Author : 
#Function description : Calculate and add relative vector angles to Data Frame to a dictionary 
#Input parameters : 
	1. Pandas Data Frame with headers - 
		Frame 	Time 	X.1 	Z.1
#Return : 
	1. Dataframe with headers -
		Frame 	Time 	X.1 	Z.1 	vector 	theta 
#Pre-condition : 
	1. dataframe has valid value

"""

def vector_angle_relative(df):
	#create column of vector [X_2 - X_1, Z_2 - Z_1] - 4th column 
	#([X_2 - X_1, Z_2 - Z_1] is a vector from data point L_1(X_1, Z_1) to L_2(X_2, Z_2))
	temp_vector = list()
	for row in range(0, len(df) - 1):
		x21 = df.iloc[row + 1, 2] - df.iloc[row, 2]
		z21 = df.iloc[row + 1, 3] - df.iloc[row, 3]
		temp_vector.append(np.array([x21, z21]))
	
	#pad array to match length of dataframe 
	for pad in range(len(temp_vector), len(df)):
		temp_vector.append(np.nan)

	df['vector'] = temp_vector	# add column under 'vector' header 

	#calculate angle between vectors and add to list 
	temp_theta = list()

	for row in range(0, len(df) - 2, 1):
		# cos(theta) = dot_product(u, v) / length(u) / length(v); u and v are vectors
		cos_theta = np.dot(df.iloc[row, 4], df.iloc[row + 1, 4]) / np.linalg.norm(df.iloc[row, 4]) / np.linalg.norm(df.iloc[row + 1, 4])
		#if cos(theta) is in valid range 
		if cos_theta <= 1 and cos_theta >= -1.0:
			#theta = acos(.);
			theta = math.degrees(math.acos(cos_theta))
			#add value of theta
			temp_theta.append(theta)
		else: 
			#add nan
			temp_theta.append(np.nan)

	#pad array to match length of dataframe 
	for pad in range(len(temp_theta), len(df)):
		temp_theta.append(np.nan)


	#add newly calculated angle list to dataframe under header 'theta' - 5th column
	df['theta'] = temp_theta
	return df
	

"""

#Function name : rate_of_change_angle
#Author : 
#Function description : Calculate and add 'rate of change of angles' to Data Frame 
#Input parameters : 
	1. Pandas Dataframe with headers -
	Frame 	Time 	X.1 	Z.1 	vector 		theta
#Return : 
	1. Dataframe with headers - 
	Frame 	Time 	X.1 	Z.1 	vector 		theta 		rate 
#Pre-condition : 
	1. data frame has valid value 
"""

def rate_of_change_angle(df):
	#create column of vector angle change rate - 6th column 
	temp_rate = list()
	for row in range(0, len(df) - 1, 1):
		#dT = T2 - T1
		denom = (float(df.iloc[row + 1, 1]) - float(df.iloc[row, 1]))
		if denom != 0 :
			#rate = (theta2 - theta1) / dT
			angle_rate = (float(df.iloc[row + 1, 5]) - float(df.iloc[row, 5])) / denom
			#add value of rate 
			temp_rate.append(angle_rate)
		else: 
			# add nan
			temp_rate.append(np.nan)

	#pad array to match length of dataframe 
	for pad in range(len(temp_rate), len(df)):
		temp_rate.append(np.nan)


	#add newly calculated 'rate of angle change' list to datafram under header 'rate' - 6th column 
	df['rate'] = temp_rate
	df.dropna()	# discard all rows with nan 
	return df

"""

#Function name : calculate_distance 
#Author : 
#Function description : Calculate and add 'distance between consective points' to Data Frame 
#Input Parameters : 
	1. Pandas Dataframe with headers - 
	Frame 	Time 	X.1 	Z.1 	vector 		theta 		rate 
#Return : 
	1. 	Dataframe with headers - 
	Frame 	Time 	X.1 	Z.1 	vector 		theta 		rate 		distance 
#Pre-condition : 
	1. Dataframe has valid value 
"""

def calculate_distance(df):
	temp_distance = list()
	for row in range(0 ,len(df) - 1): #for all rows in dataframe 
		x21 = df.iloc[row + 1, 2] - df.iloc[row, 2] #difference between x coordinates of the two points 
		z21 = df.iloc[row + 1, 3] - df.iloc[row, 3]	#difference between z coordinates of the two points 
		distance = math.sqrt(math.pow(z21, 2) + math.pow(z21, 2))	# segment length between two points 
		temp_distance.append(distance) # add to list

	#pad array to match length of dataframe 
	for pad in range(len(temp_distance), len(df)):
		temp_distance.append(np.nan)

	# add newly calculated 'segment length' list to dataframe under header 'distance' - 7th column 
	df['distance'] = temp_distance
	return df 
