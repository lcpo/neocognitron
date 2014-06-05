import math

class VSCell(object):

	def __init__(self, c):
		self.c = c

	def propagate(self,inputs):
		output = 0.0
		for k in xrange(inputs.shape[0]):
			for w in xrange(inputs[0].shape[0]):
				if inputs[k][w] == float('inf'):
					print 'AQUIIIII'
				inputs[k][w] = pow(inputs[k][w], 2)				
				output += inputs[k][w] * self.c[w]
		output = math.sqrt(output)
		if output == float('inf'):
			print 'HERE'
		return output