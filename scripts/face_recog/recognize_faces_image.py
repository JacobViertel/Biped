import face_recognition
import argparse
import pickle
import cv2
import os
import sys
import csv
import numpy as np

if os.path.exists("/home/biped/catkin_ws/src/jacob/scripts/results/face_ident.csv"):
    os.remove("/home/biped/catkin_ws/src/jacob/scripts/results/face_ident.csv")
else:
    pass

# input_qvision = sys.argv[1]
# input_qvision = "1"
# example = " "
# if input_qvision == "1":
cap = cv2.VideoCapture(0)
for i in range(1):
	return_value, image = cap.read()
	cv2.imwrite("/home/biped/catkin_ws/src/jacob/scripts/face_recog/examples/face_recog.png", image)
del(cap)

data = pickle.loads(open("/home/biped/catkin_ws/src/jacob/scripts/face_recog/encodings.pickle", "rb").read())

rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

boxes = face_recognition.face_locations(rgb, model="hog")
encodings = face_recognition.face_encodings(rgb, boxes)

names = []

for encoding in encodings:
    matches = face_recognition.compare_faces(data["encodings"], encoding)
    name = "Unknown"

    if True in matches:
        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
        counts = {}
        for i in matchedIdxs:
            name = data["names"][i]             
            counts[name] = counts.get(name, 0) + 1
        name = max(counts, key=counts.get)
    names.append(name)
if len(names) < 1:
    names.append("nobody around")
print(names)
for ((top, right, bottom, left), name) in zip(boxes, names):
    cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
    y = top - 15 if top - 15 > 15 else top + 15
    cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
cv2.imshow("Image", image)
cv2.waitKey(0)
# print("done_face_recog")
ident_result = open("/home/biped/catkin_ws/src/jacob/scripts/results/face_ident.csv", "w")
writer = csv.writer(ident_result)
writer.writerow(names)
ident_result.close()

