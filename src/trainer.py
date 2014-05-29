import random
import cv2 as cv 
import neocognitron
import initStruct

FILES_PER_CLASS = 55
TRAIN_PER_CLASS = 35
K_FOLD = 5
ALPHABET = ['ABCDEFGHIJKLMNOPQRSTUVWXYZ']

class Trainer(object):
	
	def __init__(self, dataDir, crossVal, outFile):
		self.data = dataDir
		self.crossVal = crossVal
		self.out = outFile

	def run(self, loops):
		#figure out init 
		init = initStruct.InitStruct()
		network = neocognitron.Neocognitron(init)
		trainFiles = random.sample(range(1, FILES_PER_CLASS), TRAIN_PER_CLASS)
		inputs = self.getInputs(trainFiles)
		for n in xrange(loops * len(inputs)):
				network.propagate(inputs[n % len(inputs)][0], True)

	def crossVal(self, loops):
		#figure out init 
		init = initStruct.InitStruct()
		for k in xrange(K_FOLD):
			network = neocognitron.Neocognitron(init)
			trainFiles = random.sample(range(1, FILES_PER_CLASS), TRAIN_PER_CLASS)
			inputs = self.getInputs(trainFiles)
			for n in xrange(loops * len(inputs)):
				network.propagate(inputs[n % len(inputs)][0], True)
			#get others and validate 




	def getInputs(self, trainFiles):
		inputs = []
		for letter in ALPHABET:
			for fileNum in trainFiles:
				numZeros = 3
				if fileName/10 != 0:
					numZeros = 1
				else:
					numZeros = 2
				fileName = letter + '-' + '0'*numZeros + fileNum + '.png'
				img = cv.imread(self.dataDir + letter+ '/' + fileName)
				inputs.append((img, letter))
		return random.shuffle(inputs)
					
