

class TraderPosition:

	def __init__(self,cash=0.0,symbolList=[]):

		self.cash=cash
		self.stockPosition={}
		self.currentPosition={}
		self.transactionCost=0.0025
		self.positionHistory=[]
		self.tradedSymbols=symbolList
		for element in self.tradedSymbols:
			self.currentPosition[element]='Closed'

	def __repr__(self):

		print 'the current trader position is as follows:'
		for sym,num in self.stockPosition.iteritems():
			print '    there are ',num,' shares of ',sym
		print '    the cash account is ',self.cash
		print '    currently the position is', self.currentPosition
		return ''

	def name_position(self,symbol):
		#NAME THE CURRENT POSITION
		print 'the symbol at name_position is',symbol,'with type',type(symbol)
		if self.stockPosition[symbol]>0:
			self.currentPosition[symbol]='Long'
		elif self.stockPosition[symbol]==0:
			self.currentPosition[symbol]='Closed'
		else:
			self.currentPosition[symbol]='Short'
	#


	def buy_shares(self,number,symbol,values):
		'''buys some shares at the current price.
		It can buy either:
		1) max, which buys as many as possible with the available Cash
		2) all, which buys all the shares that are shorted so that the position is closed
		3) number, a certain number of them '''
		#
		#
		availableCash=self.cash
		sharePrice=float(values['Open'])
		#
		#
		#AS MANY AS POSSIBLE
		if number=='max':
			availableCash=availableCash*(1.0-self.transactionCost)		
			nShares=int(availableCash/sharePrice)

		#AS MANY AS ARE SHORTED
		elif number=='all':
			nShares= -self.currentPosition[symbol]
			if nShares < 0:
				print 'WARNING:'
				print '  \'All\' was selected but the position was not short'
				print '  A \'max\' trade is done instead'
				self.buy_shares('max',values)
			#
		#AS MANY AS TOLD
		else:
			nShares=number			
		#
		#
		if symbol in self.stockPosition:
			self.stockPosition[symbol]+=nShares
		else:
			self.stockPosition[symbol]=nShares
		#
		#
		#OPERATION COST
		totalCost=nShares*sharePrice*(1.0+self.transactionCost)
		#IMPACT ON CASH
		self.cash=self.cash - totalCost
		#
		#
		#CHECK
		if self.cash < 0.0:
			print 'negative cash position!',self.cash
			print 'cost = ',cost
		#
		#
		#PROVIDE A NAME FOR THIS POSITION
		self.name_position(symbol)
		#
		#
	#
	#
	#
	#
	def sell_shares(self,number,symbol,values):
		'''it sells either:
		1) the total number of shares that the trader has for the symbol, or
		2) the number of shares that it's told
		'''
	
		sharePrice=values['Open']
		if number=='all':
			nShares=self.stockPosition[symbol]
		else:
			nShares=number
		#
		cashInflow=nShares * sharePrice
		tradingCost=cashInflow * self.transactionCost
		self.cash=self.cash + cashInflow - tradingCost
		if symbol in self.stockPosition:
			self.stockPosition[symbol] = self.stockPosition[symbol] - nShares
		else:
			self.stockPosition[symbol] = - nShares
		#
		self.name_position(symbol)
	#
	#
	#
	#
	def close_position(self,symbol,values):
		'''closes the current position that the trader has'''
		if self.stockPosition[symbol]=='Closed':
			return
		elif self.stockPosition[symbol]=='Long':
			self.sell_shares('all',values)
		elif self.stockPosition[symbol]=='Short':
			self.buy_shares('all',values)

		self.name_position(symbol)
		if not self.currentPosition=='Closed':
			print 'the position was not closed'
			print 'there are ',self.stockPosition,' shares '
			assert False
	#
	#
	#
	#
	def execute_decision(self,decision,symbol,values):
		#
		#
		action=decision['action']
		#
		#
		if action=='sit':
			pass
		elif action=='buy':
			buyQuantity=decision['buyQuantity']
			self.buy_shares(buyQuantity,symbol,values)
		#
		elif action=='sell':
			sellQuantity=decision['sellQuantity']
			self.sell_shares(sellQuantity,symbol,values)
		#
		elif action=='close':
			close_position(symbol,values)
		else:
			print 'unknown action!'
			assert False
	#
	#
	#
	#



	if __name__=='__main__':

		print 'this class represents the position of a trader'
		print 'trading under a certain algorithm'






