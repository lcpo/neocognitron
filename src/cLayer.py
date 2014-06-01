import numpy as np
import message
import cCell

class CLayer(object):

	def __init__(self, layer, initStruct):
		self.size = initStruct.C_LAYER_SIZES[layer]
		self.numPlanes = initStruct.C_PLANES_PER_LAYER[layer]
		self.windowSize = initStruct.C_WINDOW_SIZE[layer]

		self.cCells = np.empty((self.numPlanes, self.size, self.size), dtype=np.object)

		self.d = initStruct.D[layer]
		
		self.createCCells()

	def createCCells(self):
		for x in xrange(self.size):
			for y in xrange(self.size):
				for plane in xrange(self.numPlanes):
					self.cCells[plane][x][y] = cCell.CCell(self.d)

	def propagate(self, inputs):
		output = message.Message(self.numPlanes, self.size)
		for x in xrange(self.size):
			for y in xrange(self.size):
				windows = inputs.getWindows(x, y, self.windowSize)
				for plane in xrange(self.numPlanes):
					val = self.cCells[plane][x][y].propagate(windows, self.d[plane])
					output.setOneOutput(plane, x, y, val)

		return output