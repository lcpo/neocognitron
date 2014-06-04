import random
import cv2 as cv 
import neocognitron
import initStruct
import numpy as np
import message
import os

IMG_SIZE = 45
FILES_PER_CLASS = 55
TRAIN_PER_CLASS = 35
K_FOLD = 5
NUM_LOOPS = 2
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
PATH_TO_SAVED = '../saved/param/'
DATA_DIR = '../data/'
TRAIN_DATA_DIR = '../data/training/'
MAX_PER_PLANE = 7
ON = 0.
OFF = 255.


def train(init):
	network = neocognitron.Neocognitron(init)
	for layer in xrange(init.NUM_LAYERS):
		trainTemplates = []
		for plane in xrange(init.PLANES_PER_LAYER[layer]):
			trainTemplates.append(getTrainFile(init, layer, plane))
		print "TRAINING LAYER " + str(layer + 1)
		network.trainLayer(layer, trainTemplates)
	return network


def getTrainFile(init, layer, plane):
	imageSize = init.S_WINDOW_SIZE[layer]
	layer = layer + 1
	plane = plane + 1
	output = []
	path = TRAIN_DATA_DIR + 'layer' + str(layer) + '/' + str(plane) + '/'
	for folder, subfolders, contents in os.walk(path):
		for content in contents:
			if not content[0] == '.':
				img = cv.imread(path + content, flags=cv.CV_LOAD_IMAGE_GRAYSCALE)
				for x in xrange(img.shape[0]):
					for y in xrange(img.shape[1]):
						if img[x][y] == OFF: img[x][y] == ON
						if img[x][y] == ON: img[x][y] == OFF
				output.append(img)
	return output


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
			if ((n+1)%10 == 0): print '\tTRAINED ' + str(n+1) + ' of ' + str(loops * len(trainInputs))
		print 'DONE TRAINING'
		validateFiles = list(set(range(1, FILES_PER_CLASS)).symmetric_difference(trainFiles))
		validateInputs = getInputs(validateFiles)
		print 'VALIDATING'
		for n in xrange(len(validateInputs)):
			guess = network.propagate(validateInputs[n][0], False)
			guess = ALPHABET[guess]
			print '\t=> ' + str(guess)
			print '\t<= ' + str(validateInputs[n][1])
			if guess == validateInputs[n][1]: numCorrect += 1
			numTotal += 1
		print 'DONE VALIDATING K=' + str(k+1)
		print 'NUM CORRECT: ' + str(numCorrect)
		print 'OF ' + str(numTotal)
		print 'CURRENT PERCENTAGE: ' + str(float(numCorrect)/numTotal)
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
			img = cv.imread(DATA_DIR + letter+ '/' + fileName, flags=cv.CV_LOAD_IMAGE_GRAYSCALE)
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

def validate(network):
	numCorrect = 0
	numTotal = 0
	validateInputs = getInputs(range(FILES_PER_CLASS))
	print 'TESTING'
	for n in xrange(len(validateInputs)):
			guess = network.propagate(validateInputs[n][0], False)
			guess = ALPHABET[guess]			
			print '\t<= ' + str(validateInputs[n][1])
			print '\t=> ' + str(guess)
			if guess == validateInputs[n][1]: numCorrect += 1
			numTotal += 1
			print 'NUM CORRECT: ' + str(numCorrect)
			print 'OF ' + str(numTotal)
			print 'CURRENT PERCENTAGE: ' + str(float(numCorrect)/numTotal)



def runTraining():
	init = initStruct.InitStruct()
	network = train(init)
	#save network ? 
	return network
					
