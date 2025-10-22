
# ANSYS Asymmetric Modes Identifier

A fully head‑less pyGeometry, pyPrimeMesh, and pyMAPDL pipeline that **generates large parametric fleets of soft‑robotic beam/tube geometries, meshes them, performs prestressed modal analyses, and exports asymmetric&nbsp;+ symmetric mode data** with the end goal being to create an ml model which takes in an asymmetric mode and outputs a structure (material, configuration) and the required frequency.

![Meshed Beam Example PNG](interesting_results_beam_meshed.png)

---

## ✨ Key Features
| Stage | Toolkit | What Happens |
|-------|---------|--------------|
| Geometry | **`ansys-geometry-core`** | Procedurally build tubes, splines, braided sleeves&nbsp;… every numerical input is a Python variable so you can loop over \(L, \; r_\text{inner}, \; p_\text{braid},\dots\). |
| Meshing | **`ansys-meshing-prime`** | Fast, stateless tet / hex‑core mesher with size controls and quality checks. |
| Solver | **`ansys-mapdl-core`** | (1) Nonlinear static inflation to capture prestress → (2) Linear perturbation modal solve. |
| Post | **`ansys-dpf-core`** | Field extraction to `.vtk`, symmetry tagging, `.npz` dataset assembly. |

Everything is **driven from Python scripts** so you can farm thousands of design points on a cluster or laptop.

---

## 🗂️ (TBD) Repository Layout
```
ansys‑asymmetric‑modes/
│
├─ geometry/          # param‑scriptable CAD builders
│   └─ beam_generator.py
├─ meshing/
│   └─ prime_mesher.py
├─ solving/
│   └─ modal_analysis.py
├─ post/
│   ├─ symmetry_check.py
│   └─ dataset_builder.py
├─ examples/          # one‑click demos
└─ README.md
```

---

## 🔧 Installation

```bash
# core toolchain
pip install ansys-geometry-core ansys-meshing-prime ansys-mapdl-core ansys-dpf-core

# extras for data and visualization
pip install numpy scipy vedo tqdm
```

> **Licenses:** You still need valid Ansys licenses for Geometry Core, Prime Server, and MAPDL on the machine or license server you run against.

---

## 🚀 Quick‑start: One variant

```bash
python examples/run_single_variant.py \
       --length 0.15  --outer-radius 0.01 \
       --wall-thickness 1.5e-3 \
       --material silicone_dragon_skin
```

The script will:
1. launch Geometry Core, generate the tube,
2. call Prime Mesh for a tet mesh,
3. hand off the mesh to MAPDL,
4. inflate to 200 kPa, solve the first 20 modes,
5. write results to `outputs/L150_R10_v01/`.

Open any `mode_*.vtk` in ParaView to visualise the shapes.

---

## ⚙️ Parameter Sweeps

`dataset_builder.py` takes a JSON or CSV grid:

```json
[
  { "length":0.15, "outer_radius":0.01, "pressure":200000 },
  { "length":0.20, "outer_radius":0.012, "pressure":250000 }
]
```

```bash
python post/dataset_builder.py sweep.json --n-workers 8
```

Outputs a single `dataset.npz` with arrays:

| key | shape | description |
|-----|-------|-------------|
| `freq` | (N, k) | natural frequencies (Hz) |
| `modes` | (N, k, n_nodes, 3) | mode‑shape displacement vectors |
| `sym` | (N, k) | 0 = symmetric, 1 = asymmetric |

---

## 🧩 Extending the Pipeline

* **New geometry** → drop a function in `geometry/`.
* **Alternative mesher** → point `prime_mesher.py` to a different `.x_t`.
* **Extra post‑metrics** → add a DPF operator in `post/metrics.py`.

---

## 📄 License

This repository is released under the MIT License (see `LICENSE`).

---

## 🤝 Contributing

Bug reports, pull requests, and feature suggestions are welcome!  
Open an issue or ping **@Victor‑JB** on GitHub.

---
