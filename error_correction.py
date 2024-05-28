from NQubitSystem import NQubitSystem
import numpy as np
from constants import gates_map
from Gate import Gate
from pytket import Circuit
from pytket.circuit.display import render_circuit_jupyter
import matplotlib.pyplot as plt
import cirq
from pytket.extensions.qiskit import tk_to_qiskit
from collections import Counter
import backend as back
import random

def print_nonzero_states(L, tol=1e-10):
    for i in range(len(L)):
        if abs(L[i].real) > tol or abs(L[i].imag) > tol:
            value_real_bin = format(int(L[i].real), 'b')
            value_imag_bin = format(int(L[i].imag), 'b')
            value_bin = f"{value_real_bin} + {value_imag_bin}j"
            index_bin = format(i, 'b')
            print(f"Index: {index_bin}, Value: {value_bin}")


def before_error_shor(nr_qubits, quantum_system, first_qubit_value):
    list_qubits = [first_qubit_value]
    for i in range(nr_qubits-1):
        list_qubits.append(0)
    quantum_system.initialize_state(list_qubits)
    print_nonzero_states(quantum_system.state)
    # First CNOT applied
    target_qubit = 3
    control_qubit = [0]
    starting_qubit = 0
    gate_name = "CNOT"
    control_gate_name = f"Controlled-{gate_name}_Cq{control_qubit}_Tq{target_qubit}"
    gate = quantum_system.control_gate(control_qubits = control_qubit, target_qubit = target_qubit, gate_matrix = gates_map[gate_name][0], name=control_gate_name)
    quantum_system.apply_gate(gate, starting_qubit = starting_qubit)
    # Second CNOT applied
    target_qubit = 6
    control_qubit = [0]
    starting_qubit = 0
    gate_name = "CNOT"
    control_gate_name = f"Controlled-{gate_name}_Cq{control_qubit}_Tq{target_qubit}"
    gate = quantum_system.control_gate(control_qubits = control_qubit, target_qubit = target_qubit, gate_matrix = gates_map[gate_name][0], name=control_gate_name)
    quantum_system.apply_gate(gate, starting_qubit = starting_qubit)
    # Apply H gates on qubits 0, 3, 6
    quantum_system.apply_H_gate(0)
    quantum_system.apply_H_gate(3)
    quantum_system.apply_H_gate(6)
    # Apply 3rd CNOT gates on 0 and 1, 3 and 4, 6 and 7
    quantum_system.apply_CNOT_gate(0)
    quantum_system.apply_CNOT_gate(3)
    quantum_system.apply_CNOT_gate(6)
    # Apply 4th CNOT gates
    target_qubit_list = [2, 5, 8]
    control_qubit_list = [[0], [3], [6]]
    starting_qubit = 0
    gate_name = "CNOT"
    for i in range(len(target_qubit_list)):
        target_qubit = target_qubit_list[i]
        control_qubit = control_qubit_list[i]
        control_gate_name = f"Controlled-{gate_name}_Cq{control_qubit}_Tq{target_qubit}"
        gate = quantum_system.control_gate(control_qubits = control_qubit, target_qubit = target_qubit, gate_matrix = gates_map[gate_name][0], name=control_gate_name)
        quantum_system.apply_gate(gate, starting_qubit = starting_qubit)
    return quantum_system
    
def after_error_shor(nr_qubits, quantum_system, first_qubit_value):
    #First CNOT gates applied
    quantum_system.apply_CNOT_gate(0)
    quantum_system.apply_CNOT_gate(3)
    quantum_system.apply_CNOT_gate(6)
    # 2nd CNOT gates applied
    target_qubit_list = [2, 5, 8]
    control_qubit_list = [[0], [3], [6]]
    starting_qubit = 0
    gate_name = "CNOT"
    for i in range(len(target_qubit_list)):
        target_qubit = target_qubit_list[i]
        control_qubit = control_qubit_list[i]
        control_gate_name = f"Controlled-{gate_name}_Cq{control_qubit}_Tq{target_qubit}"
        gate = quantum_system.control_gate(control_qubits = control_qubit, target_qubit = target_qubit, gate_matrix = gates_map[gate_name][0], name=control_gate_name)
        quantum_system.apply_gate(gate, starting_qubit = starting_qubit)
    #Double control gates
    target_qubit_list = [0, 3, 6]
    control_qubit_list = [[1, 2], [4, 5], [7, 8]]
    starting_qubit = 0
    gate_name = "CNOT10"
    for i in range(len(target_qubit_list)):
        target_qubit = target_qubit_list[i]
        control_qubit = control_qubit_list[i]
        #control_gate_name = f"Controlled-{gate_name}_Cq{control_qubit}_Tq{target_qubit}"
        #gate = quantum_system.control_gate(control_qubits = control_qubit, target_qubit = target_qubit, gate_matrix = gates_map[gate_name][0], name=control_gate_name)
        #quantum_system.apply_gate(gate, starting_qubit = starting_qubit)
        quantum_system.multi_controlled_cnot(control_qubit, target_qubit)
    #The H gates on qubits 0, 3, 6
    quantum_system.apply_H_gate(0)
    quantum_system.apply_H_gate(3)
    quantum_system.apply_H_gate(6)
    # The 4th CNOT gate
    target_qubit = 3
    control_qubit = [0]
    starting_qubit = 0
    gate_name = "CNOT"
    control_gate_name = f"Controlled-{gate_name}_Cq{control_qubit}_Tq{target_qubit}"
    gate = quantum_system.control_gate(control_qubits = control_qubit, target_qubit = target_qubit, gate_matrix = gates_map[gate_name][0], name=control_gate_name)
    quantum_system.apply_gate(gate, starting_qubit = starting_qubit)
    # 5th CNOT applied
    target_qubit = 6
    control_qubit = [0]
    starting_qubit = 0
    gate_name = "CNOT"
    control_gate_name = f"Controlled-{gate_name}_Cq{control_qubit}_Tq{target_qubit}"
    gate = quantum_system.control_gate(control_qubits = control_qubit, target_qubit = target_qubit, gate_matrix = gates_map[gate_name][0], name=control_gate_name)
    quantum_system.apply_gate(gate, starting_qubit = starting_qubit)
    # 6th CNOT gate
    #target_qubit = 0
    #control_qubit = [3, 6]
    #starting_qubit = 0
    #gate_name = "CNOT10"
    #control_gate_name = f"Controlled-{gate_name}_Cq{control_qubit}_Tq{target_qubit}"
    #gate = quantum_system.control_gate(control_qubits = control_qubit, target_qubit = target_qubit, gate_matrix = gates_map[gate_name][0], name=control_gate_name)
    #quantum_system.apply_gate(gate, starting_qubit = starting_qubit)
    control_qubits = [3, 6]
    target_qubit = 0
    quantum_system.multi_controlled_cnot(control_qubits, target_qubit)
    return quantum_system


def introduce_noise(p, quantum_system):
    target = 0
    bec = 1
    if random.random() < p:
        quantum_system.apply_X_gate(target, False)
        bec = 0
    if random.random() < p:
        quantum_system.apply_Z_gate(target, False)
        bec = 0
    return quantum_system, bec


quantum_system = NQubitSystem(n_qubits = 9)
#list_qubits = [1]
#for i in range(8):
#    list_qubits.append(0)
#quantum_system.initialize_state(list_qubits)
#target_qubit = 3
#control_qubit = [0]
## starting_qubit = np.min([target_qubit,np.min(control_qubit)])
#starting_qubit = 0
#gate_name = "CNOT"
#control_gate_name = f"Controlled-{gate_name}_Cq{control_qubit}_Tq{target_qubit}"
#gate = quantum_system.control_gate(control_qubits = control_qubit, target_qubit = target_qubit, gate_matrix = gates_map[gate_name][0], name=control_gate_name)
#quantum_system.apply_gate(gate, starting_qubit = starting_qubit)
#quantum_system.print_state()
quantum_system = before_error_shor(9, quantum_system, 1)
quantum_system, bec = introduce_noise(1, quantum_system)
print("Was an error introduced: {}".format(bec))
quantum_system = after_error_shor(9, quantum_system, 1)
print_nonzero_states(quantum_system.state)
a, b = quantum_system.produce_specific_measurement(0)
print(a)
print(b)