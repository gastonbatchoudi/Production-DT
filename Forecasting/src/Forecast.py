import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
import re

class ForecastModel:
    def __init__(self, file_path, sheet_name, date_column, output_file, pdf_file=None):
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.date_column = date_column
        self.output_file = output_file
        self.pdf_file = pdf_file
        self.data = None
        self.forecasts = {}
        self.errors = {}
        self.date_format = None  # Stocke le format détecté (D, M, Y)
        self.frequency = 'D'  # Fréquence par défaut (Jour)

    def load_data(self):
        """Charge les données à partir d'une feuille spécifique d'un fichier Excel"""
        data = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
        data[self.date_column] = pd.to_datetime(data[self.date_column], errors='coerce')
        data = data.dropna(subset=[self.date_column])
        data = data.sort_values(by=self.date_column)
        self.data = data.set_index(self.date_column)
        
        # Déterminer automatiquement le format des dates
        self._detect_date_format()

        self.data = self.data.cumsum()

    def _detect_date_format(self):
        """Détecte automatiquement le format des dates et définit la fréquence de prévision."""
        if self.data is None or len(self.data) == 0:
            self.frequency = 'D'
            self.date_format = 'day'
            return
        
        try:
            if hasattr(self.data, 'index') and hasattr(self.data.index, 'min'):
                dates = self.data.index[:min(5, len(self.data))]
            else:
                dates = pd.to_datetime(self.data.iloc[:min(5, len(self.data)), 0])
        except Exception as e:
            print(f"Erreur lors de l'extraction des dates: {e}")
            self.frequency = 'D'
            self.date_format = 'day'
            return
        
        if len(dates) > 1:
            date_diffs = pd.Series(dates).diff().dropna()
            
            if len(date_diffs) > 0:
                if all(diff >= pd.Timedelta(days=20) for diff in date_diffs):
                    avg_diff = date_diffs.mean()
                    
                    if avg_diff >= pd.Timedelta(days=300):
                        self.frequency = 'Y'
                        self.date_format = 'year'
                    else:
                        self.frequency = 'M'
                        self.date_format = 'month'
                else:
                    self.frequency = 'D'
                    self.date_format = 'day'
            else:
                self.frequency = 'D'
                self.date_format = 'day'
        else:
            self.frequency = 'D'
            self.date_format = 'day'
        
        print(f"Format de dates détecté: {self.date_format.upper()} | Fréquence de prévision: {self.frequency}")

    def train_and_forecast(self, periods=30.5):
        """Entraîne un modèle Prophet pour chaque produit et génère des prévisions."""
        for product in self.data.columns:
            print(f"Entrainement pour {product}...")
            product_data = self.data[[product]].reset_index().rename(columns={self.date_column: 'ds', product: 'y'})
            model = Prophet()
            model.fit(product_data)
            
            future = model.make_future_dataframe(periods=int(periods), freq=self.frequency)
            forecast = model.predict(future)
            forecast[['yhat', 'yhat_lower', 'yhat_upper']] = np.maximum(0, np.ceil(forecast[['yhat', 'yhat_lower', 'yhat_upper']]))
            self.forecasts[product] = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

            actual_values = product_data['y'].values
            predicted_values = forecast['yhat'][:len(actual_values)].values

            mae = mean_absolute_error(actual_values, predicted_values)
            mse = mean_squared_error(actual_values, predicted_values)
            rmse = np.sqrt(mse)

            self.errors[product] = {'MAE': mae, 'MSE': mse, 'RMSE': rmse}

    def decumulate_forecasts(self):
        """Décumule les prévisions et met les valeurs négatives à zéro."""
        decumulated_forecasts = {}
        
        for product, forecast_df in self.forecasts.items():
            df = forecast_df.copy()
            cols_to_decumulate = [col for col in df.columns if col != 'ds']

            for col in cols_to_decumulate:
                df.loc[1:, col] = df[col].diff().iloc[1:]

            df[cols_to_decumulate] = df[cols_to_decumulate].clip(lower=0)
            df = df.iloc[:-1].reset_index(drop=True)
            
            decumulated_forecasts[product] = df

        self.forecasts = decumulated_forecasts
        self.decumulate_historical_data()
        
        print("Prévisions et données historiques décumulées avec succès.")

    def decumulate_historical_data(self):
        """Décumule les données historiques pour cohérence avec les prévisions."""
        decumulated_data = self.data.copy()

        for product in decumulated_data.columns:
            decumulated_data[product] = decumulated_data[product].diff()

        decumulated_data = decumulated_data.iloc[1:]
        decumulated_data = decumulated_data.clip(lower=0)

        self.data = decumulated_data

    def save_results(self):
        """Sauvegarde les résultats de prévision dans trois fichiers CSV."""
        forecast_only = pd.DataFrame()
        length = len(next(iter(self.forecasts.values())))
        forecast_only['Periode'] = range(1, length + 1)

        for product, forecast in self.forecasts.items():
            forecast_only[f'yhat_{product}'] = forecast['yhat'].values
            forecast_only[f'yhat_lower_{product}'] = forecast['yhat_lower'].values
            forecast_only[f'yhat_upper_{product}'] = forecast['yhat_upper'].values

        yhat_only = pd.DataFrame()
        yhat_only['Periode'] = range(1, length + 1)

        for product, forecast in self.forecasts.items():
            yhat_only[f'{product}'] = forecast['yhat'].values

        base = os.path.splitext(self.output_file)[0]
        forecast_path = base + "_all.csv"
        yhat_path = base + "_only.csv"
        errors_path = base + "_errors.csv"

        forecast_only.to_csv(forecast_path, index=False)
        yhat_only.to_csv(yhat_path, index=False)
        pd.DataFrame.from_dict(self.errors, orient='index').to_csv(errors_path, index=True)

        print(f"Prévisions complètes sauvegardées dans {forecast_path}")
        print(f"Prévisions yhat uniquement sauvegardées dans {yhat_path}")
        print(f"Erreurs de prévisions sauvegardées dans {errors_path}")

    def _sanitize_filename(self, name):
        """Sanitize product name for filenames."""
        name = re.sub(r'[^\w\-_. ]', '_', str(name))
        name = name.strip().replace(' ', '_')
        return name

    def plot_forecasts_and_save_pdf(self):
        """Affiche et enregistre toutes les prévisions dans un fichier PDF et en images PNG."""
        if self.pdf_file is None:
            print("PDF file path not specified, skipping PDF generation.")
            return
        
        pdf_abs = os.path.abspath(self.pdf_file)
        pdf_dir = os.path.dirname(pdf_abs)
        os.makedirs(pdf_dir, exist_ok=True)
        pdf_base = os.path.splitext(os.path.basename(self.pdf_file))[0]

        with PdfPages(self.pdf_file) as pdf:
            for product in self.forecasts:
                plt.figure(figsize=(12, 6))
                
                plt.plot(self.forecasts[product]['ds'], self.forecasts[product]['yhat'], 
                        label='forecast (yhat)', color='blue', linewidth=2)
                
                plt.fill_between(self.forecasts[product]['ds'], 
                               self.forecasts[product]['yhat_lower'], 
                               self.forecasts[product]['yhat_upper'], 
                               color='lightblue', alpha=0.3, label='confidence interval')
                
                plt.xlabel('Date')
                plt.ylabel('Demand Value')
                plt.title(f"Demand Forecast for {product}")
                plt.legend()
                plt.grid(True, alpha=0.3)

                pdf.savefig()

                safe_name = self._sanitize_filename(product)
                png_name = f"{pdf_base}_{safe_name}.png"
                png_path = os.path.join(pdf_dir, png_name)
                plt.savefig(png_path, dpi=300, bbox_inches='tight')

                plt.close()
                print(f"Figure pour {product} sauvegardée: {png_path}")
        print(f"Les graphiques de prevision ont ete enregistres dans {self.pdf_file}.")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    
    file_path = os.path.join(project_root, "Forecasting", "Data", "Data.xlsx")
    sheet_name = "All_Data"
    date_column = "Row Labels"
    output_file = os.path.join(project_root, "Forecasting", "Outputs", "Tables", "forecast.csv")
    pdf_file = os.path.join(project_root, "Forecasting", "Outputs", "graphs", "Figure.pdf")

    forecast_model = ForecastModel(file_path, sheet_name, date_column, output_file, pdf_file)
    forecast_model.load_data()
    forecast_model.train_and_forecast(periods=1)
    forecast_model.decumulate_forecasts()

    forecast_model.save_results()
    forecast_model.plot_forecasts_and_save_pdf()

    print(f"Les resultats de prevision ont ete enregistres dans {output_file}.")
