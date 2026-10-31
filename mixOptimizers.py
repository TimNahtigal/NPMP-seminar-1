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
    def __init__(self, optimization_level: int = 1): # optimization_level is 1 for a reason
        self.pyzx_optimizer = PyZXOptimizer()
        self.qiskit_optimizer = QiskitOptimizer(optimization_level=optimization_level)

    def optimize(self, qc: QuantumCircuit) -> QuantumCircuit:
        pyzx_result = self.pyzx_optimizer.optimize(qc)
        final_result = self.qiskit_optimizer.optimize(pyzx_result)
        return final_result