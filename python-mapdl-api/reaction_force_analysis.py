# File: reaction_force_analysis.py
from ansys.mapdl.core import launch_mapdl
import numpy as np
import os

def apply_modal_bc_and_get_reaction_force(
    mode_shape_vtk,
    base_model_dir,
    amplitude=0.001,
    axis="X",
    exec_path=None
):
    """
    Run static analysis with modal displacement as prescribed BC to extract reaction force.
    """
    import pyvista as pv

    mesh = pv.read(mode_shape_vtk)

    # Extract displacement field
    for name in mesh.point_data:
        if mesh.point_data[name].ndim == 2 and mesh.point_data[name].shape[1] == 3:
            vectors = mesh.point_data[name] * amplitude
            break
    else:
        raise ValueError("No 3D vector field found in VTK.")

    coords = mesh.points
    axis_idx = {"X": 0, "Y": 1, "Z": 2}[axis.upper()]
    min_axis_val = np.min(coords[:, axis_idx])
    mask = np.abs(coords[:, axis_idx] - min_axis_val) < 1e-5
    selected_nodes = np.where(mask)[0]

    # Create new analysis folder
    analysis_dir = os.path.join(base_model_dir, "reaction_force")
    os.makedirs(analysis_dir, exist_ok=True)
    mapdl = launch_mapdl(run_location=analysis_dir, override=True, loglevel="ERROR", exec_path=exec_path)

    # Restore previous geometry/mesh
    cdb_path = os.path.join(base_model_dir, "beam.cdb")
    if not os.path.exists(cdb_path):
        raise FileNotFoundError("Expected beam.cdb not found for restoring geometry.")

    mapdl.clear()
    mapdl.input(cdb_path)
    mapdl.finish()

    # Apply modal displacement as BC
    mapdl.prep7()
    mapdl.nsel("NONE")
    for idx, node in enumerate(selected_nodes):
        mapdl.nsel("S", "NODE", "", node + 1)  # MAPDL node indexing is 1-based
        ux, uy, uz = vectors[node]
        mapdl.d("", "UX", ux)
        mapdl.d("", "UY", uy)
        mapdl.d("", "UZ", uz)
    mapdl.allsel()
    mapdl.finish()

    # Solve static case
    mapdl.slashsolu()
    mapdl.antype("STATIC")
    mapdl.solve()
    mapdl.finish()

    # Postprocessing: get total reaction force at constrained nodes
    mapdl.post1()
    mapdl.fsum("ALL")
    fx = mapdl.get_value("FSUM", 0, "ITEM", "FX")
    fy = mapdl.get_value("FSUM", 0, "ITEM", "FY")
    fz = mapdl.get_value("FSUM", 0, "ITEM", "FZ")

    mapdl.exit()
    return np.linalg.norm([fx, fy, fz]), fx, fy, fz
