import numpy as np

class Message(object):

	numPlanes = 0
	size = 0
	outputs = None

	def __init__(self, planes, initSize):
		numPlanes = planes
		size = initSize
		outputs = np.empty((numPlanes, size, size))

	def setOneOutput(self, plane, x, y, val):
		outputs[plane][x][y] = val

	def getWindows(self, x, y, windowSize):
		output = np.empty((numPlanes, (pow(windowSize, 2))))
		for plane in xrange(numPlanes):
			output[plane] = getOneWindow(plane, x, y, windowSize)
		return output

	def getOneWindow(self, plane, x, y, windowSize):
		output = np.empty((pow(windowSize, 2)))
		if windowSize == size:
			for i in xrange(windowSize):
				for j in xrange(windowSize):	
					output.append(outputs[plane][i][j])
		else:
			startX = x - (windowSize/2)
			startY = y - (windowSize/2)
			endX = x + (windowSize/2)
			endY = y + (windowSize/2)
			for i in xrange(startX, endX+1):
				for j in xrange(startY, endY+1):
					output.append(outputs[plane][i][j])
		return output