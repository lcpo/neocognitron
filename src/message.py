import numpy as np
import location

class Message(object):

	def __init__(self, planes, initSize):
		self.numPlanes = planes
		self.size = initSize
		self.outputs = np.empty((numPlanes, size, size))

	def setPlaneOutput(plane, outputs):
		outputs[plane] = outputs

	def setOneOutput(self, plane, x, y, val):
		outputs[plane][x][y] = val

	def getPointsOnPLanes(x, y):
		output = []
		for plane in xrange(self.numPlanes):
			output.append(self.outputs[plane][x][y])
		return output

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

	def getSquareWindows(x, y, windowSize):
		out = np.empty((self.numPlanes, windowSize, windowSize))
		for plane in numPlanes:
			out[plane] = self.getOneSquareWindow(plane, x, y, windowSize)
		return out

	def getOneSquareWindow(plane, x, y, windowSize):
		out = np.empty((windowSize, windowSize))
		if windowSize = self.size:
			for smallx in xrange(self.size):
				for smally in xrange(self.size):
					out[smallx][smally] = self.outputs[plane][smallx][smally]
		else:
			offset = (windowSize - 1)/2
			for smallx in xrange(self.size - offset):
				for smally in xrange(self.size - offset):
					out[x-smallx+offset][y-smally+offset] = outputs[plane][smallx][smally]
		return out 

	def getLocationOfMax(sColumn, center, windowSize):
		maxL = None
		maxVal = 0
		for plane in xrange(sColumn.shape[0]):
			for x in xrange(sColumn.shape[1]):
				for y in xrange(sColumn.shape[2]):
					if sColumn[plane][x][y] > maxVal:
						maxL = location.Location(plane, x, y)
		return maxL

	def getSingleOutput(location):
		return self.outputs[location.getPlane()][location.getX()][location.getY()]

	def getMaxPerPlane(plane, points):
		p = None
		maxVal = 0 
		for point in points:
			temp = point
			if temp == None: p = None
			elif temp.getPlane() == plane:
				if self.getSingleOutput(temp) > maxVal:
					maxVal = self.getSingleOutput(temp)
					p = temp.getPoint()
		return p

	def getRepresentatives(windowSize):
		points = []
		offset = (windowSize - 1)/2
		if windowSize == self.size:
			sColumn = self.getSquareWindows(self.size/2, self.size/2, windowSize)
			temp = self.getLocationOfMax(sColumn, (self.size/2, self.size/2), windowSize)
			points.append[temp]
		else:
			for x in xrange(self.size-offset):
				for y in xrange(self.size - offset):
					sColumn = self.getSquareWindows(x, y, windowSize)
					temp = self.getLocationOfMax(sColumn, (x, y), windowSize)
					if temp is not None and temp not in points:
						points.append(temp)

		reps = []
		for plane in self.numPlanes:
			reps.append(self.getMaxPerPlane(plane, points))
		return reps




