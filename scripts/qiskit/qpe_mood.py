#!/usr/bin/env python
# coding: utf-8

#initialization
import numpy as np
import math
import csv
import sys

# importing Qiskit
from qiskit import IBMQ, Aer
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute

# Defining quantum fourier transformation:
def qft_dagger(circ, n):
    """n-qubit QFTdagger the first n qubits in circ"""
    # Don't forget the Swaps!
    for qubit in range(n//2):
        circ.swap(qubit, n-qubit-1)
    for j in range(n):
        for m in range(j):
            circ.cu1(-math.pi/float(2**(j-m)), m, j)
        circ.h(j)

mood = sys.argv[1]
mood = int(float(mood))
# Setting up the quantum circuit:
qpe = QuantumCircuit(3, 2)
qpe.x(2)
for qubit in range(2):
    qpe.h(qubit)
repetitions = 1
for counting_qubit in range(2):
    for i in range(repetitions):
        qpe.cu1(math.pi*2*mood/4, counting_qubit, 2); # This is C-U
    repetitions *= 2
# Apply inverse QFT
qft_dagger(qpe, 2)
# Measure
qpe.barrier()
for n in range(2):
    qpe.measure(n,n)

# Execute circuit and write results
backend = Aer.get_backend('qasm_simulator')
shots = 2048
results = execute(qpe, backend=backend, shots=shots).result()
answer = results.get_counts()

mood_result = open("/home/biped/catkin_ws/src/jacob/scripts/results/qpe_mood_result.csv", "w")
writer = csv.writer(mood_result)
for key, value in answer.items():
    writer.writerow([key, value])
mood_result.close()
print("QPE is done!")
