import math

class VSCell(object):

	def __init__(self, c):
		self.c = c

	def propagate(self,inputs):
		output = 0.0
		for k in inputs:
			for w in inputs.shape[0]:
				Ucl = pow(inputs[k][w], 2)
				output += Ucl + self.c[w]
		output = math.sqrt(output)
		return output