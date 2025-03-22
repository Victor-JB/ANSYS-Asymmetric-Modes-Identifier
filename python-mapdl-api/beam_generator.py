"""
Define Parametric Beam Geometry to use with other pyMAPDL analysis files
"""

def create_beam(mapdl, length=1.0, width=0.1, height=0.1, element_size=0.05):
    mapdl.clear()
    mapdl.prep7()

    # Material properties
    mapdl.mp("EX", 1, 2e11)
    mapdl.mp("PRXY", 1, 0.3)
    mapdl.mp("DENS", 1, 7850)

    # Element type
    mapdl.et(1, "SOLID185")

    # Geometry
    mapdl.blc4(0, 0, length, width, height)

    # Mesh
    mapdl.esize(element_size)
    mapdl.vmesh("ALL")

    # Boundary conditions
    mapdl.nsel("S", "LOC", "X", 0)
    mapdl.d("ALL", "ALL")
    mapdl.allsel()
