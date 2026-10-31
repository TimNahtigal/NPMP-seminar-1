import random
from qiskit import QuantumCircuit, transpile, qasm2
import pyzx as zx

class PyZXOptimizer:
    """Converts a Qiskit circuit to PyZX, optimizes it using ZX-calculus, 
    and converts it back to a Qiskit circuit format.
    """

    def __init__(self):
        pass

    def optimize(self, qc: QuantumCircuit) -> QuantumCircuit:
        # Step 0: Decompose high-level gates (like ccx) into primitive basis gates 
        # so they can be properly exported and interpreted by PyZX.
        decomposed_qc = transpile(
            qc, 
            basis_gates=['cx', 'u3', 't', 'tdg', 'h', 's', 'x', 'z', 'rz'], 
            optimization_level=0
        )

        # Convert Qiskit circuit to OpenQASM 2 string using the qasm2 module
        qasm_str = qasm2.dumps(decomposed_qc)
        zx_circuit = zx.Circuit.from_qasm(qasm_str)

        # Convert to a ZX graph, simplify/optimize via ZX-calculus graph rewriting
        graph = zx_circuit.to_graph()
        zx.full_reduce(graph)
        
        # Extract back to a PyZX circuit and export to QASM string
        optimized_zx_circuit = zx.extract_circuit(graph)
        optimized_qasm = optimized_zx_circuit.to_qasm()

        # Convert back to a Qiskit QuantumCircuit
        optimized_qc = QuantumCircuit.from_qasm_str(optimized_qasm)
        return optimized_qc