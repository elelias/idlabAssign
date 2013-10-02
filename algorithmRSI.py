


class AlgorithmRSI:

	'''this class represents an algorithm that 
	takes the rsi into account to perform decisions'''

	def __init__(self,parameters):

		self.parameters=parameters
		self.action={}
		self.buyAt=parameters.get('buyAt',None)
		self.sellAt=parameters.get('sellAt',None)
		self.buyQuantity=parameters.get('buyQuantity',None)
		self.sellQuantity=parameters.get('sellQuantity',None)		

	def make_decision(self,stockHistory):
		'''it makes a decision based on the RSI'''

		if stockHistory.RSI==0:
			self.action['action']='sit'
			return self.action

		if stockHistory.RSI < self.buyAt:
			#
			self.action['action']='buy'
			self.action['buyQuantity']=self.buyQuantity

		elif stockHistory.RSI > self.sellAt:
			#
			self.action['action']='sell'
			self.action['sellQuantity']=self.sellQuantity

		else:
			self.action['action']='sit'
		return self.action




