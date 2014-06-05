import cPickle as pickle
import random
import math
import numpy as np

class InitStruct(object):

	def __init__(self):

##########################################################################
#                        DON'T CHANGE THESE                              #
##########################################################################
		# self.NUM_LAYERS = 4
		self.NUM_LAYERS = 3
		self.INPUT_LAYER_SIZE = 45
		
		
##########################################################################
#                              VARIABLE                                  #
##########################################################################		

		# self.S_LAYER_SIZES = [19, 21, 13, 3]
		# self.C_LAYER_SIZES = [21, 13, 7, 1]
		self.S_LAYER_SIZES = [19, 21, 13]
		self.C_LAYER_SIZES = [21, 13, 1]

		# self.PLANES_PER_LAYER = [12, 38, 35, 26]
		self.PLANES_PER_LAYER = [12, 28, 26]

		self.S_WINDOW_SIZE = [3, 9, 20]
		self.C_WINDOW_SIZE = [3, 9, 9]

		self.S_COLUMN_SIZE = [3, 9, 9, 5]

		# Q -> speed of reinforcement 
		self.Q = [5, 10, 10, 16]

		# R -> efficiency of inhibitory signals
		self.R = [4, 1.5, 1.5, 1.5]

		self.gamma = [.11, .42, .06]
		self.delta = [.49, .87, .52]
		self.delta_bar = [.39, .68, .39]

		self.generateC()
		self.generateD()

		# C -> strength of the fixed excitatory connections for V cells 
		# monotonically decreasing in size of receptive field 
		# self.C = [.6, .2, .06, .04]
		# self.C = [.6, .24, .06]

		# D -> strength of the fixed excitatory connections for C cells 
		# monotonically decreasing in size of receptive field 
		# self.D = [.6, .2, .06, .04]
		# self.D = [.6, .24, .06]

	def generateC(self):	
		self.C = []
		self.C.append(self.generateMonotonic(self.gamma[0], self.S_WINDOW_SIZE[0], 1, True))
		for i in xrange(1, self.NUM_LAYERS):
			self.C.append(self.generateMonotonic(self.gamma[i], self.S_WINDOW_SIZE[i], self.PLANES_PER_LAYER[i-1], True))

	def generateD(self):	
		self.D = []
		for i in xrange(self.NUM_LAYERS):
			self.D.append(self.generateMonotonic(self.delta[i], self.C_WINDOW_SIZE[i], self.PLANES_PER_LAYER[i], False))
			for w in xrange(self.D[i].shape[0]):
				self.D[i][w] = self.D[i][w]*self.delta_bar[i]

	def distance(self, a, b):
		d = 0
		d += pow(a[0] - b[0], 2)
		d += pow(a[1] - b[1], 2)
		d = math.sqrt(d)
		return d

	def generateMonotonic(self, base, size, planes, norm):	
		output = np.empty((pow(size, 2)))
		center = (float(size) - 1)/2
		center = (center, center)
		index = 0
		for x in xrange(size):
			for y in xrange(size):
				output[index] = pow(base, self.distance(center, (x, y)))
				index += 1
		if norm:
			total = 0
			for w in xrange(output.shape[0]):
				total += output[w]
			mult = float(1)/(planes * total)
			for w in xrange(output.shape[0]):
				output[w] = output[w]*mult
		return output


	def makeRanges(self):
		try: 
			self.LAYER_RANGE != None
		except AttributeError:
			self.LAYER_RANGE = [range(15, 36), range(15, 36), range(10, 21), range(3, 11)]
			self.PLANE_RANGE = [range(5, 16), range(25, 46), range(25, 46)]
			self.WINDOW_RANGE = [range(2, 6), range(5, 13), range(9, 16), range(9, 16)]
			self.COLUMN_RANGE = [range(2, 6), range(5, 13), range(9, 16), range(3, 11)]
			self.Q_RANGE = [range(5, 16), range(5, 21), range(5, 21)]


	def randomize(self):

		self.makeRanges()

		# Layer sizes
		# self.S_LAYER_SIZES = list()
		# self.C_LAYER_SIZES = list()
		# self.S_LAYER_SIZES.append(random.choice(self.LAYER_RANGE[0]))
		# for i in xrange(1, 4):
		# 	choice = random.choice(self.LAYER_RANGE[i])
		# 	self.S_LAYER_SIZES.append(choice)
		# 	self.C_LAYER_SIZES.append(choice)
		# self.C_LAYER_SIZES.append(1)

		# Planes per Layer 
		# for i in xrange(3):
		# 	self.PLANES_PER_LAYER[i] = random.choice(self.PLANE_RANGE[i])

		# Window Size 
		# for i in xrange(0, 4):
		# 	self.S_WINDOW_SIZE[i] = random.choice(self.WINDOW_RANGE[i])
		# 	self.C_WINDOW_SIZE[i] = random.choice(self.WINDOW_RANGE[i])
		
		# Column Size 
		# for i in xrange(0, 4):
		# 	self.S_COLUMN_SIZE[i] = random.choice(self.COLUMN_RANGE[i])

		# Q 
		self.Q[0] = random.uniform(.05, .75)
		for i in xrange(1, 4):
			self.Q[i] = random.choice(self.Q_RANGE[i-1])

		# R 
		self.R[0] = random.choice(range(2, 6))
		self.R[1] = random.uniform(.1, .9)*2
		self.R[2] = max(random.uniform(.1, .9)*2, self.R[1])
		self.R[3] = max(random.uniform(.1, .9)*2, self.R[1])

		# C 
		self.C[0] = random.uniform(.4, .8)
		self.C[1] = random.uniform(.09 , (1.0 - self.C[0])/2)
		self.C[2] = random.uniform(.05, (1.0 - self.C[0] - self.C[1])/2)
		# self.C[3] = (1.0 - self.C[0] - self.C[1] - self.C[2])/2

		# D 
		self.D[0] = random.uniform(.4, .8)
		self.D[1] = random.uniform(.09 , (1.0 - self.D[0])/2)
		self.D[2] = random.uniform(.05, (1.0 - self.D[0] - self.D[1])/2)
		# self.D[3] = (1.0 - self.D[0] - self.D[1] - self.D[2])/2




	def pickle(self, fileName):
		pickle.dump(self, open(fileName, 'wb'))

	def loadPickle(self, fileName):
		return pickle.load(open(fileName, 'rb'))
