import random
import cv2 as cv 
import neocognitron

FILES_PER_CLASS = 55
TRAIN_PER_CLASS = 35
K_FOLD = 5
ALPHABET = ['ABCDEFGHIJKLMNOPQRSTUVWXYZ']

class Trainer(object):
	
	def __init__(self, dataDir, crossVal, outFile):
		self.data = dataDir
		self.crossVal = crossVal
		self.out = outFile

	def train(self, init, loops):
		network = neocognitron.Neocognitron(init)
		trainFiles = random.sample(range(1, FILES_PER_CLASS), TRAIN_PER_CLASS)
		inputs = self.getInputs(trainFiles)
		for n in xrange(loops * len(inputs)):
				network.propagate(inputs[n % len(inputs)][0], True)
		return network

	def crossVal(self, init, loops):
		numCorrect = 0
		numTotal = 0	
		filesPerFold = FILES_PER_CLASS/K_FOLD
		for k in xrange(K_FOLD):			
			network = neocognitron.Neocognitron(init)
			trainFiles = range(filesPerFold*k, filesPerFold*(k+1)) 
			trainInputs = self.getInputs(trainFiles)
			for n in xrange(loops * len(trainInputs)):
				network.propagate(trainInputs[n % len(trainInputs)][0], True)
			validateFiles = list(set(range(1, FILES_PER_CLASS)).symmetric_difference(trainFiles))
			validateInputs = self.getInputs(validateFiles)
			for n in xrange(len(validateInputs)):
				guess = network.propagate(validateInputs[n][0], False)
				guess = ALPHABET[guess]
				if guess == validateInputs[n][1]: numCorrect += 1
				numTotal += 1
		return float(numCorrect)/numTotal

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
					
