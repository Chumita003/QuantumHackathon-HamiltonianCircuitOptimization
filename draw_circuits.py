import qiskit
from qiskit import QuantumCircuit
import matplotlib.pyplot as plt


plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

base_qasm_file = 'base_circuit.qasm'
opt_qasm_file = 'optimized_circuit.qasm'

print(f"Loading circuit from {base_qasm_file}...")
try:
    # Load the base circuit from the QASM file
    base_circuit = QuantumCircuit.from_qasm_file(base_qasm_file)
    
    # Draw the circuit and save it to a file
    print("Drawing base circuit to 'base_circuit.png'...")
    base_circuit.draw(output='mpl', style='iqp', filename='base_circuit.png')
    print("Saved 'base_circuit.png'")

except Exception as e:
    print(f"Error processing {base_qasm_file}: {e}")
    print("It might be too large for the 'mpl' drawer.")
    print("You can also try drawing it with 'text':")

print(f"\nLoading circuit from {opt_qasm_file}...")
try:
    opt_circuit = QuantumCircuit.from_qasm_file(opt_qasm_file)
    
    print("Drawing optimized circuit to 'optimized_circuit.png'...")
    opt_circuit.draw(output='mpl', style='iqp', filename='optimized_circuit.png')
    print("Saved 'optimized_circuit.png'")

except Exception as e:
    print(f"Error processing {opt_qasm_file}: {e}")

print("\nDone. Check your folder for 'base_circuit.png' and 'optimized_circuit.png'.")