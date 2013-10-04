



def invertFile(fileName,reversedName):

	
	f=open(fileName,'r')
	print f
	w=open(reversedName,'w')

	for line in f:
		print 'the line is ',line
		w.write(line)
		break
	f.close()

	f=open(fileName,'r')
	for num,line in enumerate(reversed(f.readlines())):
		#print 'the line is now ',line
		if num==45:
			break		
		w.write(line)

	f.close()
	w.close()


if __name__=='__main__':

	#invertFile('table.csv','orderedTable.csv')
	invertFile('dividends.csv','orderedDividends.csv')


