from dataclasses import dataclass
from skyfield.api import Topos, load, EarthSatellite, utc
from datetime import datetime, timedelta

@dataclass
class Config:
    # Informations du satellite
    NORAD_ID = 59051

    # Coordonnées du site de réception (Palaiseau)
    LAT = '48.7128 N'
    LON = '2.2101 E'
    PALAISEAU = Topos(LAT, LON)

    # Paramètres du signal Meteor-M2
    BAUDRATE = 72000
    SAMPLES_PER_SYMBOL = 4 

    # Calcul automatique du débit binaire (2 bits par symbole en QPSK)
    BYTES_PER_SEC = BAUDRATE * 2