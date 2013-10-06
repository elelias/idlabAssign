
from applyStopLoss import apply_STOPLOSS

class AlgorithmRSI:

	'''this class represents an algorithm that 
	takes the rsi into account to perform decisions'''

	def __init__(self,parameters):

		self.parameters=parameters
		self.RSI_PERIODS=parameters['RSI_PERIODS']
		self.action={}
		self.averageGain={}
		self.averageLoss={}
		self.sumGain={}
		self.sumLoss={}		
		self.RSI={}
		self.RS={}
		self.nPeriods=0
		self.buyAt=parameters.get('buyAt',None)
		self.sellAt=parameters.get('sellAt',None)
		self.buyQuantity=parameters.get('buyQuantity',None)
		self.sellQuantity=parameters.get('sellQuantity',None)
		self.STOP_LOSS=parameters['stop_loss']
		self.VERBOSE=parameters.get('VERBOSE',False)


	#
	#
	#
	#




	def get_RS(self,newValue,oldValue,symbol):
		'''gets the average gain over the average loss in the last RSI_PERIODS 
		periods and 0 if there are no 14 periods yet.
		Values at Open and Close are considered for the calculation,
		even though that only values at Open are considered for trading.
		'''
		#
		#
		if self.VERBOSE:
			print '    Inside get_RS:'

		diffLast=newValue-oldValue
		#
		#
		self.nPeriods+=1
		#
		#
		#the initial difference is artificially high
		if self.nPeriods==1:
			diffLast=0.0
			diffNeg=0.0
			diffPos=0.0
		#
		#
		#
		if self.nPeriods <= self.RSI_PERIODS:
			if diffLast<0:
				diffPos=0.0
				diffNeg=diffLast
			else:
				diffPos=diffLast
				diffNeg=0.0

			if symbol in self.sumLoss:
				self.sumLoss[symbol] += diffNeg
				self.sumGain[symbol] += diffPos
			else:
				self.sumLoss[symbol] = diffNeg
				self.sumGain[symbol] = diffPos
		#
		#
		if self.nPeriods < self.RSI_PERIODS:
			#
			#
			self.RS[symbol]=0.0
			return
		#
		#
		elif self.nPeriods == self.RSI_PERIODS:


			self.averageLoss[symbol]=self.sumLoss[symbol]/self.RSI_PERIODS
			self.averageGain[symbol]=self.sumGain[symbol]/self.RSI_PERIODS
		#
		#
		else:						
			#more than nPeriods
			#
			if diffLast<0.:
				diffNeg=diffLast
				diffPos=0.0
			else:
				diffPos=diffLast
				diffNeg=0.0


			if self.VERBOSE:
				print '       old averageLoss = ',self.averageLoss[symbol]
				print '       old averageGain = ',self.averageGain[symbol]
				print '       diffLast is ',diffLast
				print '       diffPos  is ',diffPos
				print '       diffNeg  is ',diffNeg

			self.averageLoss[symbol] = (self.averageLoss[symbol]*(self.RSI_PERIODS-1) + diffNeg)/self.RSI_PERIODS
			self.averageGain[symbol] = (self.averageGain[symbol]*(self.RSI_PERIODS-1) + diffPos)/self.RSI_PERIODS			

			if self.VERBOSE:

				print '       the new average Loss is ',self.averageLoss[symbol]
				print '       the new average Gain is ',self.averageGain[symbol]				

		#
		#
		if self.averageLoss[symbol]==0.0:
			self.RS[symbol]=float('inf')
		else:
			self.RS[symbol]=-self.averageGain[symbol]/self.averageLoss[symbol]

	#
	#
	#
	#
	#
	#
	#
	def get_RSI(self,value,oldValue,symbol):
			'''calculates the relative index strength 
			given a new value, for which it first 
			needs to know the RS'''
			#
			self.get_RS(value,oldValue,symbol)
			self.RSI[symbol]=100. - 100./(1.0 + self.RS[symbol])
			if self.VERBOSE:
				print '   with RS =',self.RS[symbol]
				print '   the RSI is = ',self.RSI[symbol]
			#
		#
	#
	#
	#
	#

	def get_RSI_from_history(self,stockHistory,symbol):
		'''it calculates the RSI from the history of prices.
		decisions are taken on opening, but we calculate the RSI
		with the open and close
		'''


		if len(stockHistory[symbol].history)>1:
			yesterday=stockHistory[symbol].history[-2]
			today=stockHistory[symbol].history[-1]
		else:
			yesterday=None
			today=stockHistory[symbol].history[-1]
		#
		#

		if not yesterday==None:	
			#contribution to RSI from yesterday close-yesterday open


			value=float(yesterday['Close'])
			predecessor=float(yesterday['Open'])
			if self.VERBOSE:
				print '    value at Close yesterday ',value
				print '    value at Open  yesterday ',predecessor

			self.get_RSI(value,predecessor,symbol)
			#
			#
			#contribution to RSI from today open-yesterday close
			value=float(today['Open'])
			predecessor=float(yesterday['Close'])

			if self.VERBOSE:
				print '    value at Open today ',value
				print '    value at Close yesterday ',predecessor			

			self.get_RSI(value,predecessor,symbol)				
			#
			#
		else:
			predecessor=0.0
			value=float(today['Open'])
			self.get_RSI(predecessor,value,symbol)
	#
	#
	#
	#
	#
	def make_decision(self,stockHistory,symbol,traderPosition):
		'''it makes a decision based on the RSI.
			the decision is performed for every
			symbol followed by the trader'''
		#
		#
		if self.VERBOSE:
			print
			print 'welcome to the decision making in RSI algorithm '

		if self.STOP_LOSS:
			stopLoss=apply_STOPLOSS(traderPosition.PFValue,traderPosition.PFValue_LastAction)			
			if stopLoss:
				if traderPosition.currentPosition[symbol]!= 'Closed':
					if self.VERBOSE:
						print '   the loss is above 10%'
						print '   the last PF value is ',traderPosition.PFValue_LastAction
						print '   and currently the PF is worth ',traderPosition.PFValue
					self.action['action']='close'
					return self.action
				#
			else:
				pass


		#
		self.get_RSI_from_history(stockHistory,symbol)
		#
		#
		#
		RSI=self.RSI[symbol]
		if self.VERBOSE:
			print '    the RSI is ',RSI
		#
		#
		if symbol in traderPosition.currentPosition:
			currentPosition=traderPosition.currentPosition[symbol]

		#
		#
		#
		if RSI==0.:
			self.action['action']='sit'

			if self.VERBOSE:
				print '    No RSI, leaving...bye'
			return self.action

		if RSI < self.buyAt:
			#
			if currentPosition == 'Short':
				self.action['action']='close'
			elif currentPosition == 'Long':
				self.action['action']='sit'
			elif currentPosition == 'Closed':
				self.action['action']='buy'
				self.action['buyQuantity']='max'
			else:
				print 'WARNING'
				print 'the trader position is uknown'
				raw_input('press to continue if OK')
	#
		elif RSI > self.sellAt:
			#
			if currentPosition == 'Short':
				self.action['action']='sit'
			elif currentPosition == 'Long':
				self.action={}
				self.action['action']='close'
			elif currentPosition == 'Closed':
				self.action['action']='sell'
				self.action['sellQuantity']='max'

	#
		else:
			self.action['action']='sit'

		if self.VERBOSE:
			print '    the decision was to ',self.action['action']
			print '    the whole dict is ',self.action
		
		return self.action

	





