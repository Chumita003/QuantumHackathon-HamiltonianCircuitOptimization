from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import SuzukiTrotter
from qiskit import QuantumCircuit
import numpy as np
from qiskit.qasm2 import dumps as qasm2_dumps

try:
    from hamiltonian_terms import get_toluene_hamiltonian_terms
except ImportError:
    print("Error: Could not find 'hamiltonian_terms.py'.")
    print("Please make sure it's in the same directory.")
    exit()
except Exception as e:
    print(f"An unexpected error occurred importing: {e}")
    exit()


# Get the Hamiltonian terms
print("Building Hamiltonian...")
all_terms = get_toluene_hamiltonian_terms()
H_toluene = SparsePauliOp.from_list(all_terms)
print(f"Successfully built Hamiltonian with {len(all_terms)} terms.")


# Build the Trotterized Circuit
# These are the parameters for our first circuit
simulation_time = 0.5 # (in ms, as the paper)
trotter_steps = 1  

print(f"Building circuit for t={simulation_time}ms, steps={trotter_steps}...")

# first-order Trotter formula
trotter = SuzukiTrotter(order=1, reps=trotter_steps)
evo_gate = PauliEvolutionGate(H_toluene, time=simulation_time)

# Synthesize the circuit
base_circuit = trotter.synthesize(evo_gate)

# Decompose the circuit into basic gates (CNOTs, Rz, etc.)
# required for pyZX
base_circuit_decomposed = base_circuit.decompose()

base_circuit.draw()

print("Circuit built and decomposed.")
# Use count_ops() to get a dictionary of gates and their counts
ops_count = base_circuit_decomposed.count_ops()
print(f"Original circuit CNOT count: {ops_count.get('cx', 0)}")
print(f"Original circuit total operations: {sum(ops_count.values())}")


# Save the Circuit to QASM
qasm_filename = 'base_circuit.qasm'
try:
    qasm_string = qasm2_dumps(base_circuit_decomposed)
    
    with open(qasm_filename, 'w') as f:
        f.write(qasm_string)
    
    print(f"\nSuccessfully saved circuit to {qasm_filename}")
    print("You are now ready to run the pyZX optimization step on this file.")

except Exception as e:
    print(f"\nError saving QASM file: {e}")