

import sys
import csv
from stockHistory import StockHistory
from algorithmRSI import AlgorithmRSI
from traderPosition import TraderPosition
#from executeDecision import execute_decision



def make_money(fileName,stockHistory,algorithms):


	with open(fileName) as ffile:
		#
		#
		reader = csv.DictReader(ffile)
		#
		#
		for row in reader:
			#
			#
			stockHistory['SPY'].add_entry(row)			
			#
			#
			for name,bundle in algorithms.iteritems():
				#
				#
				algorithm=bundle[0]
				traderPosition=bundle[1]
				#
				#
				#TRADE EVERY SYMBOL
				for symbol in traderPosition.tradedSymbols:
					#
					#
					#THE ALGORITHM MAKES A DECISION
					decision=algorithm.make_decision(stockHistory,symbol,traderPosition)
					print 'the decision was',decision
					#
					#
					#THE TRADER EXECUTES IT
					traderPosition.execute_decision(decision,symbol,row)
					print 'the decision is executed'
					print traderPosition
					raw_input('')





if __name__=='__main__':

	if len(sys.argv)>1:
		fileName=sys.argv[1]
	else:
		print 'there is no file to read'
		sys.exit()
	#
	stockHistory={}
	#
	INITIAL_CASH=100000.0
	#
	#
	# RSI ALGORITHM
	parameters={'buyAt':35,'sellAt':65, 'RSI_PERIODS':14}
	#
	# CREATE A NEW INSTANCE OF THE ALGORITHM
	algorithmRSI=AlgorithmRSI(parameters) 
	#
	#SYMBOLS TRADING
	tradingSymbols=['SPY']
	#
	#
	#THIS SYMBOL HAS A HISTORY, ASSOCIATE AN INSTANCE OF StockHistory
	stockHistory['SPY']=StockHistory()
	#
	#REPRESENT THE TRADERPOSITION OBJECT TRADING
	#UNDER THIS ALGORITHM
	traderRSI=TraderPosition(INITIAL_CASH,tradingSymbols)
	#
	#CREATE A BUNDLE WITH THE ALGORITHM AND THE POSITION
	bundleRSI = (algorithmRSI,traderRSI)
	#
	#PACKAGE IT IN A DICT:
	algorithmsDictionary={'RSI_40_60':bundleRSI}
	#





	#START TRADING WITH THE DIFFERENT ALGORITHMS AND MAKE MONEY
	make_money(fileName,stockHistory,algorithmsDictionary)
	#
	#
