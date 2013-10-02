

class TraderPosition:


	def __init__(cash=0.0):

		self.cash=cash
		self.stockPosition={}
		self.currentPosition=None
		self.transactionCost=0.0025

	def buy_shares(number,values):
		'''buys some shares at the current price.
		It can buy either:
		1) max, which buys as many as possible with the available Cash
		2) all, which buys all the shares that are shorted so that the position is closed
		3) number, a certain number of them '''


		availableCash=self.cash
		symbol=values['symbol']

		if number=='max':
			availableCash=availableCash*(1.0-self.transactionCost)		
			nShares=int(availableCash/values['price'])

		elif number=='all':
			nShares= -self.currentPosition[symbol]
			if nShares < 0:
				print 'WARNING:'
				print '  \'All\' was selected but the position was not short'
				print '  A \'max\' trade is done instead'
				buy_shares('max',values)


		else
			pass



		self.stockPosition[symbol]+=nShares

		#operation cost
		totalCost=nShares*values['price']*(1.0+self.transactionCost)
		#
		self.cash=self.cash - totalCost
		#
		if self.cash < 0.0:
			print 'negative cash position',self.cash
			print 'cost = ',cost



		#EVALUATE THE CURRENT POSITION
		if self.stockPosition[symbol]>0:
			self.currentPosition[symbol]='Long'
		elif self.stockPosition[symbol]==0:
			self.currentPosition[symbol]='Closed'
		else:
			print 'the position is short after a buy, is this OK?'
			self.currentPosition[symbol]='Short'

	def sell_shares(number,values):

		if number=='max':
			symbol=values['symbol']
			nShares=self.stockPosition[symbol]
		else:
			pass
		#
		cashInflow=nShares * values['price']
		tradingCost=cashInflow * self.transactionCost
		self.cash=self.cash + cashInflow - tradingCost
		self.stockPosition[symbol] = self.stockPosition[symbol] - nShares
		#
		#
		#EVALUATE THE CURRENT POSITION
		if self.stockPosition[symbol]>0:
			print 'the position is long after a sale, is this OK?'			
			self.currentPosition[symbol]='Long'
		elif self.stockPosition[symbol]==0:
			self.currentPosition[symbol]='Closed'
		else:
			self.currentPosition[symbol]='Short'
		#
	#
	#
	def close_position(symbol,values):
		'''closes the current position that the trader has'''
		if self.stockPosition[symbol]=='Closed':
			return
		elif self.stockPosition[symbol]=='Long':
			sell_shares('max',values)
		elif self.stockPosition[symbol]=='Short':
			buy_shares('max',values)

	def execute_decision(self,decision,values):

		action=decision['action']
		symbol=values['symbol']

		if action=='sit':
			return

		if action=='buy':

			if self.currentPosition=='Long':
				#ONLY ONE POSITION AT A TIME
				return
			elif self.currentPosition=='Short':
				close_position(values)
			elif self.currentPosition=='Closed'

				buyQuantity=decision['buyQuantity']
				buyPrice=values['price']




