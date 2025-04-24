
# File: beam_generator.py
"""
Define Parametric Beam Geometry to use with other pyMAPDL analysis files
"""

def create_beam(mapdl, length, width, height, element_size, material, mesh_dir=None):
    print("Creating beam geometry...")
    print(f"Length: {length}, Width: {width}, Height: {height}, Element Size: {element_size}")
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