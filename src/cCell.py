import numpy as np

class CCell(object): 

	def __init__(self, d):

		self.d = d

	def propagate(self, inputs, vInput):
		d = numpy.empty((len(inputs)))
		d.fill(self.d)
		output = np.dot(d, inputs)

		output = max(0.0, output)
		output = output/(1 + output)

		return output
