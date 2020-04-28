#!/usr/bin/env python

from qiskit import *
from math import pi
import numpy as np
import csv
import os

name = sys.argv[1]
homedir = os.environ['HOME']
motion_file = homedir + "/catkin_ws/src/jacob/motions/"+ name + ".txt"
file = open(name,"w+")
file.close()

#removing old reuslts
if os.path.exists(motion_file):
    os.remove(motion_file)
else:
    pass
if os.path.exists("/home/biped/catkin_ws/src/jacob/scripts/results/circuit_properties.csv"):
    os.remove("/home/biped/catkin_ws/src/jacob/scripts/results/circuit_properties.csv")
else:
    pass
if os.path.exists("/home/biped/catkin_ws/src/jacob/scripts/results/circuit_results.csv"):
    os.remove("/home/biped/catkin_ws/src/jacob/scripts/results/circuit_results.csv")
else:
    pass

motors = ["shoulder", "elbow", "wrist"]
#Define circuit properties for joints
for i in range(len(motors)):
    circ_prop = []
    circ_prop.append(motors[i]) 
    
    print("Circuit type of " + motors[i] + " joint ?")
    circuit_type = input("Deter. [d], Class.Proba. [c],\nQuan. Proba. [q],or mix Proba. [m]: ")
    if circuit_type == "d" or circuit_type == "c" or circuit_type == "q" or circuit_type == "m":
        pass
    else:
        raise Exception("Value is not defined")
    rot = 0
    qp_hadamard = 0
    cp_hadamard = 0
    if circuit_type == "d":
        #print("Deterministic circuit build")
        pass
    elif circuit_type == "c":
        #print("Classical Probabilistic circuit build")
        cp_hadamard = 1
        qp_hadamard = 1
    elif circuit_type == "q":
        #print("Quantum Probabilistic circuit build")
        qp_hadamard = 1
    else:
        #print("mix Probabilistic circuit build")
        qp_hadamard = 1
        cp_hadamard = 1
        mix_percent = int(input("How much percent quantum prob? "))
        rot = mix_percent/200
    circ_prop.append(rot)
    circ_prop.append(qp_hadamard)
    circ_prop.append(cp_hadamard)
    print("Define input state!(e.g. 01 or 11)")
    input_state = input("Your input state: ")
    input_state = "01"
    def split(word): 
        return [char for char in word] 
    split_input = split(input_state)
    for i in split_input: 
        if i == "1" or i == "0":
            circ_prop.append(i)
            pass
        else:
            print(i)
            raise Exception("Input state is not defined")
    with open("/home/biped/catkin_ws/src/jacob/scripts/results/circuit_properties.csv", 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(circ_prop)

#build and execute circuits for joints
posture_it = int(input("How many postures do you want? "))
with open("/home/biped/catkin_ws/src/jacob/scripts/results/circuit_properties.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        count = 0
        circ_res = []
        while count < posture_it: 
            #print("Starting iteration no. " + str(count+1)) 
            count +=1
            qc = QuantumCircuit(4,2)
            #input q2
            if row[4] == "1":
                qc.x(2)
            #input q3
            if row[5] == "1":
                qc.x(3)
            #activation classical hadamard
            if row[3] == "1":
                qc.x(0)
            #activation quantum hadamard
            if row[2] == "1":
                qc.x(1)
            qc.ch(0,3) #classical c.hadamard
            qc.ch(1,2) #quantum c.hadamard
            qc.u3(pi*float(row[1]),0,0,3) #rotation gate
            qc.cx(2,3) #permanent toffoli
            qc.measure([2,3],[0,1])
            backend = BasicAer.get_backend('qasm_simulator')
            job = execute(qc, backend).result()
            result = execute(qc, backend, shots=1).result()
            answer = result.get_counts(qc)

            #write results into csv
            for key, value in answer.items():
                circ_res.append(key)
        #print(circ_res)
        with open("/home/biped/catkin_ws/src/jacob/scripts/results/circuit_results.csv", 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(circ_res) 
            # for key, value in result.items():
                # writer.writerow([key])
        with open("/home/biped/catkin_ws/src/jacob/scripts/results/circuit_results.csv", 'r') as file:
            data = file.read().rstrip('\n')

#create the motion file 
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

    
with open(motion_file, "a") as fp:
    wr = csv.writer(fp, dialect="excel")
    wr.writerow(Lshoulder_motion)
    wr.writerow(Rshoulder_motion)
    wr.writerow(Lelbow_motion)
    wr.writerow(Relbow_motion)
    wr.writerow(Lwrist_motion)
    wr.writerow(Rwrist_motion)

with open(motion_file) as file:
    lis = [x.replace('\n', '').split(',') for x in file]

x = np.array(lis)
# print(x)
init_pose = [0.03,-0.005,1.4,-0.04,0.21,3.16]
with open(motion_file, "w") as fp:
    wr = csv.writer(fp, dialect="excel")
    for i in range(len(x.T)):
        wr.writerow(x.T[i])
    wr.writerow(init_pose)
print("motion file " + name + ".txt was generated")
        