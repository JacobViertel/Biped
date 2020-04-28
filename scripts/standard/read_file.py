from csv import reader
import csv
import os
import numpy as np

if os.path.exists("/home/biped/catkin_ws/src/jacob/motions/quantum.txt"):
    os.remove("/home/biped/catkin_ws/src/jacob/motions/quantum.txt")
else:
    pass

#spaeter in python2 umwandeln 
with open("/home/biped/catkin_ws/src/jacob/scripts/results/circuit_results.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    Lshoulder_motion = []
    Lelbow_motion = []
    Lwrist_motion = []
    Rshoulder_motion = []
    Relbow_motion = []
    Rwrist_motion = []
    
    for row in csv_reader:
        if  line_count == 0:
            for i in row:
                if i == "00":
                    Lshoulder_motion.append(-0.06)
                elif i == "01":
                    Lshoulder_motion.append(-0.82)
                elif i == "10":
                    Lshoulder_motion.append(-2.01)
                elif i == "11":
                    Lshoulder_motion.append(-2.86)
            line_count +=1
        elif line_count == 1:
            for i in row:
                if i == "00":
                    Lelbow_motion.append(1.51)
                elif i == "01":
                    Lelbow_motion.append(0.97)
                elif i == "10":
                    Lelbow_motion.append(0.46)
                elif i == "11":
                    Lelbow_motion.append(-0.06)
            line_count +=1
        elif line_count == 2:
            for i in row:
                if i == "00":
                    Lwrist_motion.append(0.14)
                elif i == "01":
                    Lwrist_motion.append(-0.45)
                elif i == "10":
                    Lwrist_motion.append(0.96)
                elif i == "11":
                    Lwrist_motion.append(1.55)
            line_count +=1

    for i in row:
        Rshoulder_motion.append(-0.13)
        Relbow_motion.append(0.21)
        Rwrist_motion.append(0.12)
    # print(shoulder_motion)
    # print(elbow_motion)
    # print(wrist_motion)

    
with open("/home/biped/catkin_ws/src/jacob/motions/quantum.txt", "a") as fp:
    wr = csv.writer(fp, dialect="excel")
    wr.writerow(Lshoulder_motion)
    wr.writerow(Rshoulder_motion)
    wr.writerow(Lelbow_motion)
    wr.writerow(Relbow_motion)
    wr.writerow(Lwrist_motion)
    wr.writerow(Rwrist_motion)

with open("/home/biped/catkin_ws/src/jacob/motions/quantum.txt") as file:
    lis = [x.replace('\n', '').split(',') for x in file]

x = np.array(lis)
# print(x)
init_pose = [0.03,-0.005,1.4,-0.04,0.21,3.16]
with open("/home/biped/catkin_ws/src/jacob/motions/quantum.txt", "w") as fp:
    wr = csv.writer(fp, dialect="excel")
    for i in range(len(x.T)):
        wr.writerow(x.T[i])
    wr.writerow(init_pose)
