
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

    return mapdl

def generate_configs(materials, lengths, widths, heights):
    configs = []
    for mat in materials:
        for L in lengths:
            for W in widths:
                for H in heights:
                    configs.append({
                        "material": mat,
                        "length": L,
                        "width": W,
                        "height": H,
                    })
    return configs