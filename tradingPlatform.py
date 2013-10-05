

import sys
import csv
from stockHistory import StockHistory
from algorithmRSI import AlgorithmRSI
from traderPosition import TraderPosition
from makeMoney import make_money
from parseArguments import parse_arguments
from processPerformance import process_performance





if __name__=='__main__':



	parseOK,fileNames=parse_arguments(sys.argv)
	if not parseOK:
		sys.exit()
	#
	#
	#
	#
	#
	stockHistory={}
	#
	INITIAL_CASH=100000.0
	#
	#
	# RSI ALGORITHM
	parameters={'buyAt':35,'sellAt':55, 'RSI_PERIODS':14,'stop_loss':True,'VERBOSE':False}
	#
	# CREATE A NEW INSTANCE OF THE ALGORITHM
	algorithmRSI=AlgorithmRSI(parameters) 
	#
	#SYMBOLS TRADING
	tradingSymbols=['SPY']
	#
	#THIS SYMBOL HAS A HISTORY, ASSOCIATE AN INSTANCE OF StockHistory
	stockHistory['SPY']=StockHistory()
	#
	#
	#
	#REPRESENT THE POSITION OF THE TRADER WITH
	#A TraderPosition OBJECT TRADING UNDER THIS ALGORITHM
	traderRSI=TraderPosition(INITIAL_CASH,tradingSymbols)
	#
	#REPRESENT THE DAILY PORTFOLIO VALUE WITH A LIST
	portfolioValues={}
	#
	#
	#CREATE A BUNDLE WITH THE ALGORITHM AND THE TRADER POSITION
	bundleRSI = (algorithmRSI,traderRSI,portfolioValues)
	#
	#PACKAGE IT ALL IN A DICT:
	algorithmsDictionary={'RSI_35_50':bundleRSI}
	#
	#
	#
	#
	#

	#START TRADING WITH THE DIFFERENT ALGORITHMS AND MAKE MONEY
	make_money(fileNames,stockHistory,algorithmsDictionary)
	#
	#
	print 'done making money!'
	#
	#
	#PROCESS THE PERFORMANCE OF EACH ALGORITHM
	for name,bundle in algorithmsDictionary.iteritems():
		traderPosition=bundle[1]
		PFvalue=bundle[2]
		process_performance(name,stockHistory,traderPosition,PFvalue)






