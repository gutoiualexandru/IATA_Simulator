from qiskit_error_correction import *


def preprocess(circuit, q):
    circuit.h(q[0])


simulate_Shor(0.1, preprocess)
