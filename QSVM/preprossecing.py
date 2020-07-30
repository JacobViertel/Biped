# Imports PIL module  
from PIL import Image 
import matplotlib.pyplot as plt

import cv2
import numpy as np
from numpy import asarray
# open method used to open different extension image file  
try:  
    im6 = cv2.imread("6.png") 
    im9 = cv2.imread("9.png") 
except IOError: 
    pass
# This method will show image in any image viewer  
gray6 = cv2.cvtColor(im6, cv2.COLOR_BGR2GRAY)
gray9 = cv2.cvtColor(im9, cv2.COLOR_BGR2GRAY)
(thresh, blackAndWhiteImage6) = cv2.threshold(gray6, 127, 255, cv2.THRESH_BINARY)
(thresh, blackAndWhiteImage9) = cv2.threshold(gray9, 127, 255, cv2.THRESH_BINARY)
data6 = asarray(blackAndWhiteImage6)
data9 = asarray(blackAndWhiteImage9)
# Step 1 calc HR and VR
print("Step 1 calc HR and VR")
ri_px = 0
le_px = 0
up_px = 0
lo_px = 0
for i in range(gray6.shape[0]):
    for j in range(gray6.shape[1]):
        if data6[i][j] == 0:
            if j < (gray6.shape[1]/2)+25:
                le_px +=1
            elif j >= (gray6.shape[1]/2)+25:
                ri_px +=1
            if i < (gray6.shape[0]/2)-23:
                up_px +=1
            elif i >= (gray6.shape[0]/2)-23:
                lo_px +=1 

HR6 = float(le_px)/ri_px
VR6 = float(up_px)/lo_px 
# print("HR6: ", HR6)
# print("VR6: ", VR6)

ri_px = 0
le_px = 0
up_px = 0
lo_px = 0
for i in range(gray9.shape[0]):
    for j in range(gray9.shape[1]):
        if data9[i][j] == 0:
            if j < (gray9.shape[1]/2)+25:
                le_px +=1
            elif j >= (gray9.shape[1]/2)+25:
                ri_px +=1
            if i < (gray9.shape[0]/2)-23:
                up_px +=1
            elif i >= (gray9.shape[0]/2)-23:
                lo_px +=1  

HR9 = float(le_px)/ri_px
VR9 = float(up_px)/lo_px 

# Step 2 Linear mapping 
print("Step 2 Linear mapping")
v_61 = HR6*1.3-0.62
v_62 = VR6*0.95-0.42
print("v_61 = ", v_61)
print("v_62 = ", v_62)
v_91 = HR9*1.3-0.62
v_92 = VR9*0.95-0.42

# Step 3 Normalization 
print("Step 3 Normalization")
x_61 = v_61/(abs(v_61)+abs(v_62))
x_62 = v_62/(abs(v_61)+abs(v_62))
print("x_61 = ", x_61)
print("x_62 = ", x_62)
x_91 = v_91/(abs(v_91)+abs(v_92))
x_92 = v_92/(abs(v_91)+abs(v_92))

# Step 4 Trigonometric function
print("Step 4 Trigonometric function")
if x_61 > 0 and x_62 > 0 or x_61 > 0 and x_62 < 0:       #first quad and forth quad 
    theta_6 = np.arctan(x_62/x_61)
elif x_61 < 0 and x_62 > 0:     #second quad
    theta_6 = np.arccot(x_61/x_62)
elif x_61 < 0 and x_62 < 0:     #third quad 
    theta_6 = np.arctan(x_61/x_62)
else:
    print("Error with Step 4 Trigonometric function")
if x_91 > 0 and x_92 > 0 or x_91 > 0 and x_92 < 0:       #first quad and forth quad 
    theta_9 = np.arctan(x_92/x_91)
elif x_91 < 0 and x_92 > 0:     #second quad
    theta_9 = np.arccot(x_91/x_92)
elif x_91 < 0 and x_92 < 0:     #third quad 
    theta_9 = np.arctan(x_91/x_92)
else:
    print("Error with Step 4 Trigonometric function")
print(theta_6)
# plt.scatter(xyz[:,0], xyz[:,1])

plt.scatter(x_61, x_62,color='red')
plt.scatter(x_91, x_92,color='blue')
plt.title('Preprocessed data')
plt.xlabel('x_1')
plt.ylabel('x_2')
plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.show()