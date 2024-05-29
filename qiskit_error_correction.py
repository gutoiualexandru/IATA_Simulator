import random
from qiskit import QuantumCircuit, execute, Aer
from qiskit.tools.monitor import job_monitor
from qiskit import ClassicalRegister, QuantumRegister
import matplotlib.pyplot as plt


def apply_random_errors(circuit, q, error_prob=0.1):
    """Apply random bit flip and phase flip errors to the circuit with a given probability."""
    for qubit in q:
        if random.random() < error_prob:
            circuit.barrier(q)
            circuit.x(qubit)  # Bit flip error
            circuit.barrier(q)
        if random.random() < error_prob:
            circuit.barrier(q)
            circuit.z(qubit)  # Phase flip error
            circuit.barrier(q)


# Use the Aer simulator
def nul_process(circuit, q):
    print("no preprocess")


def simulate_Shor(error_prob=0.1, preprocess=nul_process):

    backend = Aer.get_backend('qasm_simulator')

    # q = QuantumRegister(1, 'q')
    # c = ClassicalRegister(1, 'c')

    # circuit = QuantumCircuit(q, c)
    # preprocess(circuit, q)
    # circuit.h(q[0])
    # circuit.barrier(q)
    # apply_random_errors(circuit, q, error_prob)
    # circuit.h(q[0])
    # circuit.barrier(q)

    # circuit.measure(q[0], c[0])
    # job = execute(circuit, backend, shots=1000)
    # job_monitor(job)

    # counts = job.result().get_counts()

    # print("\n Uncorrected bit flip and phase error")
    # print("--------------------------------------")
    # print(counts)

    ##### Shor code starts here ########
    q = QuantumRegister(9, 'q')
    c = ClassicalRegister(1, 'c')

    circuit = QuantumCircuit(q, c)
    preprocess(circuit, q)
    circuit.cx(q[0], q[3])
    circuit.cx(q[0], q[6])
    apply_random_errors(circuit, q, error_prob)

    circuit.h(q[0])
    circuit.h(q[3])
    circuit.h(q[6])
    apply_random_errors(circuit, q, error_prob)

    circuit.cx(q[0], q[1])
    circuit.cx(q[3], q[4])
    circuit.cx(q[6], q[7])
    apply_random_errors(circuit, q, error_prob)

    circuit.cx(q[0], q[2])
    circuit.cx(q[3], q[5])
    circuit.cx(q[6], q[8])
    apply_random_errors(circuit, q, error_prob)

    circuit.cx(q[0], q[1])
    circuit.cx(q[3], q[4])
    circuit.cx(q[6], q[7])
    apply_random_errors(circuit, q, error_prob)

    circuit.cx(q[0], q[2])
    circuit.cx(q[3], q[5])
    circuit.cx(q[6], q[8])
    apply_random_errors(circuit, q, error_prob)

    circuit.ccx(q[1], q[2], q[0])
    circuit.ccx(q[4], q[5], q[3])
    circuit.ccx(q[8], q[7], q[6])
    apply_random_errors(circuit, q, error_prob)

    circuit.h(q[0])
    circuit.h(q[3])
    circuit.h(q[6])
    apply_random_errors(circuit, q, error_prob)

    circuit.cx(q[0], q[3])
    circuit.cx(q[0], q[6])
    circuit.ccx(q[6], q[3], q[0])
    apply_random_errors(circuit, q, error_prob)

    circuit.measure(q[0], c[0])

    # Draws an image of the circuit
    circuit.draw(output='mpl', filename='shorcode.png')

    job = execute(circuit, backend, shots=1000)

    job_monitor(job)

    counts = job.result().get_counts()

    print("\nShor code with bit flip and phase error")
    print("----------------------------------------")
    print(counts)

    plt.show()  # To display the circuit image
