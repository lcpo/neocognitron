import numpy as np
import message
import random
import vsCell
import sCell
import trainer

class SLayer(object):

	def __init__(self, layer, initStruct):
		self.size = initStruct.S_LAYER_SIZES[layer]
		self.numPlanes = initStruct.PLANES_PER_LAYER[layer]
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
			prev = initStruct.PLANES_PER_LAYER[layer - 1]

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

	def propagate(self, inputs):
		output = message.Message(self.numPlanes, self.size)
		vOutput = np.empty((self.size, self.size))
		for x in xrange(self.size):
			for y in xrange(self.size):
				windows = inputs.getWindows(x, y, self.windowSize)
				vOutput[x][y] = self.vCells[x][y].propagate(windows)
				for plane in xrange(self.numPlanes):
					val = self.sCells[plane][x][y].propagate(windows, vOutput[x][y], self.b[plane], self.a[plane])
					output.setOneOutput(plane, x, y, val)
		# if train:
		# 	self.train(inputs, output, vOutput)
		# 	output = self.propagate(inputs, False)
		return output

	def seedPropagate(self, inputs):
		x = self.size/2
		y = x
		windows = inputs.getWindows(x, y, self.windowSize)
		vOutput = self.vCells[x][y].propagate(windows)
		output = np.empty((self.numPlanes))
		for plane in xrange(self.numPlanes):		
			sOutput = self.sCells[plane][x][y].propagate(windows, vOutput, self.b[plane], self.a[plane])
			output[plane] = sOutput
		return output, vOutput
			
	def adjustWeights(self, inputs, output, vOutput):
		weightLength = pow(self.windowSize, 2)
		x = self.size/2
		y = x
		for plane in xrange(self.numPlanes):
			delta = self.q * vOutput
			self.b[plane] += delta
			for ck in xrange(self.a[plane].shape[0]):
					prev = inputs.getOneWindow(ck, x, y, self.windowSize)
					for weight in xrange(weightLength):
						delta = self.q * self.c * prev[weight]
						self.a[plane][ck][weight] += delta

	def train(self, trainTemplates):
		for example in xrange(trainer.MAX_PER_PLANE):
			inputs = message.Message(self.numPlanes, self.windowSize)
			for plane in xrange(len(trainTemplates)):
				print plane, example
				inputs.setPlaneOutput(plane, trainTemplates[plane][example])
			output, vOutput = self.seedPropagate(inputs)
			self.adjustWeights(inputs, output, vOutput)


		


