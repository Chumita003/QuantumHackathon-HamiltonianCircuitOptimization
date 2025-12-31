import numpy as np
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import SuzukiTrotter
from qiskit import QuantumCircuit

def get_toluene_hamiltonian_terms():
    """
    Qubit Mapping:
    C13 -> Qubit 0
    H1  -> Qubit 1
    H2  -> Qubit 2
    H3  -> Qubit 3
    H4  -> Qubit 4
    H5  -> Qubit 5
    H6  -> Qubit 6
    H7  -> Qubit 7
    H8  -> Qubit 8
    
    Prefactors used:
    d_ij^ZZ (C-H) = D_Ci / 2.0
    d_ij^XY (H-H) = -D_ij / 4.0
    """
    
    num_qubits = 9
    pauli_terms = []

    def pauli_string(qubits, op):
        """Helper function to create a 9-qubit Pauli string."""
        s = ['I'] * num_qubits
        for i, o in zip(qubits, op):
            s[i] = o
        return "".join(s)

    # --- Part 1: C-H (ZZ) couplings ---
    # 8 total terms
    # d_ij^ZZ = D_Ci / 2.0
    zz_couplings = {
        (0, 1): -4139.45, # D_C1
        (0, 2): 50.16,    # D_C2
        (0, 3): 50.16,    # D_C3 
        (0, 4): -77.68,   # D_C4
        (0, 5): -77.68,   # D_C5 
        (0, 6): -45.33,   # D_C6
        (0, 7): -45.33,   # D_C7 
        (0, 8): -45.33    # D_C8 
    }

    for (i, j), D_Ci in zz_couplings.items():
        coeff = D_Ci / 2.0
        pauli_terms.append((pauli_string([i, j], "ZZ"), coeff))

    # H-H (XY) couplings
    # 28 total pairs -> 56 total terms (XX and YY)
    # d_ij^XY = -D_ij / 4.0
    xy_couplings = {
        # H-H couplings from Table III
        (1, 2): -242.25,  # D_12
        (1, 3): -242.25,  # D_13
        (1, 4): -196.73,  # D_14
        (1, 5): -196.73,  # D_15
        (1, 6): -100.95,  # D_16
        (1, 7): -100.95,  # D_17 
        (1, 8): -100.95,  # D_18 
        
        (2, 3): 26.64,    # D_23
        (2, 4): -1412.40, # D_24
        (2, 5): -30.53,   # D_25
        (2, 6): -126.91,  # D_26
        (2, 7): -126.91,  # D_27 
        (2, 8): -126.91,  # D_28 
        
        (3, 4): -30.53,   # D_34
        (3, 5): -1412.40, # D_35
        (3, 6): -126.91,  # D_36
        (3, 7): -126.91,  # D_37
        (3, 8): -126.91,  # D_38 
        
        (4, 5): 27.38,    # D_45
        (4, 6): -405.22,  # D_46
        (4, 7): -405.22,  # D_47 
        (4, 8): -405.22,  # D_48 

        (5, 6): -405.22,  # D_56 
        (5, 7): -405.22,  # D_57 
        (5, 8): -405.22,  # D_58 

        (6, 7): 1860.23,  # D_67
        (6, 8): 1860.23,  # D_68 
        (7, 8): 1860.23   # D_78 
    }

    for (i, j), D_ij in xy_couplings.items():
        # d_ij^XY * (X_i X_j - Y_i Y_j)
        coeff_xx = -D_ij / 4.0
        coeff_yy = -coeff_xx  # The minus sign is from (-Y_i Y_j)
        
        # Add (coeff_xx * XX)
        pauli_terms.append((pauli_string([i, j], "XX"), coeff_xx))
        # Add (coeff_yy * YY)
        pauli_terms.append((pauli_string([i, j], "YY"), coeff_yy))

    return pauli_terms

if __name__ == "__main__":
    # full list of 64 terms
    all_terms = get_toluene_hamiltonian_terms()
    
    print(f"--- Generated Toluene Hamiltonian ---")
    print(f"Total number of qubits: 9")
    print(f"Total Pauli terms: {len(all_terms)}") # 8 (ZZ) + 28*2 (XY) = 64
    
    # Build the Qiskit Hamiltonian object
    H_toluene = SparsePauliOp.from_list(all_terms)
    
    print("\n--- First 5 terms (C-H couplings): ---")
    print(H_toluene.to_list()[:5])
    
    print("\n--- Last 5 terms (H-H couplings): ---")
    print(H_toluene.to_list()[-5:])

    print("\nThis 'H_toluene' object is now ready for Trotterization.")