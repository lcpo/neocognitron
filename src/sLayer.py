import numpy as np
import message
import random
import vsCell
import sCell

class SLayer(object):

	def __init__(self, layer, initStruct):
		self.size = initStruct.S_LAYER_SIZES[layer]
		self.numPlanes = initStruct.S_PLANES_PER_LAYER[layer]
		self.windowSize = initStruct.S_WINDOW_SIZE[layer]
		self.columnSize = initStruct.S_COLUMN_SIZE[layer]

		self.q = initStruct.Q[layer]
		self.r = initStruct.R[layer]
		self.c = initStruct.C[layer]

		self.sCells = np.empty((self.numPlanes, self.size, self.size), dtype=np.object)
		self.vCells = np.empty((self.size, self.size), dtype=np.object)

		prev = 0
		if layer == 0: 
			prev = 1
		else: 
			prev = initStruct.C_PLANES_PER_LAYER[layer - 1]

		self.initA(prev)
		self.initB()
		self.createCells()

	def createCells(self):
		for x in xrange(self.size):
			for y in xrange(self.size):				
				self.vCells[x][y] = vsCell.VSCell(self.c)
				for plane in xrange(self.numPlanes):
					self.sCells[plane][x][y] = sCell.SCell(self.r)

	def initA(self, prev):
		self.a = np.empty((self.numPlanes, prev, pow(self.windowSize, 2)))
		for k in xrange(self.numPlanes):
			for ck in xrange(prev):
				for w in xrange(pow(self.windowSize, 2)):
					self.a[k][ck][w] = random.random()*.4

	def initB(self):
		self.b = np.empty((self.numPlanes))
		for k in xrange(self.numPlanes):
			self.b[k] = 0.

	def propagate(self, inputs, train):
		output = message.Message(self.numPlanes, self.size)
		vOutput = np.empty((self.size, self.size))
		for x in xrange(self.size):
			for y in xrange(self.size):
				windows = inputs.getWindows(x, y, self.windowSize)
				self.vCells[x][y].propagate(windows)
				for plane in xrange(self.numPlanes):
					val = self.sCells[plane][x][y].propagate(windows, vOutput[x][y], self.b[plane], self.a[plane])
					output.setOneOutput(plane, x, y, val)
		if train:
			self.train(inputs, output, vOutput)
			output = self.propagate(inputs, False)
		return output

	def train(self, inputs, output, vOutput):
		weightLength = pow(self.windowSize, 2)
		representatives = output.getRepresentatives(self.columnSize)
		for plane in xrange(self.numPlanes):
			p = representatives[plane]
			delta = self.q * vOutput[p[0]][p[1]]
			b[plane] += delta
			for ck in self.a[plane].size:
				prev = inputs.getOneWindow(ck, p[0], p[1], self.windowSize)
				for weight in weightLength:
					delta = q * self.c[weight] * prev[weight]
					a[plane][ck][weight] += delta


