import numpy as np
import cv2

cap = cv2.VideoCapture(0)

for i in range(1):
	return_value, image = cap.read()
	cv2.imwrite('opencv'+str(i)+'.png', image)
del(cap)
