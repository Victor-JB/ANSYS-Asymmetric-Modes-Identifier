"""
This script creates a dataset of beam geometries and their corresponding modal frequencies.
Each beam has different dimensions, and the modal analysis results are saved in VTK format.
"""

# File: dataset_builder.py
import os
import numpy as np
import pandas as pd
from datetime import datetime
from ansys.mapdl.core import launch_mapdl
from beam_generator import create_beam
from modal_analysis import run_modal_analysis
from symmetry_check import is_mode_asymmetric
from force_estimator import estimate_force

# --- Configurable Parameters ---
NUM_MODES = 3
ELEMENT_SIZE = 0.05

# Example material definitions
materials = [
    {"name": "steel", "EX": 2e11, "PR": 0.3, "DENS": 7850},
    {"name": "aluminum", "EX": 7e10, "PR": 0.33, "DENS": 2700},
]

# Example geometry sweep
lengths = np.linspace(0.5, 1.5, 3)
widths = np.linspace(0.05, 0.15, 3)
heights = np.linspace(0.05, 0.15, 3)

# Storage
records = []

# --- Loop Through All Configs ---
beam_id = 0

for mat in materials:
    for L in lengths:
        for W in widths:
            for H in heights:
                run_dir = f"runs/beam_{beam_id}"
                os.makedirs(run_dir, exist_ok=True)

                mapdl = launch_mapdl(run_location=run_dir, override=True, loglevel="ERROR")
                create_beam(mapdl, length=L, width=W, height=H, element_size=ELEMENT_SIZE, material=mat)
                freqs, vtk_paths = run_modal_analysis(mapdl, n_modes=NUM_MODES, base_filename=f"beam_{beam_id}", output_dir=f"{run_dir}/mode_shapes",)
                
                for mode_idx, (f, vtk_path) in enumerate(zip(freqs, vtk_paths), 1):
                    is_asym = is_mode_asymmetric(vtk_path)
                    force = estimate_force(freq=f, mass=mat['DENS'], amplitude=0.001)

                    records.append({
                        "beam_id": beam_id,
                        "material": mat['name'],
                        "EX": mat['EX'],
                        "PR": mat['PR'],
                        "DENS": mat['DENS'],
                        "L": L,
                        "W": W,
                        "H": H,
                        "mode": mode_idx,
                        "frequency": f,
                        "asymmetric": is_asym,
                        "force": force,
                        "vtk_path": vtk_path
                    })

                mapdl.exit()
                beam_id += 1

# --- Save dataset to CSV and NPZ ---
# Save dataset
os.makedirs("dataset", exist_ok=True)
df = pd.DataFrame(records)
df.to_csv("dataset/asymmetric_mode_dataset.csv", index=False)

# Also save .npz for ML
np.savez_compressed("dataset/asymmetric_mode_dataset.npz",
    X=df[["EX", "PR", "DENS", "L", "W", "H", "mode"]].values,
    y_force=df["force"].values,
    y_freq=df["frequency"].values,
    y_asym=df["asymmetric"].astype(int).values
)

# Load the dataset for verification
np.load("asymmetric_mode_dataset.npz")
