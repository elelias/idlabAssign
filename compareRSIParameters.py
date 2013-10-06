

import sys
import csv
from stockHistory import StockHistory
from algorithmRSI import AlgorithmRSI
from traderPosition import TraderPosition
from makeMoney import make_money
from parseArguments import parse_arguments
from processPerformance import process_performance,compare_performance
import copy





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
	#SYMBOLS TRADING
	tradingSymbols=['SPY']
	#
	#THIS SYMBOL HAS A HISTORY, ASSOCIATE AN INSTANCE OF StockHistory
	stockHistory['SPY']=StockHistory()
	#	
	#	



	#===============================================
	# RSI ALGORITHM BUNDLE 30 70
	#===============================================
	parameters={'buyAt':30,'sellAt':70, 'RSI_PERIODS':14,'stop_loss':True,'VERBOSE':False}
	#
	# CREATE A NEW INSTANCE OF THE ALGORITHM
	algorithmRSI=AlgorithmRSI(parameters) 
	#
	#
	#REPRESENT THE POSITION OF THE TRADER WITH
	#A TraderPosition OBJECT TRADING UNDER THIS ALGORITHM
	traderRSI=TraderPosition(INITIAL_CASH,tradingSymbols)
	#
	#REPRESENT THE DAILY PORTFOLIO VALUE WITH A LIST
	portfolioValues={}
	#
	#CREATE A BUNDLE WITH THE ALGORITHM AND THE TRADER POSITION
	bundleRSI = (algorithmRSI,traderRSI,copy.copy(portfolioValues))
	#
	#PACKAGE IT ALL IN A DICT:
	algorithmsDictionary={'RSI_30_70_14':bundleRSI}
	#===============================================



	#===============================================
	# RSI ALGORITHM BUNDLE 22 70
	#===============================================
	parameters={'buyAt':22,'sellAt':70, 'RSI_PERIODS':14,'stop_loss':True,'VERBOSE':False}
	#
	# CREATE A NEW INSTANCE OF THE ALGORITHM
	algorithmRSI_2=AlgorithmRSI(copy.copy(parameters))
	#
	#
	#REPRESENT THE POSITION OF THE TRADER WITH
	#A TraderPosition OBJECT TRADING UNDER THIS ALGORITHM
	traderRSI_2=TraderPosition(INITIAL_CASH,tradingSymbols)
	#
	#REPRESENT THE DAILY PORTFOLIO VALUE WITH A LIST
	portfolioValues={}
	#
	#CREATE A BUNDLE WITH THE ALGORITHM AND THE TRADER POSITION
	bundleRSI_2 = (algorithmRSI_2,traderRSI_2,copy.copy(portfolioValues))
	#
	#PACKAGE IT ALL IN A DICT:
	algorithmsDictionary['RSI_22_70_14']=bundleRSI_2
	#===============================================	
	#
	#
	#
	#===============================================
	# RSI ALGORITHM BUNDLE 30 75
	#===============================================
	parameters={'buyAt':30,'sellAt':75, 'RSI_PERIODS':14,'stop_loss':True,'VERBOSE':False}
	#
	# CREATE A NEW INSTANCE OF THE ALGORITHM
	algorithmRSI_3=AlgorithmRSI(copy.copy(parameters))
	#
	#
	#REPRESENT THE POSITION OF THE TRADER WITH
	#A TraderPosition OBJECT TRADING UNDER THIS ALGORITHM
	traderRSI_3=TraderPosition(INITIAL_CASH,tradingSymbols)
	#
	#REPRESENT THE DAILY PORTFOLIO VALUE WITH A LIST
	portfolioValues={}
	#
	#CREATE A BUNDLE WITH THE ALGORITHM AND THE TRADER POSITION
	bundleRSI_3 = (algorithmRSI_3,traderRSI_3,copy.copy(portfolioValues))
	#
	#PACKAGE IT ALL IN A DICT:
	algorithmsDictionary['RSI_30_75_14']=bundleRSI_3
	#===============================================	
	#
	#
	#
	#===============================================
	# RSI ALGORITHM BUNDLE 22 75
	#===============================================
	parameters={'buyAt':22,'sellAt':75, 'RSI_PERIODS':14,'stop_loss':True,'VERBOSE':False}
	#
	# CREATE A NEW INSTANCE OF THE ALGORITHM
	algorithmRSI_4=AlgorithmRSI(copy.copy(parameters))
	#
	#
	#REPRESENT THE POSITION OF THE TRADER WITH
	#A TraderPosition OBJECT TRADING UNDER THIS ALGORITHM
	traderRSI_4=TraderPosition(INITIAL_CASH,tradingSymbols)
	#
	#REPRESENT THE DAILY PORTFOLIO VALUE WITH A LIST
	portfolioValues={}
	#
	#CREATE A BUNDLE WITH THE ALGORITHM AND THE TRADER POSITION
	bundleRSI_4 = (algorithmRSI_4,traderRSI_4,copy.copy(portfolioValues))
	#
	#PACKAGE IT ALL IN A DICT:
	algorithmsDictionary['RSI_22_75_14']=bundleRSI_4
	#===============================================	
	#
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
	print 'processing the results now'
	#COMPARE ALGORITHMS AMONG THEMSELVES
	plotParameters={}
	plotParameters['plotName']='parameters.pdf'
	compare_performance(stockHistory,algorithmsDictionary,plotParameters)

	#Get their sharpe ratio:
	#PROCESS THE PERFORMANCE OF EACH ALGORITHM
	for name,bundle in algorithmsDictionary.iteritems():
		#
		traderPosition=bundle[1]
		sharpeRatio=traderPosition.get_sharpeRatio('SPY')	
		print 'the sharpe ratio for ',name, 'is ',traderPosition.get_sharpeRatio('SPY')		





