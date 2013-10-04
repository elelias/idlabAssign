
import csv
def get_dividends(fileName):
	'''this function reads the dividends for a given 
	symbol and stores them into a list
	'''

	dividendList=[]
	with open(fileName) as dFile:
		reader=csv.DictReader(dFile)
		for row in reader:
			dividendList.append(row)
		#

	return dividendList




