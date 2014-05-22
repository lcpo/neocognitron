import sLayer
import cLayer

class Neocognitron(object):

	numLayers = 0
	sLayers = None
	cLayers = None

	def __init__(self, init):

		numLayers = init.NUM_LAYERS
		sLayers = []
		cLayers = []

		for layer in xrange(numLayers):
			sLayers.append(sLayer.SLayer(layer, init))
			cLayers.append(cLayer.CLayer(layer, init))

	def propagate(self, image, train):

		