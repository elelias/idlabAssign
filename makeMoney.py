

import sys
import csv
from stockHistory import StockHistory
from algorithmRSI import AlgorithmRSI
from traderPosition import TraderPosition
from getDividends import get_dividends


global VERBOSE
VERBOSE=False

def make_money(fileNames,stockHistory,algorithms):


	#Portfolio value after 
	#each trading day
	#PFValue=[]



	#LOAD THE DIVIDENDS LIST
	if len(fileNames)>1:
		dividends=get_dividends(fileNames[1])



	#START THE TRADES
	stockHistoryFile=fileNames[0]
	with open(stockHistoryFile) as sFile:
		#
		#
		reader = csv.DictReader(sFile)
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
				PFValue=bundle[2]
				#
				#
				#TRADE EVERY SYMBOL
				for symbol in traderPosition.tradedSymbols:
					#
					#
					#
					#
					#THE ALGORITHM MAKES A DECISION
					decision=algorithm.make_decision(stockHistory,symbol,traderPosition)
					#print 'the decision was',decision['action']
					#
					#
					#THE TRADER EXECUTES IT
					traderPosition.execute_decision(decision,symbol,row)
					#
					#
					#
					#
					#
					#PROCESS POSSIBLE DIVIDENDS
					traderPosition.process_dividends(stockHistory,symbol,dividends)
					#
					#
					#EVALUATE AND SAVE THE POSITION OF THE TRADER AFTER CLOSE
					if not symbol in PFValue:
						PFValue[symbol]=[]
					PFValue[symbol].append(traderPosition.evaluate_position(symbol,row))

					#
					#
					#
					if VERBOSE:
						print stockHistory[symbol]
						print traderPosition
						raw_input('press any key')




