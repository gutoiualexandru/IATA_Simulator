from error_correction import *


def preprocess(quantum_system):
    quantum_system.apply_H_gate(0)


simulate_circuit(100, 1, 0.1, preprocess)
