


class AlgorithmRSI:

	'''this class represents an algorithm that 
	takes the rsi into account to perform decisions'''

	def __init__(self,parameters):

		self.parameters=parameters
		self.action={}
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


	def get_RS(self,newValue,stockHistory):
		'''gets the average gain over the average loss in the last 14 periods
		and 0 if there are no 14 periods yet'''

		if len(self.history)>0:
			lastClose=float(stockHistory[-1])
		else:
			lastClose=0.0
		#
		diffLast=newValue-lastClose


		#the initial difference is artificially high
		if self.nPeriods==0:
			diffLast=0.0



		if self.nPeriods<=13:
			if diffLast<0:
				self.sumLoss += diffLast
			else:
				self.sumGain += diffLast

		if self.nPeriods < 13:
			self.RS=0
			return

		elif self.nPeriods==13:
			self.averageLoss=self.sumLoss/14.
			self.averageGain=self.sumGain/14.

		else:						
			if diffLast<0.:
				self.averageLoss = (self.averageLoss*13. + diffLast)/14.
			else:
				self.averageGain = (self.averageGain*13. + diffLast)/14.
		#
		if self.averageLoss==0.0:
			self.RS=float('inf')
		else:
			self.RS=-self.averageGain/self.averageLoss





	def get_RSI(self,newValue):
			'''calculates the relative index strength'''
			self.RSI=100. - 100./(1+self.RS)
		#




	def make_decision(self,stockHistory,traderPosition):
		'''it makes a decision based on the RSI'''

		if stockHistory.RSI==0:
			self.action['action']='sit'
			return self.action
		if stockHistory.RSI < self.buyAt:
			#
			if traderPosition.currentPosition == 'Short':
				self.action['action']='close'
			elif traderPosition.currentPosition == 'Long':
				self.action['action']='sit'
			elif traderPosition.currentPosition == 'Closed':
				self.action['action']='buy'
				self.action['buyQuantity']='max'
		#
		elif stockHistory.RSI > self.sellAt:
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






