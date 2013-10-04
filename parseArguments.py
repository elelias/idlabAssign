



def parse_arguments(parseList):

	'''it parses the arguments given 
	in the command line'''

	parseOK=True
	#
	#
	fileNames=[]
	if len(parseList)>1:
		fileNames.append(parseList[1])
		if len(parseList)>2:
			fileNames.append(parseList[2])
		else:
			print 'there is no dividends file'
	else:
		print 'there is no file to read'
		parseOK=False
	#


	return parseOK,fileNames