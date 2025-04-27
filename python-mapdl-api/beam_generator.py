
# File: beam_generator.py
"""
Define Parametric Beam Geometry to use with other pyMAPDL analysis files
"""

# Updated: modeling a flexible McKibben-type arm instead of a beam

import os
from ansys.mapdl.core import launch_mapdl

def create_mckibben_tube(mapdl, length, outer_diameter, inner_diameter, element_size, material, mesh_dir=None, fix_both_ends=False):
    """
    Create a soft robotic tube approximating a McKibben actuator outer bladder.

    Args:
        mapdl: MAPDL instance
        length: Total length (m)
        outer_diameter: Outer diameter (m)
        inner_diameter: Inner diameter (m)
        element_size: Target mesh element size (m)
        material: Dictionary with 'EX', 'PR', 'DENS'
        mesh_dir: Directory to save mesh files (optional)
        fix_both_ends: Whether to fix both ends or just one
    """
    mapdl.clear()
    mapdl.prep7()

    # Material
    mapdl.mp("EX", 1, material["EX"])
    mapdl.mp("PRXY", 1, material["PR"])
    mapdl.mp("DENS", 1, material["DENS"])

    # Element type
    mapdl.et(1, "SOLID185")

    # Create hollow cylinder (tube)
    mid_radius = (outer_diameter + inner_diameter) / 4  # average radius / 2
    thickness = (outer_diameter - inner_diameter) / 2

    mapdl.cylind(length, mid_radius - thickness, mid_radius + thickness)

    # Mesh
    mapdl.esize(element_size)
    mapdl.vmesh("ALL")

    # Boundary conditions
    mapdl.nsel("S", "LOC", "Z", 0)
    mapdl.d("ALL", "ALL")

    if fix_both_ends:
        mapdl.nsel("S", "LOC", "Z", length)
        mapdl.d("ALL", "ALL")

    mapdl.allsel()
    mapdl.finish()

    if mesh_dir:
        os.makedirs(mesh_dir, exist_ok=True)
        mapdl.cdwrite("DB", os.path.join(mesh_dir, "tube_mesh"), "cdb")

# -------------------
# TEST SINGLE SIM SCRIPT
# -------------------

if __name__ == "__main__":
    BEAM_ID = 0
    RUN_DIR = f"test_runs/tube_{BEAM_ID}"
    N_MODES = 3
    ELEMENT_SIZE = 0.02  # meters
    FIX_BOTH_ENDS = False

    # Tube geometry
    LENGTH = 0.3
    OUTER_DIAMETER = 0.04
    INNER_DIAMETER = 0.03

    # Material: soft silicone
    MATERIAL = {
        "name": "silicone",
        "EX": 1e6,    # Young's modulus (Pa)
        "PR": 0.49,   # Poisson's ratio (nearly incompressible)
        "DENS": 1100  # Density (kg/m^3)
    }

    os.makedirs(RUN_DIR, exist_ok=True)
    mapdl = launch_mapdl(run_location=f"{RUN_DIR}/output", override=True, loglevel="ERROR")

    create_mckibben_tube(mapdl, length=LENGTH,
                         outer_diameter=OUTER_DIAMETER,
                         inner_diameter=INNER_DIAMETER,
                         element_size=ELEMENT_SIZE,
                         material=MATERIAL,
                         mesh_dir=RUN_DIR,
                         fix_both_ends=FIX_BOTH_ENDS)

    # You can now continue to run modal analysis or harmonic analysis on this geometry!

    mapdl.exit()

def create_beam(mapdl, length, width, height, element_size, material, mesh_dir=None, fix_both_ends=False):
    print("Creating beam geometry...")
    print(f"Length: {length}, Width: {width}, Height: {height}, Element Size: {element_size}")
    print("Material Properties: ")
    print(f"EX: {material['EX']}, PR: {material['PR']}, DENS: {material['DENS']}")
    print(f"Fix both ends: {fix_both_ends}")

    mapdl.clear()
    mapdl.prep7()

    # Material properties
    mapdl.mp("EX", 1, material["EX"])
    mapdl.mp("PRXY", 1, material["PR"])
    mapdl.mp("DENS", 1, material["DENS"])

    # Element type
    mapdl.et(1, "SOLID185")

    # Geometry
    mapdl.blc4(0, 0, length, width, height)

    # Mesh
    mapdl.esize(element_size)
    mapdl.vmesh("ALL")

    # Constraints: Fix face at x=0
    if fix_both_ends:
        mapdl.nsel("S", "LOC", "X", length)
        mapdl.d("ALL", "ALL")
    else:
        mapdl.nsel("S", "LOC", "X", 0)
        mapdl.d("ALL", "ALL")

    
    mapdl.allsel()

    mapdl.finish()

    print("Beam geometry created successfully!\n")

    if mesh_dir:
        try:
            print("Saving CDB file...")

            # Save .cdb for later recovery (used by reaction_force_analysis)
            mapdl.cdwrite("DB", f"{mesh_dir}/beam_mesh.cdb", "cdb")
            print("CDB file saved successfully!\n")

        except Exception as e:
            print(f"Error saving CDB file: {e}\n")


    return mapdl