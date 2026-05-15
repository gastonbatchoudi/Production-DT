"""
Configuration centrale pour le module d'optimisation
Définit les chemins et paramètres par défaut
"""

import os

# Chemins relatifs
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(BASE_DIR, '..', '..', '..')
FORECASTING_DIR = os.path.join(ROOT_DIR, 'Forecasting', 'Outputs', 'Tables')
OUTPUT_DIR = os.path.join(BASE_DIR, '..', 'Outputs')

# Fichier de prévision par défaut
DEFAULT_FORECAST_FILE = os.path.join(FORECASTING_DIR, 'forecast_aggregated_20days.csv')

# Paramètres de simulation par défaut
DEFAULT_TEMP_INIT = 500  # T0 - Température initiale
DEFAULT_TEMP_FINAL = 1   # Tf - Température finale
COOLING_RATE = 0.95      # alpha - Taux de refroidissement
MAX_ITERATIONS = 100
MAX_ITERATIONS_PER_TEMP = 30

# Solveurs disponibles
AVAILABLE_SOLVERS = ['Gurobi', 'GLPK']  # Note: CPLEX supprimé

# Configuration de stockage
STORAGE_CAPACITY = 80000  # Cs - Capacité de stockage
