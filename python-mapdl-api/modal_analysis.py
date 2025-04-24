# File: modal_analysis.py
import os

def run_modal_analysis(mapdl, n_modes=3, output_dir="mode_shapes", base_filename="beam"):
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

    mapdl.finish()

    print(f"{n_modes} found succesfully\n")
    return frequencies, vtk_paths
