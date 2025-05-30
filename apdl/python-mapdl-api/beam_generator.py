
# File: beam_generator.py
"""
Define Parametric Beam Geometry to use with other pyMAPDL analysis files
"""

# --------------------------------------------------------------------------- #
# Updated: modeling a flexible McKibben-type arm instead of a beam
def create_mckibben_tube(mapdl, length, outer_diameter, inner_diameter, 
                         material, n_through=6, mesh_dir=None, fix_both_ends=True, n_circ=32, n_len=40):
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
    print(f"Length: {length}, Outer diam: {outer_diameter}, Inner diam: {inner_diameter}, Number elements through wall: {n_through}")
    print("Material Properties: ")
    print(f"EX: {material['EX']}, PR: {material['PR']}, DENS: {material['DENS']}")
    print(f"Fix both ends: {fix_both_ends}")
    
    mapdl.clear()
    # 1) make sure we’re in PREP7
    mapdl.finish()
    mapdl.prep7()

    # Material
    # mapdl.mp("EX", 1, material["EX"])
    # mapdl.mp("PRXY", 1, material["PR"])

    #q: how do I have whatever material setting here be the same as one I set in dict?
    mapdl.tb("MOONEY", 1, "", 2)      # 2 Mooney terms
    # term 1: C10, D1
    mapdl.tbdata(1, 0.5, 0.02)         # example C10=0.5 MPa, D1=0.02
    # term 2: C20, D2
    mapdl.tbdata(2, 0.1, 0.01)         # example C20=0.1 MPa, D2=0.01

    # turn on large‐deformation geometrical nonlinearity
    mapdl.nlgeom("ON")
    
    mapdl.mp("DENS", 1, material["DENS"])

    """
    Note: SOLID186 is a 3D 20-node structural solid element. It is used for modeling 3D structures with large deformations and nonlinear material behavior.
    SOLID185 is a linear 8-node brick. For curved, hyperelastic bodies a 10-node tetra (SOLID186) often gives better accuracy in bending modes.
    """
    # Element type
    mapdl.et(1, "SOLID186")

    # ── geometry ───────────────────────────────────────────────
    r_o, r_i = outer_diameter / 2, inner_diameter / 2
    mapdl.cylind(r_i, r_o, z1=0, z2=length)

    # ── mesh controls ──────────────────────────────────────────
    mapdl.mshape(1, "3D")               # enable sweep brick
    mapdl.mshkey(1)                     # let ANSYS detect sweep source/target

    # Radial division (wall thickness)
    t = r_o - r_i
    esize_r = t / float(n_through)
    mapdl.esize(esize_r)

    # Circumferential and axial edge divisions (optional, for regularity)
    mapdl.lsel("S", "LOC", "Z", 0)      # select end cap lines
    mapdl.lesize("ALL", "", n_circ)     # n_circ quads around circumference
    mapdl.allsel()

    mapdl.lsel("S", "LOC", "R", r_o, r_o, 1e-4)   # ‘R’, not ‘RAD’
    mapdl.lesize("ALL", "", n_len)
    mapdl.allsel()

    # ── sweep‑mesh the volume ──────────────────────────────────
    mapdl.vmesh("ALL", 1)               # 1 = sweep hex bric

    # ── boundary conditions ────────────────────────────────────
    if fix_both_ends:
        mapdl.nsel("S", "LOC", "Z", 0, tol=1e-6)
        mapdl.d("ALL", "ALL")
        mapdl.nsel("S", "LOC", "Z", length, tol=1e-6)
        mapdl.d("ALL", "ALL")
    else:
        mapdl.nsel("S", "LOC", "Z", 0, tol=1e-6)
        mapdl.d("ALL", "ALL")

    mapdl.allsel()
    mapdl.finish() # finish prep7

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

# --------------------------------------------------------------------------- #
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