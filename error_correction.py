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


def nul_function(quantum_system):
    print("no preprocess")


def print_nonzero_states(L, tol=1e-10):
    for i in range(len(L)):
        if abs(L[i].real) > tol or abs(L[i].imag) > tol:
            value_real_bin = format(int(L[i].real), 'b')
            value_imag_bin = format(int(L[i].imag), 'b')
            value_bin = f"{value_real_bin} + {value_imag_bin}j"
            index_bin = format(i, 'b')
            print(f"State: {index_bin}")


def before_error_shor(nr_qubits, quantum_system, first_qubit_value, preprocess0=nul_function):

    list_qubits = [first_qubit_value]
    for i in range(nr_qubits-1):
        list_qubits.append(0)
    quantum_system.initialize_state(list_qubits)
    print_nonzero_states(quantum_system.state)
    # First CNOT applied
    cnot_list = [
        ([0], 3),
        ([0], 6)
    ]
    preprocess0(quantum_system)
    quantum_system.apply_cnot_chain(cnot_list)
    # Apply H gates on qubits 0, 3, 6
    quantum_system.apply_H_gate(0)
    quantum_system.apply_H_gate(3)
    quantum_system.apply_H_gate(6)
    # Apply 3rd CNOT gates on 0 and 1, 3 and 4, 6 and 7
    quantum_system.apply_CNOT_gate(0)
    quantum_system.apply_CNOT_gate(3)
    quantum_system.apply_CNOT_gate(6)
    # Apply 4th CNOT gates
    cnot_list = [
        ([0], 2),
        ([3], 5),
        ([6], 8)
    ]
    quantum_system.apply_cnot_chain(cnot_list)
    return quantum_system


def after_error_shor(quantum_system):
    # First CNOT gates applied
    quantum_system.apply_CNOT_gate(0)
    quantum_system.apply_CNOT_gate(3)
    quantum_system.apply_CNOT_gate(6)
    # 2nd CNOT gates applied
    cnot_list = [
        ([0], 2),
        ([3], 5),
        ([6], 8)
    ]
    quantum_system.apply_cnot_chain(cnot_list)
    # Double control gates
    target_qubit_list = [0, 3, 6]
    control_qubit_list = [[1, 2], [4, 5], [7, 8]]
    for i in range(len(target_qubit_list)):
        target_qubit = target_qubit_list[i]
        control_qubit = control_qubit_list[i]
        quantum_system.multi_controlled_cnot(control_qubit, target_qubit)
    # The H gates on qubits 0, 3, 6
    quantum_system.apply_H_gate(0)
    quantum_system.apply_H_gate(3)
    quantum_system.apply_H_gate(6)
    # The 4th CNOT gate
    cnot_list = [
        ([0], 3),
        ([0], 6)
    ]
    quantum_system.apply_cnot_chain(cnot_list)
    # 6th CNOT gate
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


def complete_circuit(first_qubit, p, preprocess0=nul_function):
    quantum_system = NQubitSystem(n_qubits=9)
    quantum_system = before_error_shor(
        9, quantum_system, first_qubit, preprocess0)
    quantum_system, bec = introduce_noise(p, quantum_system)
    print("Was an error introduced: {}".format(bec))
    quantum_system = after_error_shor(quantum_system)
    print_nonzero_states(quantum_system.state)
    a, b = quantum_system.produce_specific_measurement(0)
    return [a, b]


def simulate_circuit(shots, first_qubit=0, p=0.1, preprocess0=nul_function):
    out = [0]*2
    for i in range(shots):
        a, b = complete_circuit(first_qubit, p, preprocess0)
        out[0] += a
        out[1] += b
    plt.figure(figsize=(6, 4))
    plt.bar(['State 0', 'State 1'], out, color=['blue', 'orange'])
    plt.xlabel('State')
    plt.ylabel('Frequency')
    plt.title('Histogram of States')
    plt.show()


# simulate_circuit(10, 0, 0.1, preprocess)
