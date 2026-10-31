import random
from qiskit import QuantumCircuit, transpile, qasm2
import pyzx as zx

class PyZXOptimizer:
    def __init__(self):
        pass

    def optimize(self, qc: QuantumCircuit) -> QuantumCircuit:
        decomposed_qc = transpile(
            qc, 
            basis_gates=['cx', 'u3', 't', 'tdg', 'h', 's', 'x', 'z', 'rz'], 
            optimization_level=0
        )

        qasm_str = qasm2.dumps(decomposed_qc)
        zx_circuit = zx.Circuit.from_qasm(qasm_str)

        graph = zx_circuit.to_graph()
        zx.full_reduce(graph)
        
        optimized_zx_circuit = zx.extract_circuit(graph)
        optimized_qasm = optimized_zx_circuit.to_qasm()

        optimized_qc = QuantumCircuit.from_qasm_str(optimized_qasm)
        return optimized_qc