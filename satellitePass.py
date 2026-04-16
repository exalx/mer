import numpy as np
from config import Config
from skyfield.api import Topos, load, EarthSatellite, utc
from datetime import datetime, timedelta


class SatellitePass:
    def __init__(self, label, date_start, tle_file, s_file):
        self.label = label
        self.date_start = date_start

        self.tle_file = tle_file
        self.tle_lines = []
        self._load_tle()

        self.s_file = s_file
        self.data = np.array([])
        self._load_data()

        self.duration = len(self.data) // Config.BYTES_PER_SEC

        self.elevations = []
        self.azimut = []
        self.distance = []
        self.polar_coords = [[], []]
        self._load_satellite_data()
        
        self.mer = []
        self._load_mer()

    @classmethod
    def from_dict(cls, data_dict):
        label = data_dict['label']
        date_start = data_dict['start']
        tle_file = data_dict['tle']
        s_file = data_dict['s_file']
        return cls(label, date_start, tle_file, s_file)

    def _load_tle(self):
        tle_lines = []
        with open(self.tle_file, 'r', encoding='utf-16') as f:
            for line in f:
                clean_line = line.strip()
                
                if "1 59051U" in clean_line:
                    debut = clean_line.find("1 59051U")
                    tle_lines.append(clean_line[debut:])
                
                elif "2 59051" in clean_line:
                    debut = clean_line.find("2 59051")
                    tle_lines.append(clean_line[debut:])
        
        if len(tle_lines) < 2:
            raise ValueError(f"Le fichier {self.tle_file} ne contient pas un TLE complet pour le satellite 59051.")
            
        self.tle_lines = tle_lines
    
    def _load_data(self):
        self.data = np.fromfile(self.s_file, dtype=np.int8).astype(np.float32)
    
    def _load_satellite_data(self):
        ts = load.timescale()
        line1, line2, *_ = self.tle_lines
        satellite = EarthSatellite(line1, line2, 'METEOR-M2 4', ts)

        for i in range(self.duration):
            t = ts.from_datetime(self.date_start + timedelta(seconds=i))
            difference = satellite - Config.PALAISEAU
            alt, az, dist = difference.at(t).altaz()

            self.elevations.append(alt.degrees)
            self.azimut.append(az.degrees)
            self.distance.append(dist.km)

            r = 90.0 - alt.degrees # type: ignore
            theta = np.radians(az.degrees)  # type: ignore
            x = r * np.sin(theta)
            y = r * np.cos(theta)

            self.polar_coords[0].append(x)
            self.polar_coords[1].append(y)


    def _load_mer(self):
        for i in range(self.duration):
            start = i * Config.BYTES_PER_SEC
            end = (i + 1) * Config.BYTES_PER_SEC
            chunk_data = self.data[start:end]

            if (len(chunk_data) < Config.BYTES_PER_SEC) : break

            # Séparer I et Q (un point sur deux)
            I_rec = chunk_data[0::2]
            Q_rec = chunk_data[1::2]

            # Déterminer les points idéaux (pour QPSK, on prend le signe)
            I_ideal = np.sign(I_rec)
            Q_ideal = np.sign(Q_rec)

            # On évite les zéros pour ne pas fausser le calcul du signe
            I_ideal[I_ideal == 0] = 1
            Q_ideal[Q_ideal == 0] = 1

            # Calcul de la puissance du signal et de l'erreur
            P_signal = np.sum(I_ideal**2 + Q_ideal**2)
            P_erreur = np.sum((I_ideal - I_rec/np.mean(np.abs(I_rec)))**2 + 
                            (Q_ideal - Q_rec/np.mean(np.abs(Q_rec)))**2)

            self.mer.append(10 * np.log10(P_signal / P_erreur))

    def get_binned_stats(self, bin_size : int =10):
        bins = np.arange(0, 91, bin_size)
        indices = np.digitize(self.elevations, bins)

        binned_data = []
        bin_centers = []

        for i in range(1, len(bins)):
            mer_in_bin = np.array(self.mer)[indices == i]
            if len(mer_in_bin) > 0:
                binned_data.append(mer_in_bin)
                bin_centers.append(bins[i-1] + bin_size/2)

        return [bin_centers, binned_data]

