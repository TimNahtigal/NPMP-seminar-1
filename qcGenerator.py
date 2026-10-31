import math
import random
from qiskit import QuantumCircuit


class QuantumCircuitGenerator:
    """Generates a random quantum circuit using Qiskit with basic and complex gates.

    The circuit is built layer by layer. In every layer each qubit gets exactly one gate,
    and multi-qubit gates act on randomly chosen (not necessarily adjacent) qubits.
    Gates in a layer never share a qubit, so qc.depth() equals `depth`
    (a ccx or swap counts as one layer, as in Qiskit's depth()).
    """

    def __init__(self, num_qubits: int, depth: int):
        self.num_qubits = num_qubits
        self.depth = depth

    def generate(self) -> QuantumCircuit:
        qc = QuantumCircuit(self.num_qubits)
        single_qubit_gates = ["h", "t", "s", "x", "rz"]

        for _ in range(self.depth):
            # Qubits that have no gate yet in this layer, in random order
            free = list(range(self.num_qubits))
            random.shuffle(free)
            while free:
                # 3-qubit gate (Toffoli) on any 3 free qubits
                if len(free) >= 3 and random.random() < 0.15:
                    qc.ccx(free.pop(), free.pop(), free.pop())
                # 2-qubit gates (CNOT or SWAP) on any 2 free qubits
                elif len(free) >= 2 and random.random() < 0.35:
                    gate_2q = random.choice(["cx", "swap"])
                    if gate_2q == "cx":
                        qc.cx(free.pop(), free.pop())
                    else:
                        qc.swap(free.pop(), free.pop())
                else:
                    # Single-qubit gates
                    q = free.pop()
                    gate = random.choice(single_qubit_gates)
                    if gate == "h":
                        qc.h(q)
                    elif gate == "t":
                        qc.t(q)
                    elif gate == "s":
                        qc.s(q)
                    elif gate == "x":
                        qc.x(q)
                    elif gate == "rz":
                        # Random multiple of pi/4, so the circuit stays in Clifford+T
                        # (an arbitrary angle has no exact T-count)
                        angle = random.randint(0, 7) * math.pi / 4
                        qc.rz(angle, q)
        return qc
