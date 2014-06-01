import cPickle as pickle
import random

class InitStruct(object):

	def __init__(self):

##########################################################################
#                        DON'T CHANGE THESE                              #
##########################################################################
		self.NUM_LAYERS = 4
		self.INPUT_LAYER_SIZE = 45
		
		
##########################################################################
#                              VARIABLE                                  #
##########################################################################		

		self.S_LAYER_SIZES = [19, 21, 13, 3]
		self.C_LAYER_SIZES = [21, 13, 7, 1]

		self.PLANES_PER_LAYER = [12, 38, 35, 26]

		self.S_WINDOW_SIZE = [3, 9, 12, 10]
		self.C_WINDOW_SIZE = [3, 9, 9, 5]

		self.S_COLUMN_SIZE = [3, 9, 9, 5]

		# Q -> speed of reinforcement 
		self.Q = [.1, 16, 16, 16]

		# R -> efficiency of inhibitory signals
		self.R = [4, 1.5, 1.5, 1.5]

		# C -> strength of the fixed excitatory connections for V cells 
		# monotonically decreasing in size of receptive field 
		self.C = [.6, .2, .06, .04]

		# D -> strength of the fixed excitatory connections for C cells 
		# monotonically decreasing in size of receptive field 
		self.D = [.6, .2, .06, .04]

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
		self.S_LAYER_SIZES = list()
		self.C_LAYER_SIZES = list()
		self.S_LAYER_SIZES.append(random.choice(self.LAYER_RANGE[0]))
		for i in xrange(1, 4):
			choice = random.choice(self.LAYER_RANGE[i])
			self.S_LAYER_SIZES.append(choice)
			self.C_LAYER_SIZES.append(choice)
		self.C_LAYER_SIZES.append(1)

		# Planes per Layer 
		for i in xrange(3):
			self.PLANES_PER_LAYER[i] = random.choice(self.PLANE_RANGE[i])

		# Window Size 
		for i in xrange(0, 4):
			self.S_WINDOW_SIZE[i] = random.choice(self.WINDOW_RANGE[i])
			self.C_WINDOW_SIZE[i] = random.choice(self.WINDOW_RANGE[i])
		
		# Column Size 
		for i in xrange(0, 4):
			self.S_COLUMN_SIZE[i] = random.choice(self.COLUMN_RANGE[i])

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
		self.C[3] = (1.0 - self.C[0] - self.C[1] - self.C[2])/2

		# D 
		self.D[0] = random.uniform(.4, .8)
		self.D[1] = random.uniform(.09 , (1.0 - self.D[0])/2)
		self.D[2] = random.uniform(.05, (1.0 - self.D[0] - self.D[1])/2)
		self.D[3] = (1.0 - self.D[0] - self.D[1] - self.D[2])/2




	def pickle(self, fileName):
		pickle.dump(self, open(fileName, 'wb'))

	def loadPickle(self, fileName):
		return pickle.load(open(fileName, 'rb'))
