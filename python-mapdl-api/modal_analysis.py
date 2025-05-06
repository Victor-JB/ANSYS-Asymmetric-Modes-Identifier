# File: modal_analysis.py
import os

# --------------------------------------------------------------------------- #
def prestressed_analysis(mapdl, pressure, inner_diam, n_modes, base_filename, output_dir="mode_shapes"):
    """
    1) static inflation at given internal pressure
    2) prestressed modal extraction (LANB)
    returns list of eigenfrequencies [Hz]
    """
    print("Running modal analysis...")
    print(f"Number of modes to extract: {n_modes}")
    r_inner = inner_diam / 2

    # --- static inflation ---
    mapdl.finish()                   # leave any POST1
    mapdl.prep7()
    mapdl.antype("STATIC")
    # apply uniform face-pressure on all internal faces
    mapdl.asel("S", "LOC", "R", 0, r_inner + 1e-6)   # select inner-surface nodes
    mapdl.sf("ALL", "PRES", pressure)
    mapdl.solve()

    # capture that prestress state
    mapdl.finish()
    mapdl.post1()
    mapdl.set(1, "LAST")             # snapshot last loadstep

    # --- prestressed modal solve ---
    mapdl.finish()
    mapdl.prep7()
    mapdl.antype("MODAL")
    mapdl.modtyp("PREST")            # do a prestress modal
    mapdl.modopt("LANB", n_modes)
    mapdl.mxpand(n_modes)            # recover full modes
    mapdl.solve()

    os.makedirs(output_dir, exist_ok=True)
    frequencies = []
    vtk_paths = []

    for mode_num in range(1, n_modes + 1):
        mapdl.set(1, mode_num)
        freq = mapdl.get_value("MODE", mode_num, "FREQ")
        frequencies.append(freq)

        vtk_file = os.path.join(output_dir, f"{base_filename}_mode_{mode_num}.vtk")
        mapdl.result.save_as_vtk(vtk_file, mode_num - 1)
        vtk_paths.append(vtk_file)

    # extract freqs
    # freqs = [mapdl.get_value("MODE", i+1, "FREQ") for i in range(n_modes)]

    print(f"{n_modes} found succesfully\n")
    return frequencies, vtk_paths

# --------------------------------------------------------------------------- #
def cold_not_prestressed_analysis(mapdl, base_filename, n_modes, output_dir="mode_shapes"):
    """
    Run a modal analysis on the pre-inflated model and save the mode shapes as VTK files.
    Args:
        mapdl: MAPDL instance
        base_filename: Base filename for output files
        n_modes: Number of modes to extract
        output_dir: Directory to save the VTK files
    Returns:
        frequencies: List of frequencies for the extracted modes
        vtk_paths: List of paths to the saved VTK files
    """
    print("Running modal analysis...")
    print(f"Number of modes to extract: {n_modes}")

    mapdl.slashsolu()
    mapdl.antype("MODAL")
    mapdl.modopt("LANB", n_modes)
    mapdl.mxpand(n_modes)
    mapdl.solve()
    mapdl.finish()

    os.makedirs(output_dir, exist_ok=True)
    frequencies = []
    vtk_paths = []

    for mode_num in range(1, n_modes + 1):
        mapdl.set(1, mode_num)
        freq = mapdl.get_value("MODE", mode_num, "FREQ")
        frequencies.append(freq)

        vtk_file = os.path.join(output_dir, f"{base_filename}_mode_{mode_num}.vtk")
        mapdl.result.save_as_vtk(vtk_file, mode_num - 1)
        vtk_paths.append(vtk_file)


    print(f"{n_modes} found succesfully\n")
    return frequencies, vtk_paths

# --------------------------------------------------------------------------- #
def run_modal_analysis(mapdl, base_filename, n_modes=3, output_dir="mode_shapes"):
    print("Running modal analysis...")
    print(f"Number of modes to extract: {n_modes}")

    mapdl.slashsolu()
    mapdl.antype("MODAL")
    mapdl.modopt("LANB", n_modes)
    mapdl.mxpand(n_modes)
    mapdl.solve()
    mapdl.finish()

    mapdl.post1()
    os.makedirs(output_dir, exist_ok=True)
    frequencies = []
    vtk_paths = []

    for mode_num in range(1, n_modes + 1):
        mapdl.set(1, mode_num)
        freq = mapdl.get_value("MODE", mode_num, "FREQ")
        frequencies.append(freq)

        vtk_file = os.path.join(output_dir, f"{base_filename}_mode_{mode_num}.vtk")
        mapdl.result.save_as_vtk(vtk_file, mode_num - 1)
        vtk_paths.append(vtk_file)

    print(f"{n_modes} found succesfully\n")
    return frequencies, vtk_paths
