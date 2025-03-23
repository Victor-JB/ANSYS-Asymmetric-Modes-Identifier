# File: symmetry_check.py
import pyvista as pv
import numpy as np

import pyvista as pv
import numpy as np

def is_mode_asymmetric(vtk_path, axis="Y", tolerance=1e-3):
    """
    Checks whether the nodal displacement field is symmetric across the specified axis.
    """
    mesh = pv.read(vtk_path)

    # Print available fields
    print("Available point data:", mesh.point_data.keys())

    # Try to find displacement vector
    if "Nodal Solution" in mesh.point_data:
        vectors = mesh.point_data["Nodal Solution"]
    else:
        raise ValueError("Displacement field not found in VTK. Available fields: " + str(mesh.point_data.keys()))

    coords = mesh.points
    axis_idx = {"X": 0, "Y": 1, "Z": 2}[axis.upper()]

    for i, coord in enumerate(coords):
        mirrored_coord = coord.copy()
        mirrored_coord[axis_idx] *= -1

        distances = np.linalg.norm(coords - mirrored_coord, axis=1)
        match_idx = np.argmin(distances)

        if distances[match_idx] > tolerance:
            continue

        diff = np.abs(vectors[i] - vectors[match_idx])
        if np.any(diff > tolerance):
            return True  # Asymmetric

    return False  # Symmetric
