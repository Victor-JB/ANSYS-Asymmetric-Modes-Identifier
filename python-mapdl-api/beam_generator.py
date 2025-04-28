
# File: beam_generator.py
"""
Define Parametric Beam Geometry to use with other pyMAPDL analysis files
"""

# Updated: modeling a flexible McKibben-type arm instead of a beam
def create_mckibben_tube(mapdl, length, outer_diameter, inner_diameter, element_size, material, mesh_dir=None, fix_both_ends=True):
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
    print("Creating arm geometry...")
    print(f"Length: {length}, Outer diam: {outer_diameter}, Inner diam: {inner_diameter}, Element Size: {element_size}")
    print("Material Properties: ")
    print(f"EX: {material['EX']}, PR: {material['PR']}, DENS: {material['DENS']}")
    print(f"Fix both ends: {fix_both_ends}")
    
    mapdl.clear()
    mapdl.prep7()

    # Material
    mapdl.mp("EX", 1, material["EX"])
    mapdl.mp("PRXY", 1, material["PR"])
    mapdl.mp("DENS", 1, material["DENS"])

    # Element type
    mapdl.et(1, "SOLID185")

    # Geometrical parameters
    r_outer = outer_diameter / 2
    r_inner = inner_diameter / 2

    # Create solid outer cylinder
    mapdl.cyl4(0, 0, r_outer, length)

    # Create solid inner cylinder
    mapdl.cyl4(0, 0, r_inner, length)

    # Subtract inner cylinder from outer cylinder
    mapdl.vsbv(1, 2)

    # Mesh
    mapdl.esize(element_size)
    mapdl.vmesh("ALL")

    # Boundary conditions
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