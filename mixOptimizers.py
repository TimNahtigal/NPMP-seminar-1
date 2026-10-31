from qiskit import QuantumCircuit

from qcGenerator import QuantumCircuitGenerator
from pxOptimizer import PyZXOptimizer
from qiskitOptimizer import QiskitOptimizer

class QiskitThenPyZXOptimizer:
    """Optimizes a circuit using Qiskit first, then passes the result to PyZX."""

    def __init__(self, optimization_level: int = 3):
        self.qiskit_optimizer = QiskitOptimizer(optimization_level=optimization_level)
        self.pyzx_optimizer = PyZXOptimizer()

    def optimize(self, qc: QuantumCircuit) -> QuantumCircuit:
        # Step 1: Optimize with Qiskit
        qiskit_result = self.qiskit_optimizer.optimize(qc)
        # Step 2: Optimize the result with PyZX
        final_result = self.pyzx_optimizer.optimize(qiskit_result)
        return final_result


class PyZXThenQiskitOptimizer:
    """Optimizes a circuit using PyZX first, then passes the result to Qiskit.

    NOTE: uses Qiskit optimization level 1 on purpose. PyZX output is mostly runs of
    H and pi/4 phases; at level 2/3 Qiskit re-synthesizes those blocks (KAK/Euler) into
    arbitrary angles and approximates them with many T gates, so the T-count goes up
    (e.g. 21 -> 397) and the result is only approximately equal. Level 1 keeps it exact.
    """

    def __init__(self, optimization_level: int = 1):
        self.pyzx_optimizer = PyZXOptimizer()
        self.qiskit_optimizer = QiskitOptimizer(optimization_level=optimization_level)

    def optimize(self, qc: QuantumCircuit) -> QuantumCircuit:
        # Step 1: Optimize with PyZX
        pyzx_result = self.pyzx_optimizer.optimize(qc)
        # Step 2: Optimize the result with Qiskit
        final_result = self.qiskit_optimizer.optimize(pyzx_result)
        return final_result