


def apply_STOPLOSS(newValue,oldValue,parameters={}):
	'''it applies a stop loss order'''

	maxLoss=parameters.get('maxLoss',0.1)

	if oldValue==0.0:
		return False
		
	if (oldValue-newValue)/oldValue > 0.1:
		return True

