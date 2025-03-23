
# File: beam_generator.py
"""
Define Parametric Beam Geometry to use with other pyMAPDL analysis files
"""

def create_beam(mapdl, length, width, height, element_size, material):
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

    # Export geometry to MAPDL commands file
    mapdl.cdwrite("DB", f"beam_export_{material['name']}_{length:.2f}_{width:.2f}_{height:.2f}", "cdb")


    return mapdl