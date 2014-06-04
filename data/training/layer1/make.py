import numpy as np
import cv2 as cv 

train = np.empty((3, 3))
train.fill(255.)
train[0][0] = 0.
train[1][1] = 0.
train[1][2] = 0.
cv.imwrite('012.png', train)

