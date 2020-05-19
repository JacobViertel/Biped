#!/usr/bin/env python
# coding: utf-8

#initialization
import numpy as np
pi = np.pi
# importing Qiskit
from qiskit import *

import os
import csv

if os.path.exists("/home/biped/catkin_ws/src/jacob/scripts/results/l_r_greet_result.csv"):
    os.remove("/home/biped/catkin_ws/src/jacob/scripts/results/l_r_greet_result.csv")
else:
    pass

# setting up params
n = 2
rot = 0.77
with open("/home/biped/catkin_ws/src/jacob/scripts/results/strong_hand.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            lor = row[0]
print(lor)

q = QuantumRegister(n)
grover_circuit = QuantumCircuit(q)
for qubit in range(n):
    grover_circuit.h(qubit)
if lor == "1":
    for qubit in range(n):
        grover_circuit.x(qubit)
grover_circuit.cu1(pi/rot,q[0], q[1])
if lor == "1":
    for qubit in range(n):
        grover_circuit.x(qubit)
for qubit in range(n):
    grover_circuit.h(qubit)
for qubit in range(n):
    grover_circuit.z(qubit)
grover_circuit.cu1(pi/rot,q[0], q[1])
for qubit in range(n):
    grover_circuit.h(qubit)
grover_circuit.measure_all()

backend = BasicAer.get_backend('qasm_simulator')
shots = 1
results = execute(grover_circuit, backend=backend, shots=shots).result()
answer = results.get_counts()

lor_result = open("/home/biped/catkin_ws/src/jacob/scripts/results/l_r_greet_result.csv", "w")
writer = csv.writer(lor_result)
writer.writerow(answer.keys())
lor_result.close()
print(answer)
print("motion selection is done")



