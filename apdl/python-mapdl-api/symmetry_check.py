# File: symmetry_check.py
import pyvista as pv
import numpy as np

def classify_symmetry(vtk_path, axis="Y", relative_tol=0.05):
    """
    Classify the mode shape in a VTK file as 'symmetric', 'antisymmetric', or 'asymmetric'
    relative to the specified mirror axis ('X', 'Y', or 'Z').
    """
    mesh = pv.read(vtk_path)

    # Auto-detect vector field
    for name in mesh.point_data:
        if mesh.point_data[name].ndim == 2 and mesh.point_data[name].shape[1] == 3:
            vectors = mesh.point_data[name]
            mesh.point_data.active_vectors_name = name
            break
    else:
        raise ValueError("No 3D vector field found in VTK. Fields: " + str(mesh.point_data.keys()))

    coords = mesh.points
    axis_idx = {"X": 0, "Y": 1, "Z": 2}[axis.upper()]

    max_disp = np.max(np.linalg.norm(vectors, axis=1))
    adaptive_tol = relative_tol * max_disp

    symmetry_status = []

    for i, coord in enumerate(coords):
        mirrored_coord = coord.copy()
        mirrored_coord[axis_idx] *= -1

        distances = np.linalg.norm(coords - mirrored_coord, axis=1)
        match_idx = np.argmin(distances)

        if distances[match_idx] > adaptive_tol:
            continue  # No valid mirrored point

        direct_diff = np.abs(vectors[i] - vectors[match_idx])
        flipped_diff = np.abs(vectors[i] + vectors[match_idx])

        if np.all(direct_diff < adaptive_tol):
            symmetry_status.append("symmetric")
        elif np.all(flipped_diff < adaptive_tol):
            symmetry_status.append("antisymmetric")
        else:
            return "asymmetric"

    return "symmetric" if all(s == "symmetric" for s in symmetry_status) else "antisymmetric"

# Backward-compatible alias

def is_mode_asymmetric(vtk_path, axis="Y", tolerance=1e-3):
    return classify_symmetry(vtk_path, axis=axis, relative_tol=tolerance) == "asymmetric"
