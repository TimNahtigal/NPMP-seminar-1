"""Funkcije za obdelavo enega vezja.

Ločeno od zvezka, da jih lahko procesi (ProcessPoolExecutor, na Windows 'spawn') uvozijo.
"""
import os
import random
import time

from qiskit import QuantumCircuit, qasm2, transpile

from qcGenerator import QuantumCircuitGenerator
from pxOptimizer import PyZXOptimizer
from qiskitOptimizer import CLIFFORD_T_BASIS, QiskitOptimizer
from mixOptimizers import PyZXThenQiskitOptimizer, QiskitThenPyZXOptimizer


def make_optimizers(qiskit_level: int) -> dict:
    return {
        "Qiskit only": QiskitOptimizer(optimization_level=qiskit_level),
        "PyZX only": PyZXOptimizer(),
        "Qiskit -> PyZX": QiskitThenPyZXOptimizer(optimization_level=qiskit_level),
        "PyZX -> Qiskit": PyZXThenQiskitOptimizer(),
    }


def gate_metrics(qc: QuantumCircuit) -> dict:
    decomposed = transpile(qc, basis_gates=CLIFFORD_T_BASIS, optimization_level=0)
    ops = decomposed.count_ops()
    total = sum(ops.values())
    t_count = ops.get("t", 0) + ops.get("tdg", 0)
    return {
        "total_gates": total,
        "t_count": t_count,
        "clifford_gates": total - t_count,  # baza je Clifford+T, vse razen T/Tdg je Cliffordovo vrata
        "two_qubit_gates": ops.get("cx", 0),
        "circuit_depth": decomposed.depth(),
    }


def file_name(method: str) -> str:
    return method.lower().replace(" -> ", "_then_").replace(" ", "_") + ".qasm"


def ratio_metrics(time_s: float, t_reduction_pct: float, n: int, d: int) -> dict:
    # d je parameter globine generatorja (število plasti vrat)
    return {
        "time_per_qubit_s": time_s / n,
        "time_per_depth_s": time_s / d,
        "t_reduction_pct": t_reduction_pct,
        "t_reduction_pct_per_qubit": t_reduction_pct / n,
        "t_reduction_pct_per_depth": t_reduction_pct / d,
    }


def benchmark_circuit(sweep: str, n: int, d: int, i: int, circuit_seed: int, circuit_dir: str,
                      qiskit_level: int) -> list:
    # Vsak klic je neodvisen (lasten seed, lastna mapa, lastni optimizatorji), zato ga lahko izvaja ločen proces.
    random.seed(circuit_seed)
    optimizers = make_optimizers(qiskit_level)
    circuit = QuantumCircuitGenerator(num_qubits=n, depth=d).generate()
    os.makedirs(circuit_dir, exist_ok=True)
    qasm2.dump(circuit, os.path.join(circuit_dir, "original.qasm"))
    original = gate_metrics(circuit)
    base = {"sweep": sweep, "qubits": n, "depth": d, "circuit": i, "seed": circuit_seed}
    rows = [{**base, "method": "Original", "time_s": 0.0, "t_removed": 0, **original,
             **ratio_metrics(0.0, 0.0, n, d)}]

    for name, optimizer in optimizers.items():
        # time_s je samo optimizacija, brez shranjevanja
        start = time.perf_counter()
        optimized = optimizer.optimize(circuit)
        elapsed = time.perf_counter() - start
        qasm2.dump(optimized, os.path.join(circuit_dir, file_name(name)))
        optimized_metrics = gate_metrics(optimized)
        t_reduction_pct = (100 * (original["t_count"] - optimized_metrics["t_count"]) / original["t_count"]
                           if original["t_count"] else 0.0)
        rows.append({**base, "method": name, "time_s": elapsed,
                     "t_removed": original["t_count"] - optimized_metrics["t_count"],
                     **optimized_metrics, **ratio_metrics(elapsed, t_reduction_pct, n, d)})
    return rows
