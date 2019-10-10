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


"""

#Function anme : read_data_from_CSV
#Author : 
#Function description : Extract sequence of time and location data from .CSV data file to a dictionary
#Input Parameters : 
	1. Data filepath 
#Return : 
	1. Dataframe consisting movement data 
#Pre-Condition : 
	1. filepath is valid 

Sample extracted header of data file: 
	Frame, Time, X.1, Z.1
Sameple rows of data file
	0, 0.000000, - 2.041308, 1.913831
	1, 0.003344, - 2.042123, 1.929382
"""

def read.read_data_from_CSV(filepath)
	#column numbers to extract 
	cols = [0, 1, 6, 8]
	#read csv 
	#comma(,) delimited
	#read only selected columns (0=Frame, 1=Time, 6=X.1, 8=Z.1)
	#header is at row 6, do not read previous rows (0-5)
	#Do not skip blank lines while reading 
	#Drop rows with NA values
	df = pd.read_csv(filepath, sep = ',', usecols = cols, header = 6, skip_blank_lines=False).dropna()
	return df














