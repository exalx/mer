import numpy as np
import matplotlib.pyplot as plt
from config import Config

def plot_xy(sat_passes, x):
    """Trace le MER en fonction de la coordonnée 'x' disponible parmi 'elevations', 'distance' et 'azymut'.

    Args:
        sat_passes (list[satellitePass]): Liste d'objets de la classe satellitePass dont on veut le tracé sur un même graphique.
        x (String): abscisse du graphique, parmi "elevations", "azimut", "distance".
    """
    plt.figure(figsize=(10, 5))

    # Traitement de chaque passage
    for sat_pass in sat_passes:
        x_data = getattr(sat_pass, x, "elevations")
        y_data = sat_pass.mer
        plt.plot(x_data, y_data, label=sat_pass.label, alpha=0.8)

    # Affichage et légendes
    plt.xlabel(x)
    plt.ylabel("MER (dB)")
    plt.title("Évolution du MER en fonction de l'élévation - Meteor-M2 4")
    plt.grid(True, linestyle='--')
    plt.legend()
    plt.show()

def plot_xyz(sat_passes, x, y):
    """Trace un graphique 3d avec comme paramètres :
    - du plan : x et y en paramètre, par défaut azimut et elevations.
    - axe z : le MER.

    Args:
        sat_passes (list[satellitePass]): Liste d'objets de la classe satellitePass dont on veut le tracé sur un même graphique.
        x (String): 1ere coordonnée du graphique, parmi "elevations", "azimut", "distance".
        y (String): 2e coordonnée du graphique, parmi "elevations", "azimut", "distance".
    """
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Traitement de chaque passage
    for sat_pass in sat_passes:
        x_data = getattr(sat_pass, x, "azimut")
        y_data = getattr(sat_pass, y, "elevations")
        z_data = sat_pass.mer
        ax.plot(x_data, y_data, z_data,label=sat_pass.label, lw=2)

    # Gestion des légendes    
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_zlabel('MER (dB)')
    ax.set_title('Analyse 3D du signal Meteor-M2 4')

    # Affichage
    ax.set_zlim(0, 18)
    ax.legend()
    plt.show()


def plot_polar(sat_passes):
    """Trace une représentation 3d du MER selon la trajectoire du satellite.
    La trajectoire est représentée en coordonnée cylindrique :
    - r : représente l'élévation, r=0 pour 90°.
    - theta : représente l'azimut.
    - z : représente le MER.
    
    Args:
        sat_passes (list[satellitePass]): Liste d'objets de la classe satellitePass dont on veut le tracé sur un même graphique.
    """
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Cercles de référence pour 60°, 30° et 0° d'élévation
    angles = np.linspace(0, 2*np.pi, 100)
    for r in [30, 60, 90]: 
        ax.plot(r*np.cos(angles), r*np.sin(angles), 0, color='gray', linestyle='--', alpha=0.3)
        elevation_label = f"{90-r}°"
        ax.text(r, 2, 0, elevation_label, color='gray', fontsize=8, va='center')

    # Axes cardinaux : Nord affiché
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

    # Affichage des légendes et du graphique    
    ax.set_zlabel('MER (dB)')
    ax.set_title('Sky Plot 3D : MER en fonction de la position céleste')
    ax.legend()
    ax.grid(False)

    plt.show()

def plot_mer_bins(sat_passes, bin_size=10):
    """Trace un graphique 2d qui représente le MER selon l'élévation du satellite.
    Les données sont regroupées par des paquets pour en faire la moyenne sur des intervalles d'élévations.
    La taille de ces intervalles est donnée en paramètre par 'bin_size', initialisée à 10.

    Args:
        sat_passes (list[satellitePass]): Liste d'objets de la classe satellitePass dont on veut le tracé sur un même graphique.
        bin_size (int, optional): Taille des intervalles sur lesquelles le MER est moyenné. Defaults to 10.
    """
    plt.figure(figsize=(10, 6))
    
    colors = ['blue', 'red', 'green']
    
    # Traitement de chaque passage
    for idx, sat_pass in enumerate(sat_passes):
        centers, data = sat_pass.get_binned_stats(bin_size)
        
        # Création du boxplot
        plt.boxplot(data, positions=centers, widths=bin_size-2, 
                    patch_artist=True, 
                    boxprops=dict(facecolor=colors[idx % len(colors)], alpha=0.3),
                    medianprops=dict(color=colors[idx % len(colors)], linewidth=2),
                    manage_ticks=False,
                    label=sat_pass.label)

    # Affichage du graphique et des légendes
    plt.xlabel("Tranches d'élévation (degrés)")
    plt.ylabel("MER (dB)")
    plt.title(f"Analyse statistique du MER par bins de {bin_size}°")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xlim(0, 90)
    plt.legend()
    plt.show()

def plot_raw_data(sat_passes, time_offset=-1):
    """Affiche la constellation QPSK des données récupérées.
    La constellation est ramené au carré [-1, 1]**2.
    Permet de visualiser la répartition des points obtenus sur un intervalle de temps donné.

    Args:
        sat_passes (list[satellitePass]): Liste d'objets de la classe satellitePass dont on veut le tracé sur un même graphique.
        time_offset (int, optional): Début de l'intervalle de temps des données à afficher. Defaults to -1, se place à la moitié de l'enregistrement.
    """
    plt.figure(figsize=(9, 9))

    # Traitement de chaque passage
    for sat_pass in sat_passes:
        # Récupération de l'instant à afficher
        current_time = time_offset if time_offset >= 0 else sat_pass.duration // 2
        start = current_time * Config.BYTES_PER_SEC
        end = (current_time + 1) * Config.BYTES_PER_SEC

        # Récupération des points
        I = sat_pass.data[start:end:2] / 128
        Q = sat_pass.data[start+1:end:2] / 128
        
        # Tracé des points reçus
        plt.scatter(I, Q, s=1, alpha=0.03, label=f"Symboles {sat_pass.label}")
    
    # Ajout des frontières de décision
    plt.axhline(0, color='black', linewidth=1.5)
    plt.axvline(0, color='black', linewidth=1.5)
    
    # Mise en forme
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.axis('equal')
    plt.title("Analyse de la Constellation")
    plt.xlabel("Canal In-phase (I)")
    plt.ylabel("Canal Quadrature (Q)")
    leg = plt.legend(loc='upper right', markerscale=2)
    for lh in leg.legend_handles: 
        if lh is not None: lh.set_alpha(1)
    
    # Limites pour bien voir les quadrants
    plt.xlim(-1.2, 1.2)
    plt.ylim(-1.2, 1.2)
    
    plt.show()
