# Analyse de la Qualité de Réception des Données du Satellite Météor-M2 4

Ce projet a pour but d'analyser la qualité de la réception des signaux du satellite météorologique Météor-M2 4 (NORAD ID 59051). Il traite les enregistrements bruts (fichiers `.s`) des passages du satellite au-dessus de la station de réception de Palaiseau pour calculer et visualiser le **Modulation Error Ratio (MER)**.

Le MER est un indicateur clé de la qualité du signal, et ce projet permet de l'étudier en fonction de divers paramètres orbitaux comme l'élévation, l'azimut et la distance du satellite.

## 🚀 Fonctionnalités

- **Calcul Automatisé** : Calcule la position du satellite (élévation, azimut, distance) et le MER pour chaque seconde d'un passage.
- **Visualisations Multiples** : Génère une variété de graphiques pour analyser la qualité du signal sous différents angles :
  - Graphiques 2D et 3D du MER en fonction des coordonnées.
  - "Sky Plot" 3D pour visualiser le MER le long de la trajectoire du satellite.
  - Analyse statistique du MER par tranches d'élévation.
  - Affichage de la constellation QPSK pour inspecter la qualité de la modulation.
- **Comparaison de Passages** : Permet de superposer les données de plusieurs passages de satellites sur les mêmes graphiques pour comparer leurs performances.

## 📂 Structure du Projet

- `main.py`: Le script principal pour lancer les analyses. C'est ici que l'on configure les passages à traiter et les graphiques à générer.
- `satellitePass.py`: Contient la classe `SatellitePass` qui encapsule toutes les données et les calculs pour un unique passage de satellite (chargement des TLE, des données I/Q, calcul de la position et du MER).
- `plotFromPass.py`: Regroupe toutes les fonctions de visualisation `matplotlib` pour générer les différents graphiques d'analyse.
- `config.py`: Fichier de configuration contenant les constantes du projet (coordonnées de la station, paramètres du signal, etc.).
- `requirements.txt`: Liste des dépendances Python nécessaires.
- `data/`: Dossier contenant les données brutes pour chaque passage de satellite, organisé par date.

## ⚙️ Installation

1.  Clonez ce dépôt sur votre machine locale.
2.  Il est recommandé de créer un environnement virtuel Python :
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Sur Windows: .venv\Scripts\activate
    ```
3.  Installez les dépendances nécessaires avec pip :
    ```bash
    pip install -r requirements.txt
    ```

## ▶️ Utilisation

1.  **Configurer les passages** :
    Ouvrez le fichier `main.py`. La liste `passes_config` contient les configurations pour chaque passage de satellite que vous souhaitez analyser. Vous pouvez ajouter ou modifier des passages en spécifiant le chemin vers le fichier TLE (`tle`) et le fichier de données brutes (`s_file`), ainsi que la date de début de l'enregistrement.

2.  **Sélectionner les graphiques** :
    Toujours dans `main.py`, vous pouvez choisir les passages à afficher en modifiant la liste `render`. Ensuite, décommentez les appels aux fonctions de tracé que vous souhaitez générer (`plot_xy`, `plot_xyz`, `plot_polar`, etc.).

3.  **Lancer l'analyse** :
    Exécutez le script `main.py` depuis votre terminal :
    ```bash
    python main.py
    ```

Les graphiques générés par `matplotlib` s'afficheront à l'écran.
