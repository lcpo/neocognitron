import numpy as np
import message
import random

class SLayer(object):

	def __init__(self, layer, initStruct):
		self.size = S_LAYER_SIZES[layer]
		self.numPlanes = initStruct.S_PLANES_PER_LAYER[layer]
		self.windowSize = initStruct.S_WINDOW_SIZE[layer]

		self.q = initStruct.Q[layer]
		self.r = initStruct.R[layer]
		self.c = initStruct.C[layer]

		self.sCells = np.empty((numPlanes, self.size, self.size))
		self.vCells = np.empty((self.size, self.size))

		prev = 0
		if layer == 0: 
			prev = 1
		else: 
			prev = initStruct.C_PLANES_PER_LAYER[layer - 1]

		initA(prev)
		initB()
		createCells(self.sCells)

	def createCells(self, sCells):
		for x in xrange(size):
			for y in xrange(size):
				self.vCells[x][y] = VSCell(self.c)
				for plane in xrange(numPlanes):
					sCells[plane][x][y] = SCell(self.r)

	def initA(self, prev):
		self.a = np.empty((self.numPlanes, prev, pow(self.size, 2)))
		for k in self.numPlanes:
			for ck in prev:
				for w in pow(self.size, 2):
					a[k][ck][w] = random.random()*.4

	def initB(self):
		self.b = np.empty((self.numPlanes))
		for k in self.numPlanes:
			b[k] = 0.

	def propagate(self, inputs):
		output = message.Message(numPlanes, self.size)
		vOutput = np.empty((self.size, self.size))
		for x in xrange(self.size):
			for y in xrange(self.size):
				windows = inputs.getWindows(x, y, windowSize)
				vCells[x][y].propagate(windows)
				for plane in xrange(numPlanes):
					val = self.sCells[plane][x][y].propagate(windows, a[plane])
					output.setOneOutput(plane, x, y, val)

		return output