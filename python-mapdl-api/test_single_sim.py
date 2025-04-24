# File: test_single_simulation.py

import argparse
import os
from ansys.mapdl.core import launch_mapdl
from beam_generator import create_beam
from modal_analysis import run_modal_analysis
from symmetry_check import is_mode_asymmetric
from force_estimator import estimate_force_from_vtk
from reaction_force_analysis import apply_modal_bc_and_get_reaction_force

# -------------------
# GLOBAL PARAMETERS
# -------------------
BEAM_ID = 1
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
    "DENS": 3000    # Density (kg/m^3)
}

# -------------------
# MAIN EXECUTION
# -------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--accurate-force", action="store_true",
                        help="Use reaction force analysis instead of vector-based estimate.")
    args = parser.parse_args()

    os.makedirs(RUN_DIR, exist_ok=True)
    print("Attempting to launch MAPDL...")
    mapdl = launch_mapdl(run_location=f"{RUN_DIR}/output", override=True, loglevel="ERROR")
    print("MAPDL launched successfully!")
    
    try:
        create_beam(mapdl, length=LENGTH, width=WIDTH, height=HEIGHT,
                    element_size=ELEMENT_SIZE, material=MATERIAL, mesh_dir=f"{RUN_DIR}/mode_shapes")

        frequencies, vtk_paths = run_modal_analysis(
            mapdl,
            n_modes=N_MODES,
            output_dir=f"{RUN_DIR}/mode_shapes",
            base_filename=f"beam_{BEAM_ID}"
        )

        print("\n--- Simulation Results ---")
        for mode_idx, (freq, vtk_file) in enumerate(zip(frequencies, vtk_paths), 1):
            is_asym = is_mode_asymmetric(vtk_file)

            if args.accurate_force:
                force, fx, fy, fz = apply_modal_bc_and_get_reaction_force(
                    mode_shape_vtk=vtk_file,
                    base_model_dir=RUN_DIR,
                    amplitude=AMPLITUDE,
                    axis="X"
                )
                print(f"Mode {mode_idx}:")
                print(f"  Frequency: {freq:.2f} Hz")
                print(f"  Asymmetric: {is_asym}")
                print(f"  Reaction Force: {force:.4f} N (fx={fx:.2f}, fy={fy:.2f}, fz={fz:.2f})")
                print(f"  VTK File: {vtk_file}\n")
            else:
                force = estimate_force_from_vtk(vtk_file, axis="X", amplitude=AMPLITUDE)
                print(f"Mode {mode_idx}:")
                print(f"  Frequency: {freq:.2f} Hz")
                print(f"  Asymmetric: {is_asym}")
                print(f"  Estimated Force: {force:.4f} N")
                print(f"  VTK File: {vtk_file}\n")
    except Exception as e:
        print(f"Error during simulation: {e}")
    finally:
        # Clean up and exit MAPDL
        mapdl.finish()
        mapdl.clear()   

    mapdl.exit()
