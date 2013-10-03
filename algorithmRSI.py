


class AlgorithmRSI:

	'''this class represents an algorithm that 
	takes the rsi into account to perform decisions'''

	def __init__(self,parameters):

		self.parameters=parameters
		self.RSI_PERIODS=parameters['RSI_PERIODS']
		self.action={}
		self.averageGain=0.0
		self.averageLoss=0.0
		self.sumGain=0.0
		self.sumLoss=0.0		
		self.RSI=0.0
		self.RS=0.0
		self.nPeriods=0
		self.buyAt=parameters.get('buyAt',None)
		self.sellAt=parameters.get('sellAt',None)
		self.buyQuantity=parameters.get('buyQuantity',None)
		self.sellQuantity=parameters.get('sellQuantity',None)		
	#
	#
	#
	#




	def get_RS(self,newValue,oldValue):
		'''gets the average gain over the average loss in the last 14 periods
		and 0 if there are no 14 periods yet'''

		#
		#
		diffLast=newValue-oldValue
		#
		#
		self.nPeriods+=1
		#
		#
		#the initial difference is artificially high
		if self.nPeriods==1:
			diffLast=0.0
		#
		#
		#
		if self.nPeriods<=self.RSI_PERIODS:
			if diffLast<0:
				self.sumLoss += diffLast
			else:
				self.sumGain += diffLast

		if self.nPeriods < self.RSI_PERIODS:
			self.RS=0.0
			return

		elif self.nPeriods==self.RSI_PERIODS:
			self.averageLoss=self.sumLoss/self.RSI_PERIODS
			self.averageGain=self.sumGain/self.RSI_PERIODS

		else:						
			if diffLast<0.:
				self.averageLoss = (self.averageLoss*(self.RSI_PERIODS-1) + diffLast)/self.RSI_PERIODS
			else:
				self.averageGain = (self.averageGain*(self.RSI_PERIODS-1) + diffLast)/self.RSI_PERIODS
		#
		if self.averageLoss==0.0:
			self.RS=float('inf')
		else:
			self.RS=-self.averageGain/self.averageLoss

	#
	#
	#
	#
	def get_RSI(self,value,oldValue):
			'''calculates the relative index strength'''

			self.get_RS(value,oldValue)
			self.RSI=100. - 100./(1.0 + self.RS)
		#


	def get_RSI_from_history(self,stockHistory):
		'''it calculates the RSI from the history of prices
		decisions are taken on opening, but we calculate the RSI
		with the open and close
		'''

		if len(stockHistory.history)>1:
			yesterday=stockHistory.history[-2]
			today=stockHistory.history[-1]
		else:
			yesterday=None
			today=stockHistory.history[-1]
		#
		#

		if not yesterday==None:	
			#contribution to RSI from yesterday close-yesterday open
			value=float(yesterday['Close'])
			predecessor=float(yesterday['Open'])
			self.get_RSI(value,predecessor)
			#
			#
			#contribution to RSI from today open-yesterday close
			value=float(today['Open'])
			predecessor=float(yesterday['Close'])
			self.get_RSI(value,predecessor)
			#
			#
		else:
			predecessor=0.0
			value=float(today['Open'])
			self.get_RSI(predecessor,value)


	def make_decision(self,stockHistory,traderPosition):
		'''it makes a decision based on the RSI
			the decision is performed for every
			symbol followed by the trader'''


		for symbol in traderPosition.tradedSymbols:
			#
			#
			#
			#
			self.get_RSI_from_history(stockHistory)
			print 'the RSI at open is ',self.RSI
			print 'the number of periods here is ',self.nPeriods

			if self.RSI==0.:
				self.action['action']='sit'
				return self.action

			if self.RSI < self.buyAt:
				#
				if traderPosition.currentPosition == 'Short':
					self.action['action']='close'
				elif traderPosition.currentPosition == 'Long':
					self.action['action']='sit'
				elif traderPosition.currentPosition == 'Closed':
					self.action['action']='buy'
					self.action['buyQuantity']='max'
		#
			elif self.RSI > self.sellAt:
				#
				if traderPosition.currentPosition == 'Short':
					self.action['action']='sit'
				elif traderPosition.currentPosition == 'Long':
					self.action['action']='close'
				elif traderPosition.currentPosition == 'Closed':
					self.action['action']='sell'
					self.action['buyQuantity']='max'
		#
			else:
				self.action['action']='sit'

		
		return self.action

	





