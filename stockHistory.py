import sys
import math

class StockHistory:

	'''keeps track of the history and evolution of the stock values'''

	def __init__(self):
		#
		self.mean=0.0
		self.stddev=None
		self.RSI=None
		self.RS=0.0
		self.nPeriods=0
		self.sumValues=0.0
		self.sumSquaredValues=0.0
		self.averageGain=0.0
		self.averageLoss=0.0
		self.sumGain=0.0
		self.sumLoss=0.0		
		self.history=[]
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




	def get_RS(self,newValue):
		'''gets the average gain over the average loss in the last 14 periods
		and 0 if there are no 14 periods yet'''

		if len(self.history)>0:
			lastClose=float(self.history[-1]['Adj Close'])
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



	def add_entry(self,entry):
		'''adds the value to the history and re-calculates the
		quantities'''

		if not type(entry)==dict:
			print 'the entry has to be a dictionary'
			assert False
		#

		#get the adjusted close
		close=float(entry['Adj Close'])
		#obtain the relevant quantities
		self.get_mean(close)
		self.get_stddev(close)
		self.get_RS(close)
		self.get_RSI(close)
		#save the entry
		self.history.append(entry)
		self.nPeriods+=1



