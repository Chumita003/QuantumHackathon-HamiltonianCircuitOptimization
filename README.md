# QuantumHackathon-HamiltonianCircuitOptimization

This repository contains a hackathon project focused on constructing and optimizing
quantum circuits derived from a physically motivated Hamiltonian model.

## Overview

The goal of this project was to construct a quantum circuit implementing time evolution
under an interacting spin Hamiltonian, and to analyze the impact of circuit optimization
on depth and gate structure.

Due to time constraints typical of a hackathon setting, the project focuses on a
before-and-after comparison between an unoptimized circuit and its optimized counterpart.

## Physical Model

The Hamiltonian model and interaction coefficients used in this project are derived from:

Zhang et al., "Quantum computation of molecular geometry via many-body nuclear spin echoes",
arXiv:2510.19550 (2025).

The model describes interacting nuclear spins with dipolar couplings. In this project,
the Hamiltonian terms were translated into a quantum circuit representation using
standard gate decompositions.

## Circuit Construction

- `hamiltonian_terms.py` defines the interaction terms and coefficients.
- `Circuit_generate.py` constructs the base quantum circuit implementing the Hamiltonian.
- The resulting circuit is exported to OpenQASM format (`base_circuit.qasm`).

## Circuit Optimization

Circuit optimization was performed using the Qiskit transpiler, which applies standard
optimization passes such as gate cancellation, rotation merging, and depth reduction.

- The optimization process is implemented in `Optimize_circuit.py`.
- The optimized circuit is exported as `optimized_circuit.qasm`.

While the reference paper employs the AlphaEvolve framework for circuit optimization,
this project uses publicly available Qiskit tools suitable for an open hackathon setting.

## Results

The figures below show a comparison between the unoptimized and optimized circuits.

- `base_circuit.png`: original circuit generated from the Hamiltonian.
- `optimized_circuit.png`: circuit after transpilation and optimization.

The optimized circuit exhibits a significant reduction in circuit depth and gate count,
demonstrating the effectiveness of standard compiler-level optimizations.

## Project Status

This project represents a partial implementation developed during a limited-time
hackathon. Further extensions could include:

- Quantitative comparison of circuit depth and gate counts
- Noise-aware optimization targeting specific hardware backends
- Benchmarking optimized circuits using simulated or real hardware

## Usage 
This workflow reproduces the circuit construction and optimization steps used during the hackathon.

1. Clone the repository:
```bash
git clone https://github.com/Chumita003/QuantumHackathon-HamiltonianCircuitOptimization.git
cd QuantumHackathon-HamiltonianCircuitOptimization
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Generate the base circuit from the Hamiltonian terms:
```bash
python Circuit_generate.py
```
This will create base_circuit.qasm.

4. Optimize the circuit using Qiskit transpiler passes:
```bash
python Optimize_circuit.py
```
This will produce optimized_circuit.qasm.

5. Draw and export the circuits as images:
```bash
python draw_circuits.py
```
This will generate base_circuit.png and optimized_circuit.png for visual comparison.
