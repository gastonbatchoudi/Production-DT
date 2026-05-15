from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting
import matplotlib.pyplot as plt
import pandas as pd

class ParetoFront:
    def __init__(self, solutions_df):
        self.solutions_df = solutions_df

    def non_dominated_solutions(self):
        df = self.solutions_df
        points = df[["shifts", "stock_moyen", "livraisons"]].to_numpy()
        points[:, 2] = -points[:, 2]  # inversion car on maximise "livraisons"

        nds = NonDominatedSorting().do(points, only_non_dominated_front=True)
        nds_indices = nds  # indices des solutions non dominées

        self.non_dominated_indices = nds_indices  # stocker les indices d'origine

        return df.iloc[nds].drop_duplicates()

    def non_dominated_solutions1(self):
        df = self.solutions_df
        is_dominated = []
        for idx, row in df.iterrows():
            dominated = any(
                (other_row['shifts'] <= row['shifts']) and
                (other_row['stock_moyen'] <= row['stock_moyen']) and
                (other_row['livraisons'] >= row['livraisons']) and
                ((other_row['shifts'] < row['shifts']) or
                 (other_row['stock_moyen'] < row['stock_moyen']) or
                 (other_row['livraisons'] > row['livraisons']))
                for _, other_row in df.iterrows()
            )
            is_dominated.append(not dominated)
        return df[is_dominated].drop_duplicates()


class ParetoFrontVisualizer:

    def __init__(self, data):
        self.df_non_dom = data

    def plot_pareto_front_3d(self):
        fig = plt.figure(figsize=(12, 12))
        ax = fig.add_subplot(111, projection='3d')

        scat = ax.scatter(self.df_non_dom['shifts'], self.df_non_dom['stock_moyen'], self.df_non_dom['livraisons'],
                          c=self.df_non_dom['shifts'], cmap='viridis', edgecolors='k')

        labels = [f'S{i+1}' for i in range(len(self.df_non_dom))]
        for i in range(len(self.df_non_dom)):
            ax.text(self.df_non_dom['shifts'].iloc[i],
                    self.df_non_dom['stock_moyen'].iloc[i],
                    self.df_non_dom['livraisons'].iloc[i],
                    labels[i], fontsize=10, color='red')

        ax.set_xlabel('Total number of teams',fontsize=14)
        ax.set_ylabel('Average stock',fontsize=14)
        ax.set_zlabel('Customers satisfaction rate',fontsize=14)
        ax.tick_params(axis='both', which='major', labelsize=12)
        plt.savefig('front_pareto_3d.pdf',dpi=300)
        plt.savefig('front_pareto_3d.jpeg',dpi=300)
        plt.show()

    def plot_satisfaction_vs_shifts(self):
        fig, ax = plt.subplots(figsize=(12, 8))
        scatter = ax.scatter(self.df_non_dom['livraisons'], self.df_non_dom['shifts'],
                             c=self.df_non_dom['stock_moyen'], cmap='coolwarm', edgecolors='k', s=100)

        ax.set_xlabel('Satisfaction rate',fontsize=14)
        ax.set_ylabel('Number of teams',fontsize=14)
        ax.set_title('Customers satisfaction vs Total number of teams',fontsize=14)
        ax.tick_params(axis='both', which='major', labelsize=12)
        ax.grid(True, linestyle='--', alpha=0.7)
        fig.colorbar(scatter, ax=ax, label='Average stock')
        plt.savefig('graphique1.pdf',dpi=300)
        plt.show()

    def plot_shifts_vs_stock_moyen(self):
        fig, ax = plt.subplots(figsize=(12, 8))
        scatter = ax.scatter(self.df_non_dom['shifts'], self.df_non_dom['stock_moyen'],
                             c=self.df_non_dom['livraisons'], cmap='viridis', edgecolors='k', s=100)

        ax.set_xlabel('Number of teams',fontsize=14)
        ax.set_ylabel('Average stock',fontsize=14)
        ax.set_title('Total number of teams vs Average stock',fontsize=14)
        ax.tick_params(axis='both', which='major', labelsize=12)
        ax.grid(True, linestyle='--', alpha=0.7)
        fig.colorbar(scatter, ax=ax, label='Customers satisfaction rate')
        plt.savefig('graphique2.pdf',dpi=300)
        plt.show()

    def plot_livraisons_vs_stock_moyen(self):
        fig, ax = plt.subplots(figsize=(12, 8))
        scatter = ax.scatter(self.df_non_dom['livraisons'], self.df_non_dom['stock_moyen'],
                             c=self.df_non_dom['shifts'], cmap='plasma', edgecolors='k', s=100)

        ax.set_xlabel('Satisfaction rate',fontsize=14)
        ax.set_ylabel('Average stock',fontsize=14)
        ax.set_title('Customers satisfaction vs Average stock',fontsize=14)
        ax.tick_params(axis='both', which='major', labelsize=12)
        ax.grid(True, linestyle='--', alpha=0.7)
        fig.colorbar(scatter, ax=ax, label='Total number of teams')
        plt.savefig('graphique3.pdf',dpi=300)
        plt.show()
