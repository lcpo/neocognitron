import os 
import numpy as np 
import cv2 as cv 

for here, subfolders, stuff in os.walk('.'):
	for folder in subfolders:
		for here2, subsubs, contents in os.walk('./' + folder):
			for content in contents:
				if content[0] != '.':
					img = cv.imread('./' + folder + '/' + content, flags=cv.CV_LOAD_IMAGE_GRAYSCALE)
					img2 = np.delete(img, 1, 0)
					cv.imwrite('./' + folder + '/' + content, img2)
