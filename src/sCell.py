import numpy as np

class SCell(object): 

	def __init__(self, r):

		self.r = r

	def propagate(self, inputs, vInput, b, a):
		output = 0.0

		for cell in xrange(inputs.shape[0]):
			print a.shape
			print inputs.shape
			output += np.dot(a[cell], inputs[cell])

		denom = (r/r+1) * b * vInput

		output = (output/denom) - 1.0

		output = max(0.0, output)

		output *= r
		
		return output


