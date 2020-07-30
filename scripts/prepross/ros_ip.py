from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute, BasicAer, Aer
import matplotlib.pyplot as plt
import math
import numpy as np
from numpy import pi
import csv
from csv import writer
from csv import reader


theta1 = 0.154555312505315
theta2 = 0.8556282786495321
theta_test = []
prediction = []
#9,0.7939398655262304
#9,1.1456569625081987
#6,-0.2509813786461824
#6,0.13373520531332234
with open('/home/biped/catkin_ws/src/jacob/scripts/prepross/test.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        theta_test.append(row[1])
#print(len(theta0))

def inner_prod(theta_train, theta_test):
    res = QuantumRegister(1, 'res')             # 2 qubit quantum register called 'q_in'
    y = QuantumRegister(1, 'y')                 # 1 qubit quantum register called 'y'
    a = QuantumRegister(1, 'train')           # 1 qubit qunatum register called 'a' for ancilla
    # defining classical register for output of circuit
    out = ClassicalRegister(1, 'read')
    # combining all quantum and classical register to define a quantum circuit object called 'qc'
    qc = QuantumCircuit(res,y,a,out)
    qc.rx(theta_train,1)
    qc.rx(theta_test,2)
    qc.h(0)
    qc.cswap(0,1,2)
    qc.h(0)
    qc.measure(res[0],out[0])
    backend = Aer.get_backend('qasm_simulator')
    # run QASM simulator on circuit
    job = execute(qc, backend, shots=1000)
    # obtain result from simulation
    result = job.result()
    # obtain counts from simulation
    counts = result.get_counts(qc)
    #print(counts["0"])
    results.append(counts["0"])
    
results = []
inner_prod(theta1, theta_test[0])
inner_prod(theta2, theta_test[0])
if results[0] > results[1]:
    print('we think it is a 6!')
    prediction.append(6)
else:
    print('we think it is a 9!')
    prediction.append(9)

# Open the input_file in read mode and output_file in write mode
with open('/home/biped/catkin_ws/src/jacob/scripts/prepross/test.csv', 'r') as read_obj, \
        open('/home/biped/catkin_ws/src/jacob/scripts/prepross/prediction_ip.csv', 'w', newline='') as write_obj:
    # Create a csv.reader object from the input file object
    csv_reader = reader(read_obj)
    # Create a csv.writer object from the output file object
    csv_writer = writer(write_obj)
    # Read each row of the input csv file as list
    i=0
    for row in csv_reader:
        # Append the default text in the row / list
        row.append(prediction[i])
        # Add the updated row / list to the output file
        csv_writer.writerow(row)
        i+=1