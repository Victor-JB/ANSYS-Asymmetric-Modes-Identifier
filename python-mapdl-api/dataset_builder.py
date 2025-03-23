"""
This script creates a dataset of beam geometries and their corresponding modal frequencies.
Each beam has different dimensions, and the modal analysis results are saved in VTK format.
"""

from ansys.mapdl.core import launch_mapdl
from beam_generator import create_beam
from modal_analysis import run_modal_analysis

beam_configs = [
    {"length": 0.5, "width": 0.05, "height": 0.05},
    {"length": 1.0, "width": 0.1, "height": 0.05},
    {"length": 1.5, "width": 0.1, "height": 0.1},
]

mapdl = launch_mapdl(run_location="dataset_run")

for i, config in enumerate(beam_configs):
    create_beam(mapdl, **config)
    freqs = run_modal_analysis(mapdl, n_modes=3, output_dir="vtk_modes", base_filename=f"beam_{i}")
    print(f"Beam {i}: Frequencies = {freqs}")

mapdl.exit()
