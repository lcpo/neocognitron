import os
import re

PATH_TO_DATA = '../../data/'

for folder, subfolders, contents in os.walk(PATH_TO_DATA):
	folderName = re.findall('/data/([A-Z])', folder)
	if len(folderName) != 0:
		folderName = folderName[0]
	else: continue
	print folderName
	for content in contents:
		imageName = re.findall('img[0-9][0-9][0-9]-([0-9][0-9][0-9].png)', content)
		if len(imageName) != 0:
			imageName = imageName[0]
		else: continue
		print PATH_TO_DATA + folderName + '/' + folderName + '-' + imageName
		os.rename(PATH_TO_DATA + folderName + '/' + content, PATH_TO_DATA + folderName + '/' + folderName + '-' + imageName)

