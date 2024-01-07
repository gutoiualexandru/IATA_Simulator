import numpy as np

# Map (gate, n_qubits_affected)
gates_map = {
    "X": (np.array([[0, 1], [1, 0]]), 1),
    "Y": (np.array([[0, -1j], [1j, 0]]), 1),
    "Z": (np.array([[1, 0], [0, -1]]), 1),
    "H": (np.array([[1, 1], [1, -1]]) / np.sqrt(2), 1),
    "S": (np.array([[1, 0], [0, 1j]]), 1),
    "T": (np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]]), 1),
    "CNOT": (np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]), 2),
    "CH": (np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1/2**0.5, 1/2**0.5], [0, 0, 1/2**0.5, -1/2**0.5]]), 2),
    "CY": (np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, -1j], [0, 0, 1j, 0]]), 2),
    "CZ": (np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]]), 2),
    "CT": (np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, np.exp(1j * np.pi / 4)]]), 2),
    "CS": (np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1j]]), 2),
    "SWAP": (np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]), 2),
    "CNOT10": (np.array([[1, 0, 0, 0],
                         [0, 0, 0, 1],
                         [0, 0, 1, 0],
                         [0, 1, 0, 0]]), 2),
    "TOFFOLI": (np.array([[1, 0, 0, 0, 0, 0, 0, 0],
                        [0, 1, 0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 1],
                        [0, 0, 0, 0, 0, 0, 1, 0]]), 3)
}