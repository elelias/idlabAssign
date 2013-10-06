import math

class TraderPosition:
	'''This class represents the position of the trader
	trading under a certain algorithm. That is, there is one 
	instance of the class per algorithm. 
	The most important methods are:

	1) execute_decision : executes the trading decision
	determined by the algorithm to which is associated. 
	To this end, it calls 
	   buy_shares,
	   sell_shares,
	   close_position

	2) process_dividends : it finds whether there were
	dividends on a trading day and it process what to do 
	with them

	3) evaluate_position : it establishes which is the
	value of the trader portfolio after Close on a trading
	day
	'''




	def __init__(self,cash=0.0,symbolList=[]):

		self.cash=cash
		self.stockPosition={}
		self.currentPosition={}
		self.transactionCost=0.0025
		self.positionHistory=[]
		self.tradedSymbols=symbolList
		self.PFValue=0.0
		self.actions=[]
		self.PFValue_LastAction=0.0
		for element in self.tradedSymbols:
			self.currentPosition[element]='Closed'

	def __repr__(self):

		print 'the current trader position is as follows:'
		for sym,num in self.stockPosition.iteritems():
			print '    there are ',num,' shares of ',sym
		print '    the cash account is ',self.cash
		print '    currently the position is', self.currentPosition		
		print '    the total PF value at Close is ',self.PFValue


		return ''

	def name_position(self,symbol):
		#NAME THE CURRENT POSITION

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
			nShares= -self.stockPosition[symbol]
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
		#
		#
		#RECORD THIS ACTION
		
		self.actions[-1]['nShares']=nShares
		self.actions[-1]['price']=sharePrice
		self.actions[-1]['Date']=values['Date']

		#
		#
		#
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
	
		sharePrice=float(values['Open'])
		if number=='all':
			nShares=self.stockPosition[symbol]
		elif number=='max':
			#the maximum allowed number of shares if the position is
			#short, will be all of them for the time being
			availableCash=self.cash*(1.0-self.transactionCost)		
			nShares=int(availableCash/sharePrice)
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
		#
		#RECORD THIS ACTION
		self.actions[-1]['nShares']=nShares
		self.actions[-1]['price']=sharePrice
		self.actions[-1]['Date']=values['Date']
		#
		self.name_position(symbol)
	#
	#
	#
	#
	def close_position(self,symbol,values):
		'''closes the current position that the trader has'''
		#
		#
		#
		if self.currentPosition[symbol]=='Closed':
			print 'close_position is being called and the position is already closed'
			assert False
		elif self.currentPosition[symbol]=='Long':

			self.sell_shares('all',symbol,values)
		elif self.currentPosition[symbol]=='Short':

			self.buy_shares('all',symbol,values)
		else:
			print 'the position is not known ',self.currentPosition[symbol]
		#
		#
		#
		if not self.currentPosition[symbol]=='Closed':
			print 'the position was not closed'
			print 'there are ',self.stockPosition[symbol],' shares '
			assert False
	#
	#
	#
	#
	def execute_decision(self,decision,symbol,values):
		#
		#
		action=decision['action']
		newDict={'action':action}
		self.actions.append(newDict)
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

			self.close_position(symbol,values)
		else:
			print 'unknown action!'
			assert False

	#
	#
	#

	def process_dividends(self,stockHistory,symbol,dividends):
		'''finds out whether there were dividends paid on the 
		trading day and processes the cash inflow or outflow 
		depending on the position
		'''

		if len(stockHistory[symbol].history) >0:
			today=stockHistory[symbol].history[-1]['Date']
		#
		#
		for element in dividends:
			date=element['Date']
			if today == date:
				#
				#
				div=float(element['Dividends'])
				#
				#
				if self.currentPosition[symbol]=='Long':

					#print 'keeping the dividends!'
					cashInflow = self.stockPosition[symbol] * div
					self.cash += cashInflow
				elif self.currentPosition[symbol]=='Short':

					#print 'will have to pay the dividends!'
					cashOutFlow = self.stockPosition[symbol]*div
					#print 'the quantity is ',cashOutFlow
					self.cash += cashOutFlow #+ because this is already a negative number
				else:
					pass
					#print 'nothing to be done'


	def evaluate_position(self,symbol,values):
		'''finds out the value of the portfolio after
		the Close on a trading day
		'''

		self.PFValue=self.cash
		for symbol in self.tradedSymbols:
			if symbol in self.stockPosition:
				self.PFValue += self.stockPosition[symbol] * float(values['Close'])


		if len(self.actions)>0:
			self.actions[-1]['PFValue']=self.PFValue

		if len(self.actions)>0:
			if self.actions[-1]['action'] in ['buy','sell','close']:
				#the last action was not just sit:
				self.PFValue_LastAction=self.PFValue
			#	

		return self.PFValue



	def get_sharpeRatio(self,symbol):

		#
		#
		#get the pf values
		pfvalues=[]
		norm=self.actions[0]['PFValue']
		if norm != 100000.:
			print 'problem with sharpe',norm

		oldVal=0.0
		for val in self.actions:

			if oldVal==0.0:
				pfvalues.append(0.0)
				oldVal=val['PFValue']
			else:
				newVal=val['PFValue']
				pfvalues.append(newVal-oldVal)
				oldVal=newVal

		avrg=sum(pfvalues)/len(pfvalues)
		#print 'the average is ',avrg

		#get th stddev
		#print 'the length is now ',len(pfvalues)
		suma=0.
		for val in pfvalues:
			suma+= (val-avrg)*(val-avrg)
		#print 'suma is ',suma

		stddev=math.sqrt(suma/(len(pfvalues)-1))
		#print 'the stddev is ',stddev

		sharpeRatio= math.sqrt(252)*avrg/stddev

		return sharpeRatio






	if __name__=='__main__':

		print 'this class represents the position of a trader'
		print 'trading under a certain algorithm'








