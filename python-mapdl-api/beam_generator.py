
# File: beam_generator.py
"""
Define Parametric Beam Geometry to use with other pyMAPDL analysis files
"""

def create_beam(mapdl, length, width, height, element_size, material, cdb_dir=None):
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
    mapdl.nsel("S", "LOC", "X", 0)
    mapdl.d("ALL", "ALL")
    mapdl.allsel()

    if cdb_dir:
        # Save .cdb for later recovery (used by reaction_force_analysis)
        mapdl.cdwrite("DB", f"{cdb_dir}/beam", "cdb")

    return mapdl