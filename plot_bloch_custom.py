#!/usr/bin/env python3
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

def plot_hemisperes():
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Create red hemisphere
    u_red = np.linspace(0, 2 * np.pi, 120)
    v_red = np.linspace(0, np.pi / 2, 60)
    x_red = np.outer(np.cos(u_red), np.sin(v_red))
    y_red = np.outer(np.sin(u_red), np.sin(v_red))
    z_red = np.outer(np.ones_like(u_red), np.cos(v_red))

    ax.plot_surface(x_red, y_red, z_red, rstride=4, cstride=4, color='red', alpha=0.35, linewidth=0)
    
    # Create blue hemisphere
    u_blue = np.linspace(0, 2 * np.pi, 120)
    v_blue = np.linspace(np.pi / 2, np.pi, 60)
    x_blue = np.outer(np.cos(u_blue), np.sin(v_blue))
    y_blue = np.outer(np.sin(u_blue), np.sin(v_blue))
    z_blue = np.outer(np.ones_like(u_blue), np.cos(v_blue))
    
    ax.plot_surface(x_blue, y_blue, z_blue, rstride=4, cstride=4, color='lightblue', alpha=0.35, linewidth=0)
    
    return ax

def plot_sphere():
    # Use matplotlib's default mathtext (no external LaTeX required)
    plt.rcParams.update({'font.size': 12})
    
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Create sphere
    u = np.linspace(0, 2 * np.pi, 120)
    v = np.linspace(0, np.pi, 60)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones_like(u), np.cos(v))

    ax.plot_surface(x, y, z, rstride=4, cstride=4, color='lightblue', alpha=0.35, linewidth=0)
    
    return ax

def plot_sphere_and_points(save_path='bloch_custom.png', show=True, use_hemispheres=False):
    # Use matplotlib's default mathtext (no external LaTeX required)
    plt.rcParams.update({'font.size': 12})
    
    if use_hemispheres:
        ax = plot_hemisperes()
        save_path = ''.join(save_path.split('.')[:-1]) + '_hemispheres.png'
    else:
        ax = plot_sphere()
    
    deg_45 = math.pi / 4
    pi = math.pi

    # Points to mark (as specified)
    # Use Unicode bra-ket symbols (no LaTeX required): |0⟩, -|0⟩, |1⟩, -|1⟩
    points = {
        '|0⟩': (0.0, 0.0, 1.0),
        '-|0⟩': (0.0, 0.0, -1.0),
        '|1⟩': (1.0, 0.0, 0.0),
        '-|1⟩': (-1.0, 0.0, 0.0),
        '|+⟩': (math.sin(deg_45) * math.cos(0), math.sin(deg_45) * math.sin(0), math.cos(deg_45)),
        '-|+⟩': (math.sin(pi + deg_45) * math.cos(0), math.sin(pi + deg_45) * math.sin(0), math.cos(pi + deg_45)),
        '|-⟩': (math.sin(-deg_45) * math.cos(0), math.sin(-deg_45) * math.sin(0), math.cos(-deg_45)),
        '-|-⟩': (math.sin(pi - deg_45) * math.cos(0), math.sin(pi - deg_45) * math.sin(0), math.cos(pi - deg_45)),
    }

    # Scatter the points
    xs = [p[0] for p in points.values()]
    ys = [p[1] for p in points.values()]
    zs = [p[2] for p in points.values()]
    ax.scatter(xs, ys, zs, color='red', s=60)

    # Annotate labels with a small offset so they don't overlap the marker
    for label, (x0, y0, z0) in points.items():
        # offset factor (push label slightly outward)
        off = 1.06
        ax.text(x0 * off, y0 * off, z0 * off, label, fontsize=14, ha='center', va='center')

    # Fix aspect ratio to be equal
    ax.set_box_aspect((1, 1, 1))

    # Set limits slightly larger than unit sphere for label room
    lim = 1.2
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)

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
