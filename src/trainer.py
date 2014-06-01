import random
import cv2 as cv 
import neocognitron
import initStruct
import numpy as np

IMG_SIZE = 45
FILES_PER_CLASS = 55
TRAIN_PER_CLASS = 35
K_FOLD = 5
NUM_LOOPS = 5
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
PATH_TO_SAVED = '../saved/param/'
DATA_DIR = '../data/'


def train(init, loops):
	network = neocognitron.Neocognitron(init)
	trainFiles = random.sample(range(1, FILES_PER_CLASS), TRAIN_PER_CLASS)
	inputs = getInputs(trainFiles)
	for n in xrange(loops * len(inputs)):
			network.propagate(inputs[n % len(inputs)][0], True)
	return network

def crossVal(init, loops):
	numCorrect = 0
	numTotal = 0	
	filesPerFold = FILES_PER_CLASS/K_FOLD
	for k in xrange(K_FOLD):
		print 'FOLD NUM ' + str(k+1)
		network = neocognitron.Neocognitron(init)
		trainFiles = range(filesPerFold*k, filesPerFold*(k+1)) 
		trainInputs = getInputs(trainFiles)
		print 'TRAINING'
		for n in xrange(loops * len(trainInputs)):
			network.propagate(trainInputs[n % len(trainInputs)][0], True)
		print 'DONE TRAINING'
		validateFiles = list(set(range(1, FILES_PER_CLASS)).symmetric_difference(trainFiles))
		validateInputs = getInputs(validateFiles)
		print 'VALIDATING'
		for n in xrange(len(validateInputs)):
			guess = network.propagate(validateInputs[n][0], False)
			guess = ALPHABET[guess]
			if guess == validateInputs[n][1]: numCorrect += 1
			numTotal += 1
		print 'DONE VALIDATING'
	return 1.0 - float(numCorrect)/numTotal

def getInputs(trainFiles):
	inputs = []
	for letter in ALPHABET:
		for fileNum in trainFiles:
			if fileNum == 0: continue	
			numZeros = 3
			if fileNum/10 != 0:
				numZeros = 1
			else:
				numZeros = 2
			fileName = letter + '-' + '0'*numZeros + str(fileNum) + '.png'						
			img = cv.imread(DATA_DIR + letter+ '/' + fileName)
			img = np.delete(img, (1, 2), 2)			
			img = img.reshape((IMG_SIZE,IMG_SIZE))
			inputs.append((img, letter))
	random.shuffle(inputs)
	return inputs

def runParameterSearch():
	minError = 1.0
	init = initStruct.InitStruct()
	for i in xrange(1, 501):		
		print 'PARAM SEARCH NUM: ' + str(i)			
		init.randomize()			
		error = crossVal(init, NUM_LOOPS)
		print 'ERROR FOR NUM ' + str(i) + ' : ' + str(error)
		if error < minError:				
			minError = error
			print '--------NEW BEST ' + str(minError) + '----------'
			init.pickle(PATH_TO_SAVED + error + '.init')



def runTraining():
	init = initStruct.InitStruct()
	network = train(init, NUM_LOOPS)
	#save network ? 
	return network
					
