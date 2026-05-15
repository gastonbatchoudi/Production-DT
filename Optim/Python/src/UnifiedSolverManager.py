"""
Gestionnaire unifié pour les solveurs exacts (Gurobi, GLPK) et heuristiques (Simulated Annealing)
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import json
from datetime import datetime

from exactModel_Gurobi import LotSizingGurobiTeamsFinder
from exactModel_GLPK import LotSizingGLPKTeamsFinder


class UnifiedSolverManager:
    """
    Gestionnaire unifié pour tous les solveurs
    Harmonise les résultats de Gurobi et GLPK
    """
    
    AVAILABLE_SOLVERS = ['Gurobi', 'GLPK']
    EXACT_SOLVERS = ['Gurobi', 'GLPK']
    
    def __init__(self, demand, shift_durations, production_times, min_teams, max_teams, 
                 Cs, a, components_number, initial_stock, cutting_time):
        """
        Initialise le gestionnaire unifié
        """
        self.demand = demand
        self.shift_durations = shift_durations
        self.production_times = production_times
        self.min_teams = min_teams
        self.max_teams = max_teams
        self.Cs = Cs
        self.a = a
        self.components_number = components_number
        self.initial_stock = initial_stock
        self.cutting_time = cutting_time
        
    def solve_with_solver(self, solver_name: str, eps_stock_values: List, 
                         eps_livraisons_values: List, **solver_params) -> Tuple[List[Dict], pd.DataFrame]:
        """
        Résout avec le solveur spécifié
        """
        if solver_name not in self.AVAILABLE_SOLVERS:
            raise ValueError(f"Solveur '{solver_name}' non disponible. Choisir parmi {self.AVAILABLE_SOLVERS}")
        
        print(f"\n{'='*70}")
        print(f"RÉSOLUTION AVEC {solver_name.upper()}")
        print(f"{'='*70}")
        
        if solver_name == 'Gurobi':
            solver = LotSizingGurobiTeamsFinder(
                self.demand, self.shift_durations, self.production_times,
                self.min_teams, self.max_teams, self.Cs, self.a,
                self.components_number, self.initial_stock, self.cutting_time
            )
        elif solver_name == 'GLPK':
            solver = LotSizingGLPKTeamsFinder(
                self.demand, self.shift_durations, self.production_times,
                self.min_teams, self.max_teams, self.Cs, self.a,
                self.components_number, self.initial_stock, self.cutting_time
            )
        else:
            raise ValueError(f"Solveur inconnu: {solver_name}")
        
        solutions = solver.get_all_solutions(eps_stock_values, eps_livraisons_values, **solver_params)
        
        # Créer DataFrame harmonisé
        solutions_data = []
        for i, sol in enumerate(solutions):
            solutions_data.append({
                'Solution_ID': i,
                'Solver': solver_name,
                'Shifts': sol['objectifs']['shifts'],
                'Stock_Moyen': sol['objectifs']['stock_moyen'],
                'Livraisons_%': sol['objectifs']['livraisons']
            })
        
        df_solutions = pd.DataFrame(solutions_data)
        return solutions, df_solutions
    
    def solve_all_solvers(self, eps_stock_values: List, 
                         eps_livraisons_values: List,
                         solvers: List[str] = None,
                         **solver_params) -> Dict[str, Tuple[List, pd.DataFrame]]:
        """
        Résout avec tous les solveurs spécifiés (ou tous par défaut)
        """
        if solvers is None:
            solvers = self.AVAILABLE_SOLVERS
        
        all_results = {}
        
        for solver_name in solvers:
            if solver_name not in self.AVAILABLE_SOLVERS:
                print(f"⚠️ Solveur '{solver_name}' non disponible")
                continue
            
            try:
                solutions, df = self.solve_with_solver(solver_name, eps_stock_values, eps_livraisons_values, **solver_params)
                all_results[solver_name] = (solutions, df)
            except Exception as e:
                print(f"❌ Erreur avec {solver_name}: {str(e)}")
                all_results[solver_name] = (None, None)
        
        return all_results
    
    def save_results(self, solver_name: str, solutions: List[Dict], 
                    solutions_df: pd.DataFrame, output_dir: str = "Outputs") -> None:
        """
        Sauvegarde les résultats uniformément
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Résumé
        summary_file = output_path / f"{solver_name.lower()}_objectives.csv"
        solutions_df.to_csv(summary_file, index=False)
        print(f"✅ {summary_file}")
        
        # Matrices
        for i, sol in enumerate(solutions):
            if 'x' in sol:
                x_file = output_path / f"solution_{i}_x.csv"
                sol['x'].to_csv(x_file, index=False)
            if 's' in sol:
                s_file = output_path / f"solution_{i}_s.csv"
                sol['s'].to_csv(s_file, index=False)
    
    @staticmethod
    def compare_solvers(results_dict: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Compare les résultats de plusieurs solveurs
        """
        combined = []
        for solver_name, df in results_dict.items():
            if df is not None:
                combined.append(df)
        
        if combined:
            return pd.concat(combined, ignore_index=True)
        return pd.DataFrame()
    
    @staticmethod
    def analyze_pareto(solutions_df: pd.DataFrame) -> pd.DataFrame:
        """
        Identifie les solutions Pareto-optimales
        """
        if solutions_df.empty:
            return solutions_df
        
        df = solutions_df.copy()
        # Normaliser
        df['shifts_norm'] = (df['Shifts'] - df['Shifts'].min()) / (df['Shifts'].max() - df['Shifts'].min() + 1e-6)
        df['stock_norm'] = (df['Stock_Moyen'] - df['Stock_Moyen'].min()) / (df['Stock_Moyen'].max() - df['Stock_Moyen'].min() + 1e-6)
        df['livraisons_norm'] = (df['Livraisons_%'].max() - df['Livraisons_%']) / (df['Livraisons_%'].max() - df['Livraisons_%'].min() + 1e-6)
        
        df['pareto_score'] = df['shifts_norm'] + df['stock_norm'] + df['livraisons_norm']
        
        return df.nsmallest(5, 'pareto_score')[['Solution_ID', 'Solver', 'Shifts', 'Stock_Moyen', 'Livraisons_%']]
