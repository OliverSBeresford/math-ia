#!/Users/oliverb/Documents/Projects/repos/math-ia/.venv/bin/python3
"""
Plot a unit sphere and mark four points with labels:

 - North pole:  `\ket{0}`  -> (0, 0, 1)
 - South pole:  `-\ket{0}` -> (0, 0, -1)
 - East pole:   `\ket{1}`  -> (1, 0, 0)
 - West pole:   `-\ket{1}` -> (-1, 0, 0)

Requires: matplotlib, numpy

Run: `python plot_bloch_custom.py`
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import math
from tools import plot_sphere, plot_hemispheres

def plot_sphere_and_points(save_path='images/bloch_custom.png', show=True, use_hemispheres=False):
    # Use matplotlib's default mathtext
    plt.rcParams.update({'font.size': 12})
    
    if use_hemispheres:
        ax = plot_hemispheres()
        save_path = ''.join(save_path.split('.')[:-1]) + '_hemispheres.png'
    else:
        ax = plot_sphere()
    
    deg_45 = math.pi / 4
    deg_90 = math.pi / 2
    pi = math.pi

    # Points to mark on the sphere
    # Use Unicode bra-ket symbols: |0⟩, -|0⟩, |1⟩, -|1⟩
    points = {
        '|0⟩': (0.0, 0.0, 1.0),
        '-|0⟩': (0.0, 0.0, -1.0),
        '|1⟩': (1.0, 0.0, 0.0),
        '-|1⟩': (-1.0, 0.0, 0.0),
        '|+⟩': (math.sin(deg_45) * math.cos(0), math.sin(deg_45) * math.sin(0), math.cos(deg_45)),
        '-|+⟩': (math.sin(pi + deg_45) * math.cos(0), math.sin(pi + deg_45) * math.sin(0), math.cos(pi + deg_45)),
        '|-⟩': (math.sin(-deg_45) * math.cos(0), math.sin(-deg_45) * math.sin(0), math.cos(-deg_45)),
        '-|-⟩': (math.sin(pi - deg_45) * math.cos(0), math.sin(pi - deg_45) * math.sin(0), math.cos(pi - deg_45)),
        # '|+i⟩': (math.sin(deg_45) * math.cos(deg_90), math.sin(deg_45) * math.sin(deg_90), math.cos(deg_45)),
        # '-|+i⟩': (math.sin(pi - deg_45) * math.cos(-deg_90), math.sin(pi - deg_45) * math.sin(-deg_90), math.cos(pi - deg_45)),
        # '|-i⟩': (math.sin(deg_45) * math.cos(-deg_90), math.sin(deg_45) * math.sin(-deg_90), math.cos(-deg_45)),
        # '-|-i⟩': (math.sin(pi - deg_45) * math.cos(deg_90), math.sin(pi - deg_45) * math.sin(deg_90), math.cos(pi - deg_45)),
    }

    # Scatter the points
    xs = [p[0] for p in points.values()]
    ys = [p[1] for p in points.values()]
    zs = [p[2] for p in points.values()]
    ax.scatter(xs, ys, zs, color='red', s=20)

    # Annotate labels with a small offset so they don't overlap the marker
    for label, (x, y, z) in points.items():
        # offset factor (push label slightly outward)
        off = 1.2
        ax.text(x * off, y * off, z * off, label, fontsize=14, ha='center', va='center')

    # Draw full x/y/z axes through the sphere (from -1 to 1)
    axis_args = dict(color='k', linewidth=1)
    ax.plot([-1, 1], [0, 0], [0, 0], **axis_args)
    ax.plot([0, 0], [-1, 1], [0, 0], **axis_args)
    ax.plot([0, 0], [0, 0], [-1, 1], **axis_args)
    
    # Fix aspect ratio to be equal
    ax.set_box_aspect((1, 1, 1))

    # Set limits slightly larger than unit sphere for label room
    lim = 1.2
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)

    # Set viewing angle
    ax.view_init(elev=20, azim=-60)
    
    # Labels and title
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title('Unit sphere with labeled points')

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    if show:
        plt.show()


if __name__ == '__main__':
    plot_sphere_and_points(use_hemispheres=True)
    plot_sphere_and_points(use_hemispheres=False)
