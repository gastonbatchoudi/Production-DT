
import os
import pandas as pd

class AggregatedData:
    def __init__(self, input_file_path="../Outputs/Tables/forecast_only.csv", output_folder="../Outputs/Tables/"):
        """
        Args:
            input_file_path (str): Chemin vers le fichier forecast_only.csv
            output_folder (str): Dossier de sortie pour les fichiers agrégés
        """
        self.input_file_path = input_file_path
        self.output_folder = output_folder
        self.data = None
        self.aggregated_data = None

    def load_forecast_data(self):
        """Charge les données de prévision depuis le fichier CSV."""
        try:
            self.data = pd.read_csv(self.input_file_path)
            print(f"Données chargées avec succès depuis {self.input_file_path}")
            print(f"Dimensions des données: {self.data.shape}")
            print(f"Colonnes disponibles: {list(self.data.columns)[:5]}...")
        except FileNotFoundError:
            print(f"Erreur: Le fichier {self.input_file_path} n'existe pas.")
            return False
        except Exception as e:
            print(f"Erreur lors du chargement des données: {e}")
            return False
        return True

    def aggregate_by_period(self, period_size):
        """
        Agrège les données par période spécifiée.
        
        Args:
            period_size (int): Taille de la période d'agrégation (ex: 5 pour une semaine)
        """
        if self.data is None:
            print("Erreur: Aucune donnée chargée. Utilisez load_forecast_data() d'abord.")
            return

        if period_size <= 0:
            print("Erreur: La taille de période doit être positive.")
            return

        df = self.data.copy()

        df['Period_Group'] = ((df['Periode'] - 1) // period_size) + 1

        forecast_columns = [col for col in df.columns if col not in ['Periode', 'Period_Group']]

        if not forecast_columns:
            print("Erreur: Aucune colonne de prévision trouvée.")
            return

        print(f"Colonnes à agréger: {forecast_columns[:5]}...")

        aggregated_df = df.groupby('Period_Group')[forecast_columns].sum().reset_index()

        aggregated_df = aggregated_df.rename(columns={'Period_Group': 'Periode_Agregee'})

        self.aggregated_data = aggregated_df

        print(f"Agrégation terminée par période de {period_size} jours.")
        print(f"Nombre de périodes agrégées: {len(self.aggregated_data)}")

    def save_aggregated_data(self, period_size):
        """
        Sauvegarde les données agrégées dans un fichier CSV.
        
        Args:
            period_size (int): Taille de la période utilisée pour l'agrégation
        """
        if self.aggregated_data is None:
            print("Erreur: Aucune donnée agrégée disponible.")
            return

        os.makedirs(self.output_folder, exist_ok=True)

        output_filename = f"forecast_aggregated_{period_size}days.csv"
        output_path = os.path.join(self.output_folder, output_filename)

        self.aggregated_data.to_csv(output_path, index=False)

        print(f"Données agrégées sauvegardées dans: {output_path}")

    def get_aggregated_summary(self):
        """Affiche un résumé des données agrégées."""
        if self.aggregated_data is None:
            print("Erreur: Aucune donnée agrégée disponible.")
            return

        print("\n=== Résumé des données agrégées ===")
        print(f"Nombre de périodes agrégées: {len(self.aggregated_data)}")
        print(f"Nombre de produits: {len(self.aggregated_data.columns) - 1}")
        print(f"Colonnes disponibles: {list(self.aggregated_data.columns[:6])}...")
        print("\nPremières lignes:")
        print(self.aggregated_data.head())

        forecast_columns = [col for col in self.aggregated_data.columns if col != 'Periode_Agregee']
        if forecast_columns:
            print(f"\nStatistiques descriptives des {len(forecast_columns)} produits:")
            print(self.aggregated_data[forecast_columns].describe())

    def process_aggregation(self, period_size):
        """
        Méthode complète pour traiter l'agrégation des données.
        
        Args:
            period_size (int): Taille de la période d'agrégation
        """
        print(f"\n{'='*60}")
        print(f"Démarrage de l'agrégation par période de {period_size} jours...")
        print(f"{'='*60}\n")

        if not self.load_forecast_data():
            return

        self.aggregate_by_period(period_size)
        self.save_aggregated_data(period_size)

        self.get_aggregated_summary()

        print(f"\n{'='*60}")
        print(f"Agrégation terminée avec succès pour des périodes de {period_size} jours!")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    aggregator = AggregatedData()
    aggregator.process_aggregation(5)
    aggregator.process_aggregation(10)
    aggregator.process_aggregation(20)
