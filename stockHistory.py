import sys
import math

class StockHistory:

	'''keeps track of the history and evolution of the stock values'''

	def __init__(self):
		#
		self.mean=0.0
		self.stddev=None
		#self.RSI=None
		#self.RS=0.0
		#self.nPeriods=0
		self.sumValues=0.0
		self.sumSquaredValues=0.0
		self.averageGain=0.0
		self.averageLoss=0.0
		self.sumGain=0.0
		self.sumLoss=0.0		
		self.history=[]
		self.stockPriceHistory=[]
	#
	def __repr__(self):

		print 'instance of StockHistory'
		print '   the current mean is ',self.mean
		print '   the current stddev is ',self.stddev
		print '   the current number of periods is ',self.nPeriods
		print '   the current RS is ',self.RS
		print '   the current RSI is ',self.RSI
		return ''

	def get_mean(self,newValue):
		'''gets the new value for the mean'''
		self.mean = (self.mean*self.nPeriods + newValue)/(self.nPeriods+1)

	def get_stddev(self,newValue):
		'''get the new standard deviation'''
		nPeriods=self.nPeriods+1
		self.sumSquaredValues+=newValue*newValue

		if nPeriods<2:
			self.stddev=0.0
		else:

			self.stddev=self.sumSquaredValues-nPeriods*self.mean*self.mean
			#
			self.stddev=math.sqrt(self.stddev/(nPeriods-1))


	def add_entry(self,entry):
		'''adds the value to the history and re-calculates the
		quantities'''

		if not type(entry)==dict:
			print 'the entry has to be a dictionary'
			assert False
		#

		self.history.append(entry) #ONE ENTRY PER DAY

		for price in ['Open','High','Low','Close']:

			value=float(entry[price])

			#obtain the relevant quantities
			self.get_mean(value)
			self.get_stddev(value)
			#self.get_RS(value)
			#self.get_RSI(value)

			#save the entry

			self.stockPriceHistory.append(value)
			self.nPeriods+=1



