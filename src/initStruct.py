
class InitStruct(object):

	def __init__(self):
		NUM_LAYERS = 4

		S_LAYER_SIZES = [19, 21, 13, 3]
		C_LAYER_SIZES = [21, 13, 7, 1]

		S_PLANES_PER_LAYER = [12, 38, 35, 26]
		C_PLANES_PER_LAYER = [8, 19, 23, 26]

		S_WINDOW_SIZE = [3, 9, 12, 10]

		Q = []
		R = []
		C = []