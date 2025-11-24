#!/Users/oliverb/Documents/Projects/repos/math-ia/.venv/bin/python3
"""
Useful functions that are used in other files
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

OPACITY = 0.20

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

    ax.plot_surface(x, y, z, rstride=4, cstride=4, color='lightblue', alpha=OPACITY, linewidth=0)
    
    return ax

def plot_hemisperes():
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Create red hemisphere
    u_red = np.linspace(0, 2 * np.pi, 120)
    v_red = np.linspace(0, np.pi / 2, 60)
    x_red = np.outer(np.cos(u_red), np.sin(v_red))
    y_red = np.outer(np.sin(u_red), np.sin(v_red))
    z_red = np.outer(np.ones_like(u_red), np.cos(v_red))

    ax.plot_surface(x_red, y_red, z_red, rstride=4, cstride=4, color='red', alpha=OPACITY, linewidth=0)
    
    # Create blue hemisphere
    u_blue = np.linspace(0, 2 * np.pi, 120)
    v_blue = np.linspace(np.pi / 2, np.pi, 60)
    x_blue = np.outer(np.cos(u_blue), np.sin(v_blue))
    y_blue = np.outer(np.sin(u_blue), np.sin(v_blue))
    z_blue = np.outer(np.ones_like(u_blue), np.cos(v_blue))
    
    ax.plot_surface(x_blue, y_blue, z_blue, rstride=4, cstride=4, color='lightblue', alpha=OPACITY, linewidth=0)
    
    return ax