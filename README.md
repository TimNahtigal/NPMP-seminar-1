# PyZX proti Qiskit: primerjava optimizatorjev T-vrat

Projekt na naključnih Clifford+T vezjih primerja zmanjšanje števila T-vrat pri optimizatorjih Qiskit, PyZX in njuni kombinaciji (Qiskit → PyZX, PyZX → Qiskit). Merimo število T-vrat, skupno število vrat, število dvokubitnih vrat in čas izvajanja.

## Zagon

```bash
python -m venv venv
venv\Scripts\activate        # Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
```

Nato odprite `main.ipynb` (npr. v VS Code z izbranim `venv` jedrom) in zaženite celice po vrsti. Rezultati se shranijo v `results/<časovni žig>/`, grafi pa se izrišejo iz shranjenega `results.json`.
