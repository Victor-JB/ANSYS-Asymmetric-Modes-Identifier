from ansys.mapdl.core import launch_mapdl
import numpy as np
import os

# having to set environment variable for MAPDL executable path because 'exec_path' arg doesn't exist anymore
# os.environ["MAPDL_EXEC"] = r"C:\Program Files\ANSYS Inc\ANSYS Student\v251\ansys\bin\winx64\ANSYS251.exe"
# just kidding it works now

# mapdl = launch_mapdl(run_location="beam_run", loglevel="ERROR")
mapdl = launch_mapdl(run_location="beam_run", override=True)

# print(mapdl) # info on the instance, version, license, etc.

###############################################################################
# 2. Preprocessing
###############################################################################
mapdl.clear()
mapdl.prep7()

# -- Define material properties (Steel) --
#    Young’s modulus, Poisson’s ratio, density
mapdl.mp('EX', 1, 2.0e11)    # Pa
mapdl.mp('NUXY', 1, 0.3)
mapdl.mp('DENS', 1, 7850)    # kg/m^3

# -- Define geometry --
#    For simplicity, create a rectangular “block” as a beam of length L
#    with small cross-section (W x H).
L = 1.0    # length (m)
W = 0.01   # width  (m)
H = 0.01   # height (m)

mapdl.block(0, L, 0, W, 0, H)

# -- Mesh the volume --
#    For a simple demonstration, use a 3D structural solid element (SOLID185).
mapdl.et(1, 185)     # 3-D 8-Node Structural Solid
mapdl.esize(0.02)    # element size ~ 2 cm
mapdl.vmesh('ALL')   # mesh the entire volume

###############################################################################
# 3. Apply Boundary Conditions
###############################################################################
# Fix both ends of the beam in all DOF.
#   - “Left” end at X = 0
#   - “Right” end at X = L
mapdl.nsel('S', 'LOC', 'X', 0.0)
mapdl.d('ALL', 'ALL', 0.0)
mapdl.nsel('S', 'LOC', 'X', L)
mapdl.d('ALL', 'ALL', 0.0)

# Re-select everything
mapdl.allsel()

###############################################################################
# 4. Modal Analysis
###############################################################################
mapdl.run('/SOLU')
mapdl.antype('MODAL')
# Choose a mode extraction method and number of modes.
#  E.g. "LANB" (Lanczos) extracting first 6 modes
mapdl.modopt('LANB', 6)
mapdl.solve()
mapdl.finish()

###############################################################################
# 5. Post-processing
###############################################################################
mapdl.post1()

# Extract the frequencies for each mode set.
frequencies = []
num_modes = 6
for mode_idx in range(1, num_modes + 1):
    # The SET command selects which mode shape to read in POST1
    mapdl.set(mode_idx, 1)
    freq = mapdl.get("FREQ", "ACTIVE", 0, "FREQ")
    frequencies.append(freq)

print("Extracted natural frequencies (Hz):", frequencies)

# Optionally, retrieve nodal displacements for each mode
# into a Python structure. The 'result' object can also
# be used for advanced queries such as stress, strain, etc.
result = mapdl.result
all_mode_shapes = []
for mode_idx in range(num_modes):
    # Nodal solution for each mode (0-based indexing in `result`)
    nodal_displacements = result.nodal_displacement(mode_idx)
    all_mode_shapes.append(nodal_displacements)

# Just an example: print the first 5 nodes of the first mode shape
print("Mode 1, first 5 nodes' displacements:\n", all_mode_shapes[0][:5])

###############################################################################
# 6. Clean up / exit
###############################################################################
mapdl.exit()

# frequencies now contains the natural frequencies in a Python list,
# and all_mode_shapes holds the nodal displacements for each mode.
# You can feed these into your ML pipeline as needed.
