import random
from qiskit import QuantumCircuit, transpile, qasm2
from qiskit.circuit.library import PermutationGate
import pyzx as zx

# Target basis for T-count comparisons: every T gate shows up as an explicit t/tdg
CLIFFORD_T_BASIS = ['cx', 'h', 's', 'sdg', 't', 'tdg', 'x', 'z']

class QiskitOptimizer:
    """Optimizes a quantum circuit using Qiskit's built-in transpiler tools."""

    def __init__(self, optimization_level: int = 3):
        self.optimization_level = optimization_level

    def optimize(self, qc: QuantumCircuit) -> QuantumCircuit:
        # Without a basis Qiskit hides T gates inside ccx/u1/u2/u3, so target Clifford+T
        optimized_qc = transpile(
            qc,
            basis_gates=CLIFFORD_T_BASIS,
            optimization_level=self.optimization_level
        )

        # At level 2+ Qiskit deletes SWAPs and only records the qubit permutation in
        # optimized_qc.layout. Put it back as gates so the circuit is equivalent on its
        # own (also when exported to QASM). SWAPs are Clifford, so the T-count is unchanged.
        if optimized_qc.layout is not None:
            permutation = optimized_qc.layout.routing_permutation()
            fixed_qc = QuantumCircuit(optimized_qc.num_qubits)
            fixed_qc.compose(optimized_qc, inplace=True)
            if permutation != list(range(optimized_qc.num_qubits)):
                fixed_qc.append(PermutationGate(permutation), range(optimized_qc.num_qubits))
            optimized_qc = fixed_qc.decompose(gates_to_decompose=["permutation"])
        return optimized_qc
