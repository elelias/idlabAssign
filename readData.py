

import sys
import csv
from stockHistory import StockHistory
from algorithmRSI import AlgorithmRSI
#from executeDecision import execute_decision


def make_money(fileName,algorithms):

	stockHistory=StockHistory()
	with open(fileName) as ffile:
		#
		#
		reader = csv.DictReader(ffile)
		#
		#
		for row in reader:
			#
			#
			stockHistory.add_entry(row)
			print stockHistory
			#
			#
			for name,algorithm in algorithms.iteritems():
				#
				decision=algorithm.make_decision(stockHistory)
				print decision
				raw_input('')
				#
				#execute_decision(decision)



if __name__=='__main__':

	if len(sys.argv)>1:
		fileName=sys.argv[1]
	else:
		print 'there is no file to read'
		sys.exit()
	#
	#
	# RSI ALGORITHM
	parameters={'buyAt':35,'sellAt':65,'quantity':'max'}
	# CREATE A NEW INSTANCE OF THE ALGORITHM
	algorithmRSI=AlgorithmRSI(parameters) 



	algorithmsDictionary={'RSI_40_60':algorithmRSI}

	#
	#START TRADING WITH THE DIFFERENT ALGORITHMS
	make_money(fileName,algorithmsDictionary)
	#
	#
