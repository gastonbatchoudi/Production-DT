import pandas as pd
import numpy as np

class Data:
    def __init__(self, csv_file_path="../../../Forecasting/Outputs/Tables/forecast_aggregated_20days.csv"):

        self.csv_file_path = csv_file_path
        self.df = None
        self.data = None
        self.T = 0
        self.I = 0
        self.shift_durations = []
        self.max_teams = []
        self.min_teams = []
        self.Cs = 80000
        self.production_times = None
        self.demand = None
        self.a = 0
        self.cutting_time = 0.5
        self.components_number = [4,4,4,4,4,8,8,8,8,8,7,7,7,7,7,8,8,8,8,8,4,4,4,4,4,6,6,6,6,6]
        self.initial_stock = None
        self.eps_stock_values = [30, 40, 50, 500, 1000, 1500, 2000, 3000, 80000]
        self.eps_livraisons_values = [0.95, 0.96, 0.97, 0.98, 0.99, 1.0]
        self.eps_teams_values = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

    def load_data(self):
        """Charge les données depuis le fichier CSV."""
        try:
            self.df = pd.read_csv(self.csv_file_path)
            print(f"✓ Données chargées avec succès depuis {self.csv_file_path}")
            print(f"  Dimensions du fichier CSV: {self.df.shape}")

            if 'Periode_Agregee' in self.df.columns:
                self.df = self.df.drop(columns=['Periode_Agregee'])
            elif 'Periode' in self.df.columns:
                self.df = self.df.drop(columns=['Periode'])

            # Remplacer les NaN par 0
            self.df.fillna(0, inplace=True)

            # Convertir en numpy array
            self.data = self.df.to_numpy()

            # Obtenir les dimensions
            self.T, self.I = self.data.shape
            self.T = self.T

            print(f"  Nombre de périodes: {self.T}")
            print(f"  Nombre de produits: {self.I}")

            return True

        except FileNotFoundError:
            print(f"✗ Erreur: Le fichier {self.csv_file_path} n'existe pas.")
            return False
        except Exception as e:
            print(f"✗ Erreur lors du chargement des données: {e}")
            return False

    def initialize_parameters(self):
        """Initialise les paramètres du problème en fonction des dimensions des données."""

        if self.data is None:
            return False

        base_pattern = [8400, 8400, 4200, 4200, 4200, 4200, 4200, 4200, 4200, 8400, 8400, 8400]
        self.shift_durations = (base_pattern * ((self.T // 12) + 1))[:self.T]

        base_max_teams = [1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1]
        self.max_teams = (base_max_teams * ((self.T // 12) + 1))[:self.T]

        base_min_teams = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.min_teams = (base_min_teams * ((self.T // 12) + 1))[:self.T]

        self.production_times = np.array([2 if i < 5 else 4 for i in range(self.I)])

        self.demand = self.data.T

        self.initial_stock = np.zeros(self.I)

        return True

    def process(self):
        print("\n" + "="*60)
        print("CHARGEMENT DES DONNÉES DE PRÉVISION")
        print("="*60 + "\n")

        if not self.load_data():
            return False

        if not self.initialize_parameters():
            return False

        return True

    def get_data_dict(self):
        """Retourne un dictionnaire avec toutes les données pour utilisation externe."""
        return {
            'data': self.data,
            'demand': self.demand,
            'T': self.T,
            'I': self.I,
            'shift_durations': self.shift_durations,
            'max_teams': self.max_teams,
            'min_teams': self.min_teams,
            'Cs': self.Cs,
            'production_times': self.production_times,
            'a': self.a,
            'cutting_time': self.cutting_time,
            'components_number': self.components_number,
            'initial_stock': self.initial_stock,
            'eps_stock_values': self.eps_stock_values,
            'eps_livraisons_values': self.eps_livraisons_values,
            'eps_teams_values': self.eps_teams_values,
        }
