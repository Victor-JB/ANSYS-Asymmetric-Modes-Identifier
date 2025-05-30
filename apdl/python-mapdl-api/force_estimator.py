# File: force_estimator.py
import pyvista as pv
import numpy as np

def estimate_force_from_vtk(vtk_path, axis="X", amplitude=0.001):
    mesh = pv.read(vtk_path)

    # Find displacement field
    for name in mesh.point_data:
        if mesh.point_data[name].ndim == 2 and mesh.point_data[name].shape[1] == 3:
            vectors = mesh.point_data[name]
            mesh.point_data.active_vectors_name = name
            break
    else:
        raise ValueError("No vector field found.")

    coords = mesh.points
    axis_idx = {"X": 0, "Y": 1, "Z": 2}[axis.upper()]

    # Select nodes at vibrating end (largest X by default)
    max_axis_val = np.max(coords[:, axis_idx])
    mask = np.abs(coords[:, axis_idx] - max_axis_val) < 1e-5
    surface_displacements = vectors[mask]

    # Effective force ~ sum of vector magnitudes at driving face
    # This isn't reaction force, but proportional to how much energy is transmitted at the interface
    avg_disp_vec = np.mean(surface_displacements, axis=0)
    force_magnitude = np.linalg.norm(avg_disp_vec) * amplitude * 1e6  # scaled to mN or N

    return force_magnitude
