# File: force_estimator.py
import numpy as np

def estimate_force(freq, mass, amplitude):
    """
    Estimate the force output using F = m * w^2 * u
    where:
        - freq is in Hz
        - mass is mass density (used proportionally)
        - amplitude is assumed small mode amplitude (m)
    """
    omega = 2 * np.pi * freq
    return mass * omega**2 * amplitude
