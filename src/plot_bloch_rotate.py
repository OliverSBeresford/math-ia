#!/Users/oliverb/Documents/Projects/repos/math-ia/.venv/bin/python3
"""
Plot a Bloch-sphere state, rotate it 180 degrees around the x axis,
and draw the path taken on the sphere surface.

Usage examples:
  python src/plot_bloch_rotate.py --theta 45 --phi 30        # degrees
  python src/plot_bloch_rotate.py --theta 0.9 --phi 1.2 --radians  # radians

Outputs an image `images/bloch_rotate_<theta>_<phi>.png` by default and shows the figure.

Requires: matplotlib, numpy
"""
import argparse
import math
import os

import numpy as np
import matplotlib.pyplot as plt

from tools import plot_sphere
from quantum_state import QuantumState

def plot_bloch_rotation(theta, phi, save_path=None, show=True, n_steps=100):
    plt.rcParams.update({'font.size': 12})

    ax = plot_sphere()

    # Standard labelled basis points
    base_points = {
        '|0⟩': np.array([0.0, 0.0, 1.0]),
        '-|0⟩': np.array([0.0, 0.0, -1.0]),
        '|+⟩': np.array([1.0, 0.0, 0.0]),
        '|-⟩': np.array([-1.0, 0.0, 0.0]),
    }

    # Plot base points
    for label, p in base_points.items():
        ax.scatter([p[0]], [p[1]], [p[2]], color='red', s=30)
        ax.text(*(p * 1.08), label, fontsize=12, ha='center', va='center')

    # Initial state (keep this object unchanged)
    psi0 = QuantumState(theta=theta, phi=phi)
    psi0_coords = psi0.bloch_coordinates()
    ax.scatter([psi0_coords[0]], [psi0_coords[1]], [psi0_coords[2]], color='blue', s=60, label='initial')
    ax.text(*(psi0_coords * 1.12), 'ψ₀', color='blue', fontsize=12, ha='center', va='center')

    # Rotation: 180 degrees (pi radians) about x-axis
    total_angle = math.pi

    # Path: sample rotation angles from 0 to pi and apply to psi0
    thetas = np.linspace(0.0, total_angle, n_steps)
    # Build path by rotating a fresh copy of the original state for each sample.
    # This avoids cumulative in-place rotations that produce incorrect paths.
    path = np.array([QuantumState(theta=theta, phi=phi).rotate_x(t) for t in thetas])

    # Plot the path on the sphere surface
    ax.plot(path[:, 0], path[:, 1], path[:, 2], color='orange', linewidth=2, label='rotation path')

    # Final state
    psi1_coords = QuantumState(theta=theta, phi=phi).rotate_x(total_angle)
    ax.scatter([psi1_coords[0]], [psi1_coords[1]], [psi1_coords[2]], color='green', s=60, label='rotated')
    ax.text(*(psi1_coords * 1.12), 'ψ₁', color='green', fontsize=12, ha='center', va='center')

    # Draw axes through sphere
    axis_args = dict(color='k', linewidth=1)
    ax.plot([-1, 1], [0, 0], [0, 0], **axis_args)
    ax.plot([0, 0], [-1, 1], [0, 0], **axis_args)
    ax.plot([0, 0], [0, 0], [-1, 1], **axis_args)

    # Small arrowheads for positive axes
    try:
        ax.quiver(0.9, 0, 0, 0.1, 0, 0, color='k', length=0.1, normalize=True, arrow_length_ratio=0.3)
        ax.quiver(0, 0.9, 0, 0, 0.1, 0, color='k', length=0.1, normalize=True, arrow_length_ratio=0.3)
        ax.quiver(0, 0, 0.9, 0, 0, 0.1, color='k', length=0.1, normalize=True, arrow_length_ratio=0.3)
    except Exception:
        pass

    # Adjust aspect and limits
    ax.set_box_aspect((1, 1, 1))
    lim = 1.2
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)

    # View angle and labels
    ax.view_init(elev=args.elevate, azim=args.azimuth)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title(f'Rotation of state (θ={theta:.3g}, φ={phi:.3g}) about x by 180°')

    ax.legend(loc='upper left')

    if save_path is None:
        # create images dir if missing
        os.makedirs('images', exist_ok=True)
        save_path = os.path.join('images', f'bloch_rotate_theta{theta:.3g}_phi{phi:.3g}_e{args.elevate:.3g}_a{args.azimuth:.3g}.png')

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    if show:
        plt.show()

    return save_path


def _parse_args():
    p = argparse.ArgumentParser(description='Plot Bloch rotation about x-axis and path on sphere')
    p.add_argument('--theta', type=float, default=45.0, help='Polar angle θ (degrees by default)')
    p.add_argument('--phi', type=float, default=30.0, help='Azimuthal angle φ (degrees by default)')
    p.add_argument('--radians', action='store_true', help='Interpret theta/phi as radians')
    p.add_argument('--elevate', type=float, default=20.0, help='Elevation angle for 3D view')
    p.add_argument('--azimuth', type=float, default=-60.0, help='Azimuth angle for 3D view')
    p.add_argument('--no-show', dest='show', action='store_false', help='Do not show interactive window')
    p.add_argument('--steps', type=int, default=120, help='Number of samples along rotation path')
    return p.parse_args()


if __name__ == '__main__':
    args = _parse_args()
    if args.radians:
        theta = args.theta
        phi = args.phi
    else:
        theta = math.radians(args.theta)
        phi = math.radians(args.phi)

    out = plot_bloch_rotation(theta, phi, show=args.show, n_steps=args.steps)
    print('Saved:', out)
