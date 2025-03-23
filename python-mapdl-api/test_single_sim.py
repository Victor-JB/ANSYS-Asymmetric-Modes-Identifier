# File: test_single_simulation.py

from ansys.mapdl.core import launch_mapdl
from beam_generator import create_beam
from modal_analysis import run_modal_analysis
from symmetry_check import is_mode_asymmetric
from force_estimator import estimate_force_from_vtk

import os

# -------------------
# GLOBAL PARAMETERS
# -------------------
BEAM_ID = 2
RUN_DIR = f"test_runs/beam_{BEAM_ID}"
N_MODES = 3
ELEMENT_SIZE = 0.03 # meters; Element size for meshing the beam
AMPLITUDE = 0.5  # meters; Assumed modal amplitude for force estimation

# Geometry (meters)
LENGTH = 1.0
WIDTH = 0.1
HEIGHT = 0.07

# Material: Steel
MATERIAL = {
    "name": "steel",
    "EX": 2e11,     # Young's modulus (Pa)
    "PR": 0.3,      # Poisson's ratio
    "DENS": 7850    # Density (kg/m^3)
}

# -------------------
# RUN SIMULATION
# -------------------
os.makedirs(RUN_DIR, exist_ok=True)
mapdl = launch_mapdl(run_location=f"{RUN_DIR}/output", override=True, loglevel="ERROR")

create_beam(mapdl, length=LENGTH, width=WIDTH, height=HEIGHT,
            element_size=ELEMENT_SIZE, material=MATERIAL)

frequencies, vtk_paths = run_modal_analysis(
    mapdl,
    n_modes=N_MODES,
    output_dir=f"{RUN_DIR}/mode_shapes",
    base_filename=f"beam_{BEAM_ID}"
)

print("\n--- Simulation Results ---")
for mode_idx, (freq, vtk_file) in enumerate(zip(frequencies, vtk_paths), 1):
    is_asym = is_mode_asymmetric(vtk_file)
    force = estimate_force_from_vtk(vtk_file, axis="X", amplitude=AMPLITUDE)

    print(f"Mode {mode_idx}:")
    print(f"  Frequency: {freq:.2f} Hz")
    print(f"  Asymmetric: {is_asym}")
    print(f"  Estimated Force: {force:.4f} N")
    print(f"  VTK File: {vtk_file}\n")

mapdl.exit()
