import numpy as np
import message

class CLayer(object):

	def __init__(layer, initStruct):
		self.size = C_LAYER_SIZES[layer]
		self.numPlanes = initStruct.C_PLANES_PER_LAYER[layer]
		self.windowSize = initStruct.C_WINDOW_SIZE[layer]

		self.cCells = np.empty((numPlanes, size, size))

		self.d = initStruct.D[layer]
		
		createCCells(self.cCells):

	def createCCells(cCells):
		for x in xrange(size):
			for y in xrange(size):
				for plane in xrange(numPlanes):
					cCells[plane][x][y] = CCell(d)

	def propagate(inputs):
		output = message.Message(numPlanes, size)
		for x in xrange(size):
			for y in xrange(size):
				windows = inputs.getWindows(x, y, windowSize)
				for plane in xrange(numPlanes):
					val = cCells[plane][x][y].propagate(windows, self.d[plane])
					output.setOneOutput(plane, x, y, val)

		return output