
import matplotlib.pyplot as plt
import matplotlib.legend as lgnd

def process_performance(name,stockHistory,traderPosition,portfolioValues,plotParameters={}):
	


	#parse the plot paramters
	symbol=plotParameters.get('symbol','SPY')
	#
	plotSymbol=plotParameters.get('plotSymbol',True)
	plotBuys=plotParameters.get('plotBuys',True)
	plotSales=plotParameters.get('plotSales',True)
	plotCloses=plotParameters.get('plotCloses',True)
	numpoints=plotParameters.get('numpoints',1)
	location=plotParameters.get('position',9)
	plotName=plotParameters.get('plotName','unnamed.pdf')
	ymin=plotParameters.get('ymin',50000)
	ymax=plotParameters.get('ymax',300000)	

	#



	for symbol,history in stockHistory.iteritems():
		#
		#
		valueList=portfolioValues[symbol]
		stockEvolution=[]

		if plotSymbol:
			for element in history.history:
				stockEvolution.append(1000.*float(element['Close']))
		#
		#
		buys=[]		
		if plotBuys:
			for element in traderPosition.actions:
				if element['action']=='buy':
					buys.append(element['PFValue'])
				else:
					buys.append(1000000)
		#
		sales=[]
		if plotSales:
			for element in traderPosition.actions:
				if element['action']=='sell':
					sales.append(element['PFValue'])
				else:
					sales.append(1000000)

		closes=[]
		if plotCloses:
			for element in traderPosition.actions:
				if element['action']=='close':
					closes.append(element['PFValue']+5000)
				else:
					closes.append(1000000)
		#
		#
		#
		print ''
		print '=========================================='
		print 'going to process the performance of ',name
		#
		p0,=plt.plot(valueList)
		if plotSymbol:
			p1,=plt.plot(stockEvolution,label=symbol+'*1000',color='k')
		if plotBuys:
			p2,=plt.plot(buys,'ro',label='buys')
		if plotSales:
		 	p3,=plt.plot(sales,'ko',label='sales')
		if plotCloses:
			p4,=plt.plot(closes,'ws',label='closes')


		#plt.legend([p0,p1,p2,p3,p4], numpoints = 1,loc=9)			
		plt.legend(numpoints=numpoints,loc=location)
		#print 'adding label'
		plt.ylabel('value of portfolio in $')
		plt.xlabel('number of days')

		plt.ylim(ymin,ymax)
		#plt.xlim([2000,2500])				
		#print 'showing...'
		#plt.show()
		plt.savefig(plotName)
		plt.close()





def compare_performance(stockHistory,algorithmsDictionary,plotParameters={}):


	plotName=plotParameters.get('plotName','comparison.pdf')
	plotSymbol=plotParameters.get('plotSymbol',True)
	numpoints=plotParameters.get('numpoints',1)
	location=plotParameters.get('position',9)

	for symbol,history in stockHistory.iteritems():

		stockEvolution=[]

		if plotSymbol:
			for element in history.history:
				stockEvolution.append(1000.*float(element['Adj Close']))		

		p0,=plt.plot(stockEvolution,label=symbol+'*1000',color='k')		


		portfolioValuesList=[]

		for name,bundle in algorithmsDictionary.iteritems():

			#algorithm=bundle[0]
			#traderPosition=bundle[1]
			PFvalue=bundle[2]
			plt.plot(PFvalue[symbol],label=name)
		#
		plt.legend(numpoints=numpoints,loc=location)		
		plt.ylabel('value of portfolio in $')
		plt.xlabel('number of days')
		plt.ylim([0,300000])

		#plt.show()
		plt.savefig(plotName)
		plt.close()















