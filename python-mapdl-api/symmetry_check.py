import numpy as np

def is_mode_asymmetric(nodal_displacements, node_coords, axis="Y", tolerance=1e-6):
    """
    Checks whether the nodal displacement field is symmetric across the specified axis.
    Assumes displacements is Nx3 and node_coords is Nx3.
    """
    axis_idx = {"X": 0, "Y": 1, "Z": 2}[axis.upper()]
    mirror_map = {}

    for i, coord in enumerate(node_coords):
        mirrored_coord = coord.copy()
        mirrored_coord[axis_idx] *= -1

        # Find matching node
        for j, other in enumerate(node_coords):
            if np.allclose(other, mirrored_coord, atol=tolerance):
                if not np.allclose(nodal_displacements[i], nodal_displacements[j], atol=tolerance):
                    return True
    return False
