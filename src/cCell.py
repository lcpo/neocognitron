import numpy as np

class CCell(object): 

	def __init__(self, d):

		self.d = d

	def propagate(self, inputs, vInput):
		output = np.dot(self.d, inputs)

		output = max(0.0, output)
		output = output/(1 + output)

		return output
