from ansys.mapdl.core import launch_mapdl
import numpy as np
import os

# having to set environment variable for MAPDL executable path because 'exec_path' arg doesn't exist anymore
# os.environ["MAPDL_EXEC"] = r"C:\Program Files\ANSYS Inc\ANSYS Student\v251\ansys\bin\winx64\ANSYS251.exe"
# just kidding it works now

# mapdl = launch_mapdl(run_location="beam_run", loglevel="ERROR")
mapdl = launch_mapdl(run_location="beam_run", override=True)

# print(mapdl) # info on the instance, version, license, etc.
 
# Start MAPDL
mapdl.clear()
mapdl.prep7()

# Material properties
mapdl.mp("EX", 1, 2e11)     # Young's modulus (Pa)
mapdl.mp("PRXY", 1, 0.3)    # Poisson’s ratio
mapdl.mp("DENS", 1, 7850)   # Density (kg/m^3)

# Element type
mapdl.et(1, "SOLID185")

# Geometry: 1m long, 0.1m x 0.1m cross-section
mapdl.blc4(0, 0, 1, 0.1, 0.1)

# Mesh
mapdl.esize(0.05)
mapdl.vmesh("ALL")

# Constraints: fix face at x=0
mapdl.nsel("S", "LOC", "X", 0)
mapdl.d("ALL", "ALL")
mapdl.allsel()

# Modal analysis
mapdl.finish()
mapdl.slashsolu()
mapdl.antype("MODAL")
mapdl.modopt("LANB", 3)   # 3 modes
mapdl.mxpand(3)
mapdl.solve()
mapdl.finish()

# Postprocessing
mapdl.post1()
frequencies = []

# Output folder
output_dir = "mode_shapes"
os.makedirs(output_dir, exist_ok=True)

for mode_num in range(1, 4):
    mapdl.set(1, mode_num)
    freq = mapdl.get_value("MODE", mode_num, "FREQ")
    frequencies.append(freq)

    # Save mode shape as VTK
    vtk_path = os.path.join(output_dir, f"mode_{mode_num}.vtk")
    mapdl.result.save_as_vtk(vtk_path, mode_num)

    print(f"Mode {mode_num}: {freq:.2f} Hz → saved to {vtk_path}")

mapdl.exit()
