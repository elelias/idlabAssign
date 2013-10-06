
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
	# RSI ALGORITHM BUNDLE 30 70 WITHOUT STOP-LOSS
	#===============================================
	parameters={'buyAt':30,'sellAt':70, 'RSI_PERIODS':14,'stop_loss':False,'VERBOSE':False}
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
	# RSI ALGORITHM BUNDLE 30 70 WITH STOP-LOSS
	#===============================================
	parameters={'buyAt':30,'sellAt':70, 'RSI_PERIODS':14,'stop_loss':True,'VERBOSE':False}
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
	algorithmsDictionary['RSI_30_70_14_stoploss']=bundleRSI_2
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
	print ''
	print ''
	#
	#
	#PROCESS THE PERFORMANCE OF EACH ALGORITHM
	for name,bundle in algorithmsDictionary.iteritems():
		#
		traderPosition=bundle[1]
		PFvalue=bundle[2]
		plotParameters={}
		plotParameters['plotName']=name+'.pdf'

		if 'RSI_22_70_14' in name:
			plotParameters['ymin']=50000
			plotParameters['ymax']=300000
		elif 'RSI_30_70_14' in name:	
			plotParameters['ymin']=30000
			plotParameters['ymax']=200000
		process_performance(name,stockHistory,traderPosition,PFvalue,plotParameters)


		print 'the sharpe ratio for ',name, 'is ',traderPosition.get_sharpeRatio('SPY')








