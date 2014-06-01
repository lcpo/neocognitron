import sLayer
import cLayer
import message

class Neocognitron(object):

	def __init__(self, init):

		self.numLayers = init.NUM_LAYERS
		self.sLayers = []
		self.cLayers = []
		self.init = init

		for layer in xrange(self.numLayers):
			self.sLayers.append(sLayer.SLayer(layer, init))
			self.cLayers.append(cLayer.CLayer(layer, init))

	def propagate(self, image, train):
		output = message.Message(1, self.init.INPUT_LAYER_SIZE)
		output.setPlaneOutput(0, image)
		for layer in xrange(self.numLayers):
			output = self.sLayers[layer].propagate(output, train)
			output = self.cLayers[layer].propagate(output)
		result = self.determineOutput(output.getPointsOnPlanes(0, 0))
		return result

	def determineOutput(out):
		maxVal = 0
		index = -1
		for i in xrange(len(out)):
			if out[i] > maxVal:
				maxVal = out[i]
				index = i
		return index