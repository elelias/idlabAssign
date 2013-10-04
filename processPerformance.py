
import matplotlib.pyplot as plt


def process_performance(name,stockHistory,valueDict):
	

	for symbol,history in stockHistory.iteritems():
		#
		#
		valueList=valueDict[symbol]
		stockEvolution=[]
		for element in history.history:
			stockEvolution.append(1000.*float(element['Adj Close']))
		#
		#
		#
		print 'going to proess the performance of ',name
		t=plt.plot(valueList)
		plt.plot(stockEvolution)
		print 'adding label'
		plt.ylabel('value of portfolio')
		plt.xlabel('number of days')
		print 'showing...'
		#plt.show()
		plt.savefig('first.png')


