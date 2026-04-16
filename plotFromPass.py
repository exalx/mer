import numpy as np
import matplotlib.pyplot as plt

def plot_xy(sat_passes, x):
    plt.figure(figsize=(10, 5))
    for sat_pass in sat_passes:
        x_data = getattr(sat_pass, x, "elevations")
        y_data = sat_pass.mer
        plt.plot(x_data, y_data, label=sat_pass.label, alpha=0.8)

    plt.xlabel(x)
    plt.ylabel("MER (dB)")
    plt.title("Évolution du MER en fonction de l'élévation - Meteor-M2 4")
    plt.grid(True, linestyle='--')
    plt.legend()
    plt.show()

def plot_xyz(sat_passes, x, y):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    for sat_pass in sat_passes:
        x_data = getattr(sat_pass, x, "azimut")
        y_data = getattr(sat_pass, y, "elevations")
        z_data = sat_pass.mer
        ax.plot(x_data, y_data, z_data,label=sat_pass.label, lw=2)
    
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_zlabel('MER (dB)')
    ax.set_title('Analyse 3D du signal Meteor-M2 4')

    ax.set_zlim(0, 18)
    ax.legend()
    plt.show()


def plot_polar(sat_passes):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Cercles pour 60°, 30° et 0° d'élévation
    angles = np.linspace(0, 2*np.pi, 100)
    for r in [30, 60, 90]: 
        ax.plot(r*np.cos(angles), r*np.sin(angles), 0, color='gray', linestyle='--', alpha=0.3)
        elevation_label = f"{90-r}°"
        ax.text(r, 2, 0, elevation_label, color='gray', fontsize=8, va='center')

    # Axes cardinaux
    ax.plot([-90, 90], [0, 0], [0, 0], color='gray', alpha=0.2)
    ax.plot([0, 0], [-90, 90], [0, 0], color='gray', alpha=0.2)
    ax.text(0, 95, 0, "N", color='red', fontweight='bold')

    # Affichage des différents passages
    for sat_pass in sat_passes:
        x_data = sat_pass.polar_coords[0]
        y_data = sat_pass.polar_coords[1]
        z_data = sat_pass.mer
        # On ne garde que les points au-dessus de l'horizon (Elevation > 0)
        ax.plot(x_data, y_data, z_data, label=sat_pass.label, lw=2.5)
    
    ax.set_zlabel('MER (dB)')
    ax.set_title('Sky Plot 3D : MER en fonction de la position céleste')
    ax.legend()
    ax.grid(False)

    plt.show()

def plot_mer_bins(sat_passes, bin_size=10):
    plt.figure(figsize=(10, 6))
    
    colors = ['blue', 'red', 'green']
    
    for idx, sat_pass in enumerate(sat_passes):
        centers, data = sat_pass.get_binned_stats(bin_size)
        
        # Création du boxplot
        # positions=centers permet de caler les boites sur les bons degrés
        plt.boxplot(data, positions=centers, widths=bin_size-2, 
                    patch_artist=True, 
                    boxprops=dict(facecolor=colors[idx], alpha=0.3),
                    medianprops=dict(color=colors[idx], linewidth=2),
                    manage_ticks=False,
                    label=sat_pass.label)

    plt.xlabel("Tranches d'élévation (degrés)")
    plt.ylabel("MER (dB)")
    plt.title(f"Analyse statistique du MER par bins de {bin_size}°")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xlim(0, 90)
    plt.show()
