import sys
import os
import numpy as np
import pandas as pd

from Data import Data
from exactModel_Gurobi import LotSizingGurobiTeamsFinder
from exactModel_GLPK import LotSizingGLPKTeamsFinder
from SimulatedAnnealing import SimulatedAnnealingPlanner, LotSizingSimulatedAnnealing
from UnifiedSolverManager import UnifiedSolverManager
from config import DEFAULT_FORECAST_FILE, DEFAULT_TEMP_INIT, DEFAULT_TEMP_FINAL, COOLING_RATE, MAX_ITERATIONS, MAX_ITERATIONS_PER_TEMP


if __name__ == "__main__":

    data_loader = Data(csv_file_path=DEFAULT_FORECAST_FILE)

    if data_loader.process():

        data_dict = data_loader.get_data_dict()

        data = data_dict['data']
        demand = data_dict['demand']
        T = data_dict['T']
        I = data_dict['I']
        shift_durations = data_dict['shift_durations']
        max_teams = data_dict['max_teams']
        min_teams = data_dict['min_teams']
        Cs = data_dict['Cs']
        production_times = data_dict['production_times']
        a = data_dict['a']
        cutting_time = data_dict['cutting_time']
        initial_stock = data_dict['initial_stock']
        components_number = data_dict['components_number']
        eps_stock_values = data_dict['eps_stock_values']
        eps_livraisons_values = data_dict['eps_livraisons_values']
        eps_teams_values = data_dict['eps_teams_values']
    # ========== RÉSOLUTION UNIFIÉE AVEC TOUS LES SOLVEURS ==========
    print("\n" + "=" * 70)
    print("RÉSOLUTION AVEC TOUS LES SOLVEURS DISPONIBLES")
    print("=" * 70)
    
    manager = UnifiedSolverManager(
        demand=demand,
        shift_durations=shift_durations,
        production_times=production_times,
        min_teams=min_teams,
        max_teams=max_teams,
        Cs=Cs,
        a=a,
        components_number=components_number,
        initial_stock=initial_stock,
        cutting_time=cutting_time
    )
    
    # Résoudre avec les trois solveurs exacts
    try:
        all_results = manager.solve_all_solvers(
            eps_stock_values,
            eps_livraisons_values,
            solvers=['Gurobi', 'GLPK'],
            T0=DEFAULT_TEMP_INIT,
            Tf=DEFAULT_TEMP_FINAL,
            alpha=COOLING_RATE,
            max_iter=MAX_ITERATIONS,
            max_iter_temp=MAX_ITERATIONS_PER_TEMP
        )
    except Exception as e:
        print(f"❌ Erreur lors de la résolution: {str(e)}")
        # Essayer au moins avec Gurobi et GLPK
        all_results = manager.solve_all_solvers(
            eps_stock_values,
            eps_livraisons_values,
            solvers=['Gurobi', 'GLPK']
        )
    
    # ========== AFFICHAGE ET SAUVEGARDE DES RÉSULTATS ==========
    print("\n" + "=" * 70)
    print("RÉSUMÉ DES SOLUTIONS PAR SOLVEUR")
    print("=" * 70)
    
    all_dfs = {}
    for solver_name, (solutions, df) in all_results.items():
        if solutions is not None:
            print(f"\n{solver_name}:")
            print("-" * 70)
            print(df.to_string(index=False))
            print(f"✅ {len(solutions)} solutions trouvées")
            
            # Sauvegarder
            manager.save_results(solver_name, solutions, df)
            all_dfs[solver_name] = df
        else:
            print(f"\n⚠️ {solver_name}: Pas de solutions")
    
    # ========== COMPARAISON DIRECTE ==========
    print("\n" + "=" * 70)
    print("COMPARAISON DIRECTE DE TOUS LES SOLVEURS")
    print("=" * 70)
    
    if all_dfs:
        comparison = UnifiedSolverManager.compare_solvers(all_dfs)
        print("\nRésultats côte à côte:")
        print(comparison.to_string(index=False))
        
        # Sauvegarder la comparaison
        comparison.to_csv("Outputs/all_solvers_comparison.csv", index=False)
        print("\n✅ Comparaison sauvegardée: Outputs/all_solvers_comparison.csv")
    
    # ========== ANALYSE PARETO ==========
    print("\n" + "=" * 70)
    print("ANALYSE PARETO GLOBALE (TOUS LES SOLVEURS)")
    print("=" * 70)
    
    if all_dfs:
        combined = pd.concat(all_dfs.values(), ignore_index=True)
        pareto_solutions = UnifiedSolverManager.analyze_pareto(combined)
        print("\nTop 5 solutions Pareto-optimales:")
        print(pareto_solutions.to_string(index=False))
        pareto_solutions.to_csv("Outputs/all_solvers_pareto.csv", index=False)
    
    print("\n" + "=" * 70)
    print("✅ RÉSOLUTION COMPLÈTE")
    print("=" * 70)
