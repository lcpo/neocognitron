import sLayer
import cLayer
import message

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

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
			output = self.sLayers[layer].propagate(output)
			output = self.cLayers[layer].propagate(output)
		if not train: 
			result = self.determineOutput(output.getPointsOnPlanes(0, 0))
			return result

	def determineOutput(self, out):
		print "---- DETERMINING OUTPUT -------"
		maxVal = 0
		index = -1
		for i in xrange(len(out)):
			print ALPHABET[i], str(out[i]) 
			if out[i] > maxVal:
				maxVal = out[i]
				index = i
		return index

	def trainLayer(self, layer, trainTemplates):
		self.sLayers[layer].train(trainTemplates)

