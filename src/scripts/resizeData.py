import os 
import re
import cv2 as cv 

PATH_TO_DATA = '../../data/'

for folder, subfolders, contents in os.walk(PATH_TO_DATA):
	folderName = re.findall('/data/([A-Z])', folder)
	if len(folderName) != 0:
		folderName = folderName[0]
	else: continue
	for content in contents:
		img = cv.imread(PATH_TO_DATA + folderName + '/' + content)
		smallImg = cv.resize(img, (0,0), fx=0.05, fy=0.05) 
		cv.imwrite(PATH_TO_DATA + folderName + '/' + content, smallImg)
		
