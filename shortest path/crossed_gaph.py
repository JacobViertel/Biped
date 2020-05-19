import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import math

# importing Qiskit
import qiskit
from qiskit import IBMQ, Aer
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute, BasicAer

# import basic plot tools
from qiskit.visualization import plot_histogram

dreg = QuantumRegister(1, 'd')
nreg = QuantumRegister(2, 'n')
creg = ClassicalRegister(2, 'c')
circ = QuantumCircuit(dreg, nreg, creg)
start_node = "00"
end_node = "11"


nodes = ["00","01","10","11"]

vertics =   [[0,0,1,1],
            [0,0,1,1],
            [1,1,0,0],
            [1,1,0,0]]

# drawing graph
graph = np.matrix(vertics)
K = nx.from_numpy_matrix(graph)
nx.draw(K, with_labels = True)
plt.show()
# setting params
found_path = False
vistied_nodes =[]
numb_vertices = len(vertics[0])
current_node = start_node

# compare qubit string
# def compare(a, b):
    # cnt = 1
    # for x, y in zip(a, b):
        # if x == str(y): #qubits of current and target are equal
            # print(cnt, " qubit is equal")
            # pass
        # else:
            # print(cnt, " qubit is different")
            # circ.cx(0,cnt) #qubits of current and target are different
        # cnt = cnt+1
        # 
    # circ.x(0)
# 
vistied_nodes.append(current_node)
i = 0
def compare(a, b):
    cnt = 2
    for x, y in zip(a, b):
        if x == str(y): #qubits of current and target are equal
            # print(cnt, " qubit is equal")
            pass
        else:
            # print(cnt, " qubit is different")
            circ.cx(0,cnt) #qubits of current and target are different
        cnt = cnt-1
        
    circ.x(0)
# while found_path == False:
for loop in range(10):
    circ.h(0)
    y=nodes.index(current_node)
    # print(y)
    # print("We are at vertics: ", current_node)
    for j in range(numb_vertices):
        if vertics[y][j] == 1:
            # print("We can go to vertics: ", nodes[j])
            compare(current_node, nodes[j])

    # circ.cx(0,2)
    # circ.x(0)
    # circ.cx(0,1)
    # circ.cx(0,2)
    # circ.x(0)
    # y=nodes.index(current_node)
    # print(y)
    # print("We are at vertics: ", current_node)
    # for j in range(numb_vertices):
        # if vertics[y][j] == 1:
            # print("We can go to vertics: ", nodes[j])
            # compare(current_node, nodes[j])
    # Execute and see results
    
    circ.measure(nreg[:2],creg)
    backend = BasicAer.get_backend('qasm_simulator')
    shots = 1
    results = execute(circ, backend=backend, shots=shots).result()
    answer = results.get_counts()
    found_path = False
    for key, value in answer.items():
        vistied_nodes.append(key)
        print("Currently in iteration no. ", i+1, "We are at node ", key)
        current_node = key
        if key == "11":
            found_path=True
    i = i+1
print("we found the path", vistied_nodes)
