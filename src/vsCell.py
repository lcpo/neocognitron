import math

class VSCell(object):

	def __init__(self, c):
		self.c = c

	def propagate(self,inputs):
		output = 0.0
		for k in xrange(inputs.shape[0]):
			for w in xrange(inputs.shape[0]):
				Ucl = pow(inputs[k][w], 2)
				output += Ucl + self.c
		output = math.sqrt(output)
		return output