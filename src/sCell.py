import numpy as np

class SCell(object): 

	def __init__(self, r):

		self.r = r

	def propagate(self, inputs, vInput, b, a):
		output = 0.0
		
		for cell in xrange(inputs.shape[0]):
			output += np.dot(a[0], inputs[cell])

		denom = 1 + (self.r/self.r+1) * b * vInput
		
		output = (1 + output/denom) - 1.0

		output = max(0.0, output)

		output *= self.r

		return output


