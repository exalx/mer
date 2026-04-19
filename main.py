from satellitePass import SatellitePass
from plotFromPass import *
from skyfield.api import utc
from datetime import datetime, timedelta

# --- INITIALISATION PASS ---
passes_config = [
    {
        "tle": "data/2026_03_18/tle.txt",
        "s_file": "data/2026_03_18/meteor_15-07-43_18-03-2026.s",
        "start": datetime(2026, 3, 18, 15, 7, 43, tzinfo=utc) - timedelta(hours=1),
        "label": "18/03 (15h07)"
    },
    {
        "tle": "data/2026_04_01/tle.txt",
        "s_file": "data/2026_04_01/meteor_16-04-25_01-04-2026.s",
        "start": datetime(2026, 4, 1, 16, 4, 25, tzinfo=utc) - timedelta(hours=2),
        "label": "01/04 (16h04)"
    },
    {
        "tle": "data/2026_04_17/tle.txt",
        "s_file": "data/2026_04_17/meteor_15-17-05_17-04-2026.s",
        "start": datetime(2026, 4, 17, 15, 17, 5, tzinfo=utc) - timedelta(hours=2),
        "label": "17/04 (15h17)"
    },
]

# --- CHOIX DES PASSAGES A AFFICHER ---

sat_passes = []
render = [2]
for i in render:
    sat_passes.append(SatellitePass.from_dict(passes_config[i]))


# --- LISTE PARAMETRES ---
param = ["elevations, azimut, distance"]

# --- PLOTS ---
# --- 2D ---
# plot_xy(sat_passes, "elevations")

# --- 3D ---
# plot_xyz(sat_passes, "azimut", "elevations")

# --- Polar ---
# plot_polar(sat_passes)

# --- Binned Stats ---
plot_mer_bins(sat_passes, 5)