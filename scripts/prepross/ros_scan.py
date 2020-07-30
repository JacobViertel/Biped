import cv2
import numpy as np
import utlis
# from PIL import Image 
import matplotlib.pyplot as plt
import csv
from numpy import asarray
import math
import pandas as pd
from subprocess import call
import sys


########################################################################
webCamFeed = True
pathImage = "/home/biped/catkin_ws/src/jacob/scripts/prepross/scan.jpg"
heightImg = 640
widthImg  = 480

cap = cv2.VideoCapture(0)
cap.set(10,0.5)
for i in range(1):
	return_value, img = cap.read()
	cv2.imwrite("/home/biped/catkin_ws/src/jacob/scripts/prepross/webcam_img.png", img)
del(cap)
########################################################################

# utlis.initializeTrackbars()
count=0

# img = cv2.imread(pathImage)
img = cv2.resize(img, (widthImg, heightImg)) # RESIZE IMAGE
imgBlank = np.zeros((heightImg,widthImg, 3), np.uint8) # CREATE A BLANK IMAGE FOR TESTING DEBUGING IF REQUIRED
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # CONVERT IMAGE TO GRAY SCALE
imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1) # ADD GAUSSIAN BLUR
# thres=utlis.valTrackbars() # GET TRACK BAR VALUES FOR THRESHOLDS
imgThreshold = cv2.Canny(imgBlur,152,225) # APPLY CANNY BLUR
kernel = np.ones((5, 5))
imgDial = cv2.dilate(imgThreshold, kernel, iterations=2) # APPLY DILATION
imgThreshold = cv2.erode(imgDial, kernel, iterations=1)  # APPLY EROSION
## FIND ALL COUNTOURS
imgContours = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
imgBigContour = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
pts, contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # FIND ALL CONTOURS
cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10) # DRAW ALL DETECTED CONTOURS
# FIND THE BIGGEST COUNTOUR
biggest, maxArea = utlis.biggestContour(contours) # FIND THE BIGGEST CONTOUR
if biggest.size != 0:
    biggest=utlis.reorder(biggest)
    cv2.drawContours(imgBigContour, biggest, -1, (0, 255, 0), 20) # DRAW THE BIGGEST CONTOUR
    imgBigContour = utlis.drawRectangle(imgBigContour,biggest,2)
    pts1 = np.float32(biggest) # PREPARE POINTS FOR WARP
    pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
    #REMOVE 20 PIXELS FORM EACH SIDE
    imgWarpColored=imgWarpColored[20:imgWarpColored.shape[0] - 20, 20:imgWarpColored.shape[1] - 20]
    imgWarpColored = cv2.resize(imgWarpColored,(widthImg,heightImg))
    # APPLY ADAPTIVE THRESHOLD
    imgWarpGray = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)
    imgAdaptiveThre= cv2.adaptiveThreshold(imgWarpGray, 255, 1, 1, 7, 2)
    imgAdaptiveThre = cv2.bitwise_not(imgAdaptiveThre)
    imgAdaptiveThre=cv2.medianBlur(imgAdaptiveThre,3)
    cv2.imwrite('/home/biped/catkin_ws/src/jacob/scripts/prepross/blue_scaned.png',imgWarpColored)
    # Image Array for Display
    imageArray = ([img,imgGray,imgThreshold,imgContours],
                  [imgBigContour,imgWarpColored, imgWarpGray,imgAdaptiveThre])
else:
    imageArray = ([img,imgGray,imgThreshold,imgContours],
                  [imgBlank, imgBlank, imgBlank, imgBlank])
    print("Set Threshold lower !")

grayImage = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
(thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
# cropped = blackAndWhiteImage[ y-start:y-end , x-start:x-end ]
y_start = int(blackAndWhiteImage.shape[0]/2*0.18)
y_end = int(blackAndWhiteImage.shape[0]/2*1.83)
x_start = int(blackAndWhiteImage.shape[1]/2*0.5)
x_end = int(blackAndWhiteImage.shape[1]/2*1.5)
cropped = blackAndWhiteImage[y_start:y_end, x_start:x_end]
cv2.imwrite('/home/biped/catkin_ws/src/jacob/scripts/prepross/cropped.png',cropped)
data = asarray(cropped)
# Step 1 calc HR and VR
print("Step 1 calc HR and VR")
ri_px = 0
le_px = 0
up_px = 0
lo_px = 0
most_left = data.shape[1]
most_right = 0
upperst = data.shape[0]
lowest = 0

for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        if data[i][j] == 0:
            if most_left > j:
                most_left = j
            if most_right < j:
                most_right = j
            if upperst > i:
                upperst = i
            if lowest < i:
                lowest = i
print('most_left ', most_left)
print('most_right ', most_right)
print('upperst ',upperst)
print('lowest ', lowest)

for i in range(lowest-upperst):
    for j in range(most_right-most_left):
        if data[upperst+i][most_left+j] == 0:
            if j < ((most_right-most_left)/2):
                le_px +=1
            elif j >= ((most_right-most_left)/2):
                ri_px +=1
            if i < ((lowest-upperst)/2):
                up_px +=1
            elif i >= ((lowest-upperst)/2):
                lo_px +=1 

HR = float(le_px)/ri_px
VR = float(up_px)/lo_px 
print("HR: ", HR)
print("VR: ", VR)

# Step 2 Linear mapping 
print("Step 2 Linear mapping")
v_1 = HR*1.5-0.62
v_2 = VR*1.2-0.9
print("v_1 = ", v_1)
print("v_2 = ", v_2)

# Step 3 Normalization 
print("Step 3 Normalization")
x_1 = v_1/(abs(v_1)+abs(v_2))
x_2 = v_2/(abs(v_1)+abs(v_2))
if x_1 < 0:
    x_1=-math.sqrt(-x_1)
else:
    x_1=math.sqrt(x_1)
if x_2 < 0:
    x_2=-math.sqrt(-x_2)
else:
    x_2=math.sqrt(x_2)
print("x_1 = ", x_1)
print("x_2 = ", x_2)

# Step 4 Trigonometric function
print("Step 4 Trigonometric function")
if x_1 > 0 and x_2 > 0 or x_1 > 0 and x_2 < 0:       #first quad and forth quad 
    theta = np.arctan(x_2/x_1)
elif x_1 < 0 and x_2 > 0:     #second quad
    theta = np.arctan(x_2/x_1)+3.142
elif x_1 < 0 and x_2 < 0:     #third quad 
    theta = np.arctan(x_2/x_1)+3.142
else:
    print("Error with Step 4 Trigonometric function")

print('theta: ', theta)

with open('/home/biped/catkin_ws/src/jacob/scripts/prepross/test.csv', mode='w') as employee_file:
    employee_writer = csv.writer(employee_file, delimiter=',')
    employee_writer.writerow(['theta_test', theta])
df = pd.read_csv('/home/biped/catkin_ws/src/jacob/scripts/prepross/test.csv')
df.to_csv('/home/biped/catkin_ws/src/jacob/scripts/prepross/test.csv', index=False)

plt.scatter(HR, VR,color='red', label='Test')
plt.title('Preprocessed data')
plt.xlabel('HR')
plt.ylabel('VR')
plt.legend()
plt.xlim(0, 4)
plt.ylim(0, 4)
z = call("python3.7 /home/biped/catkin_ws/src/jacob/scripts/prepross/ros_ip.py {}", shell=True)
# plt.show()

