import numpy as np

# Charger le fichier .s (en supposant du int8 / S8)
data = np.fromfile("2026_04_01/result_gnuradio.s", dtype=np.int8).astype(np.float32)

# Séparer I et Q (un point sur deux)
I_rec = data[0::2]
Q_rec = data[1::2]

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

mer = 10 * np.log10(P_signal / P_erreur)
print(f"MER calculé : {mer:.2f} dB")