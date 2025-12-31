import pyzx as zx

qasm_filename = 'base_circuit.qasm'

try:
    # Load the QASM circuit
    c_original = zx.Circuit.load(qasm_filename)
    print(f"Successfully loaded {qasm_filename}")
    print("--- Original Circuit Stats ---")
    # .stats() gives a full breakdown of gate counts
    print(c_original.stats())
    
    # Convert to ZX-Graph and Optimize
    print("\nOptimizing circuit using pyZX...")
    g = c_original.to_graph()
    
    # This is the main simplification routine
    # It simplifies the graph in-place
    zx.simplify.full_reduce(g) 
    print("Optimization complete.")

    # Extract the Optimized Circuit Back
    c_optimized = zx.extract_circuit(g)

    print("\n--- Optimized Circuit Stats ---")
    print(c_optimized.stats()) 
    
    # Save the new circuit
    optimized_filename = 'optimized_circuit.qasm'
    
    # We need to convert to basic gates for a clean QASM output
    c_optimized_basic = c_optimized.to_basic_gates()
    
    with open(optimized_filename, 'w') as f:
        f.write(c_optimized_basic.to_qasm())
        
    print(f"\nSuccessfully saved optimized circuit to {optimized_filename}")
    
    # Show the reduction
    original_cnots = c_original.count_ops().get('CNOT', 0)
    optimized_cnots = c_optimized_basic.count_ops().get('CNOT', 0)
    
    if original_cnots > 0:
        reduction = 100 * (original_cnots - optimized_cnots) / original_cnots
        print("\n--- Summary ---")
        print(f"Original CNOTs:   {original_cnots}")
        print(f"Optimized CNOTs:  {optimized_cnots}")
        print(f"CNOT Reduction:   {reduction:.2f}%")
    

except FileNotFoundError:
    print(f"Error: Could not find '{qasm_filename}'.")
    print("Please make sure it is in the same directory as this script.")
except Exception as e:
    print(f"An error occurred: {e}")