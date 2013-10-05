
import matplotlib.pyplot as plt
import matplotlib.legend as lgnd

def process_performance(name,stockHistory,traderPosition,portfolioValues,plotParameters={}):
	




	for symbol,history in stockHistory.iteritems():
		#
		#
		valueList=portfolioValues[symbol]
		stockEvolution=[]
		for element in history.history:
			stockEvolution.append(1000.*float(element['Adj Close']))
		#
		#
		buys=[]
		#print the buys
		for element in traderPosition.actions:
			if element['action']=='buy':
				buys.append(element['PFValue'])
			else:
				buys.append(1000000)
		#
		sales=[]
		for element in traderPosition.actions:
			if element['action']=='sell':
				sales.append(element['PFValue'])
			else:
				sales.append(1000000)

		closes=[]

		for element in traderPosition.actions:
			if element['action']=='close':
				closes.append(element['PFValue']+10000)
			else:
				closes.append(1000000)



		print 'going to proess the performance of ',name
		p0,=plt.plot(valueList)
		p1,=plt.plot(stockEvolution)
		p2,=plt.plot(buys,'ro')
		p3,=plt.plot(sales,'ko')
		p4,=plt.plot(closes,'ws')	
		plt.legend([p0,p1,p2,p3,p4], ['RSI','SPY*1000','buys','sales','closes'],numpoints = 1,loc=9)			
		print 'adding label'
		plt.ylabel('value of portfolio in $')
		plt.xlabel('number of days')
		plt.ylim([0,300000])
		print 'showing...'
		#plt.show()
		plt.savefig('first.png')


