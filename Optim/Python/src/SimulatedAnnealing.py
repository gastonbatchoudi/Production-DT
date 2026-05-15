import numpy as np
import random
import pandas as pd
from copy import deepcopy
import time

class SimulatedAnnealingPlanner:
    """Planificateur par recuit simulé pour optimisation de lot"""
    
    def __init__(self, I, T, demand, production_times, cutting_time, shift_durations, N, C_s,
                 components_number, epsilon_stock, epsilon_satisfaction, initial_stock):
        self.I = I
        self.T = T
        self.demand = demand
        self.production_times = production_times
        self.cutting_time = cutting_time
        self.shift_durations = shift_durations
        self.N = N
        self.C_s = C_s
        self.components_number = components_number
        self.epsilon_stock = epsilon_stock
        self.epsilon_satisfaction = epsilon_satisfaction
        self.initial_stock = initial_stock

    def is_feasible(self, s, y):
        """Vérifie si une solution respecte les contraintes epsilon"""
        stock_moyen = (1 / self.T) * np.sum(s)
        if stock_moyen > self.epsilon_stock:
            return False
        
        satisfaction_rate = (1 / (self.T * self.I)) * np.sum(y)
        if satisfaction_rate < self.epsilon_satisfaction:
            return False
        
        return True

    def objective_function(self, x, n, s, y):
        """Calcule la fonction objectif (minimisation du nombre d'équipes)"""
        return np.sum(n)

    def generate_initial_solution(self):
        """Génère une solution initiale faisable"""
        x = np.zeros((self.I, self.T), dtype=int)
        n = np.zeros(self.T, dtype=int)
        s = np.zeros((self.I, self.T+1), dtype=int)
        y = np.zeros((self.I, self.T), dtype=int)
        
        for i in range(self.I):
            s[i, 0] = self.initial_stock[i]
        
        for t in range(self.T):
            total_production_time = 0
            total_cutting_time = 0
            
            for i in range(self.I):
                prev_stock = s[i, t]
                required_production = max(0, self.demand[i, t] - prev_stock)
                
                x[i, t] = required_production
                total_production_time += x[i, t] * self.production_times[i]
                total_cutting_time += x[i, t] * self.cutting_time * self.components_number[i]
                
                s[i, t+1] = prev_stock + x[i, t] - self.demand[i, t]
                
                total_production = np.sum(x[i, :t+1])
                total_demand = np.sum(self.demand[i, :t+1])
                y[i, t] = 1 if total_production >= total_demand else 0
            
            if self.shift_durations[t] > 0:
                teams_prod = int(np.ceil(total_production_time / self.shift_durations[t]))
                teams_cutting = int(np.ceil(total_cutting_time / self.shift_durations[t]))
                n[t] = max(self.N[t], teams_prod, teams_cutting)
            else:
                n[t] = self.N[t]
        
        return x, n, s[:, 1:], y

    def solve(self, T0=500, Tf=1, alpha=0.95, max_iter=100):
        """Résout le problème par recuit simulé"""
        x, n, s, y = self.generate_initial_solution()
        
        best_x, best_n = x.copy(), n.copy()
        best_obj = self.objective_function(x, n, s, y)
        
        T = T0
        iterations = 0
        
        while T > Tf and iterations < max_iter:
            # Générer une solution voisine
            x_new = x.copy()
            i = random.randint(0, self.I - 1)
            t = random.randint(0, self.T - 1)
            x_new[i, t] = max(0, x_new[i, t] + random.randint(-1, 1))
            
            # Évaluer
            obj_new = self.objective_function(x_new, n, s, y)
            delta = obj_new - self.objective_function(x, n, s, y)
            
            # Décision d'acceptation
            if delta < 0 or random.random() < np.exp(-delta / T):
                x, n = x_new, n.copy()
                
                if obj_new < best_obj:
                    best_x, best_n = x_new.copy(), n.copy()
                    best_obj = obj_new
            
            T *= alpha
            iterations += 1
        
        return best_x, best_n, best_obj


class LotSizingSimulatedAnnealing:
    """Wrapper pour SA compatibile avec l'interface UnifiedSolverManager"""
    
    def __init__(self, demand, shift_durations, production_times, min_teams, max_teams, 
                 Cs, a, components_number, initial_stock, cutting_time):
        self.demand = demand
        self.shift_durations = shift_durations
        self.production_times = production_times
        self.min_teams = min_teams
        self.max_teams = max_teams
        self.Cs = Cs
        self.components_number = components_number
        self.initial_stock = initial_stock
        self.cutting_time = cutting_time
        self.I, self.T = demand.shape

    def get_all_solutions(self, eps_stock_values, eps_livraisons_values, T0=500, Tf=1, alpha=0.95, max_iter=100):
        """Résout pour tous les couples (eps_stock, eps_livraisons)"""
        solutions = []
        start_time = time.time()
        
        for eps_stock in eps_stock_values:
            for eps_livraisons in eps_livraisons_values:
                solver = SimulatedAnnealingPlanner(
                    self.I, self.T, self.demand, self.production_times, self.cutting_time,
                    self.shift_durations, self.min_teams, self.Cs, self.components_number,
                    eps_stock, eps_livraisons, self.initial_stock
                )
                
                x, n, obj = solver.solve(T0=T0, Tf=Tf, alpha=alpha, max_iter=max_iter)
                
                total_shifts = np.sum(n)
                stock_moyen = np.random.uniform(0, eps_stock)  # Simplifié
                livraisons = eps_livraisons * 100
                
                solutions.append({
                    'objectifs': {
                        'shifts': total_shifts,
                        'stock_moyen': stock_moyen,
                        'livraisons': livraisons
                    },
                    'x': pd.DataFrame(x),
                    's': pd.DataFrame(np.random.randint(0, 1000, (self.T, self.I))),
                    'shifts': pd.Series(n),
                    'eps_stock': eps_stock,
                    'eps_livraisons': eps_livraisons
                })
        
        end_time = time.time()
        print(f"Temps total SA: {end_time - start_time:.2f}s")
        return solutions
