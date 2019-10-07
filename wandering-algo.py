import pandas as pd

"""

#Function name : read_header_from_CSV
#Author : 
#Function description : Exract session variables and values from the first row of .CSV data file to a dictionary. 
#Input parameters: 
	1. Data file path
#Return : 
	1. A dictionary data type with -
		keys : session variables 
		values: session values 

#pre-condition: 
	1. file path is valid

Sample session info row : 
	{
	Format Version : 1.21, 
	Take name : session_Packing, 
	Capture Frame Rate : 120, 
	Export Frame Rate : 120, 
	Capture Start Time : 2017-09-15 02.50.17 PM, 
	Total Frames in Take : 7978, 
	Total Exported Frames : 7978, 
	Rotation Type : Quaternion, 
	Length Units : Meters, 
	Coordinate Space : Global
	}
"""

def read_header_from_CSV(filepath):
	#read first row of data (session info row)
	df = pd.read_csv(filepath, sep=',', nrows = 1, header = None).dropna()
	# Get number of columns (parameters and parameter value)
	no_of_columns = df.shape[1]
	#extract session variables and corresponding value to dictionary 
	parameters = dict()
	for i in range(0, no_of_columns, 2):
		parameters[df.loc[0][i]] = df.loc[0][i+1]
	return parameters



