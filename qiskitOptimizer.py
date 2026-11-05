import random
from qiskit import QuantumCircuit, transpile, qasm2
from qiskit.circuit.library import PermutationGate
import pyzx as zx

CLIFFORD_T_BASIS = ['cx', 'h', 's', 'sdg', 't', 'tdg']

class QiskitOptimizer:
    def __init__(self, optimization_level: int = 3):
        self.optimization_level = optimization_level

    def optimize(self, qc: QuantumCircuit) -> QuantumCircuit:
        optimized_qc = transpile(
            qc,
            basis_gates=CLIFFORD_T_BASIS,
            optimization_level=self.optimization_level
        )

        if optimized_qc.layout is not None:
            permutation = optimized_qc.layout.routing_permutation()
            fixed_qc = QuantumCircuit(optimized_qc.num_qubits)
            fixed_qc.compose(optimized_qc, inplace=True)
            if permutation != list(range(optimized_qc.num_qubits)):
                fixed_qc.append(PermutationGate(permutation), range(optimized_qc.num_qubits))
            optimized_qc = fixed_qc.decompose(gates_to_decompose=["permutation"])
        return optimized_qc
