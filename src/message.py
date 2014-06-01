import numpy as np
import location

class Message(object):

	def __init__(self, planes, initSize):
		self.numPlanes = planes
		self.size = initSize
		self.outputs = np.empty((self.numPlanes, self.size, self.size))

	def setPlaneOutput(self, plane, toSet):
		self.outputs[plane] = toSet

	def setOneOutput(self, plane, x, y, val):
		self.outputs[plane][x][y] = val

	def getPointsOnPlanes(self, x, y):
		output = []
		for plane in xrange(self.numPlanes):
			output.append(self.outputs[plane][x][y])
		return output

	def getWindows(self, x, y, windowSize):
		output = np.empty((self.numPlanes, (pow(windowSize, 2))))
		for plane in xrange(self.numPlanes):
			output[plane] = self.getOneWindow(plane, x, y, windowSize)
		return output

	def getOneWindow(self, plane, x, y, windowSize):
		output = np.empty((pow(windowSize, 2)))
		if windowSize == self.size:
			count = 0 
			for i in xrange(windowSize):
				for j in xrange(windowSize):	
					output[count] = self.outputs[plane][i][j]
					count += 1
		else:
			startX = x - (windowSize/2)
			startY = y - (windowSize/2)
			endX = x + (windowSize/2)
			endY = y + (windowSize/2)
			count = 0
			for i in xrange(startX, endX):
				for j in xrange(startY, endY):
					try:
						output[count] = self.outputs[plane][i][j]
					except Exception:
						output[count] = 0.
					count += 1
		return output

	def getSquareWindows(self, x, y, windowSize):
		out = np.empty((self.numPlanes, windowSize, windowSize))
		for plane in xrange(self.numPlanes):
			out[plane] = self.getOneSquareWindow(plane, x, y, windowSize)
		return out

	def getOneSquareWindow(self, plane, x, y, windowSize):
		out = np.empty((windowSize, windowSize))
		if windowSize == self.size:
			for smallx in xrange(self.size):
				for smally in xrange(self.size):
					out[smallx][smally] = self.outputs[plane][smallx][smally]
		else:
			offset = (windowSize - 1)/2
			for smallx in xrange(x - offset, x + offset):
				for smally in xrange(y - offset, y + offset):
					try: 
						out[x-smallx+offset][y-smally+offset] = self.outputs[plane][smallx][smally]
					except Exception:
						out[x-smallx+offset][y-smally+offset] = 0.
		return out 

	def getLocationOfMax(self, sColumn, center, windowSize):
		maxL = None
		maxVal = 0
		for plane in xrange(sColumn.shape[0]):
			for x in xrange(sColumn.shape[1]):
				for y in xrange(sColumn.shape[2]):
					if sColumn[plane][x][y] > maxVal:
						maxL = location.Location(plane, x, y)
		offset = (windowSize - windowSize%2)/2
		if maxL != None:
			x, y = maxL.getPoint()
			maxL.setPoint(x+center[0]-offset, y+center[1]-offset)
		return maxL

	def getSingleOutput(self, location):
		return self.outputs[location.getPlane()][location.getX()][location.getY()]

	def getMaxPerPlane(self, plane, points):
		p = None
		maxVal = -float('inf') 
		for point in points:
			temp = point
			if temp == None: p = None
			elif temp.getPlane() == plane:				
				if self.getSingleOutput(temp) > maxVal:
					maxVal = self.getSingleOutput(temp)
					p = temp.getPoint()		
		return p

	def getRepresentatives(self, windowSize):
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
		for plane in xrange(self.numPlanes):
			reps.append(self.getMaxPerPlane(plane, points))
		return reps




