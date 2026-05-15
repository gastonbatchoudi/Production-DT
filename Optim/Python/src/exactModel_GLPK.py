import pandas as pd
from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpStatus, GLPK
from itertools import product
import time

class LotSizingGLPKTeamsFinder:
    def __init__(self, demand, shift_durations, production_times, min_teams, max_teams, Cs, a, components_number, initial_stock, cutting_time):
        self.demand = demand
        self.shift_durations = shift_durations
        self.production_times = production_times
        self.min_teams = min_teams
        self.max_teams = max_teams
        self.components_number = components_number
        self.initial_stock = initial_stock
        self.cutting_time = cutting_time
        self.Cs = Cs
        self.I, self.T = demand.shape
        self.a = a

    def solve_model(self, eps_stock, eps_livraisons):

        model = LpProblem("LotSizing", LpMinimize)

        x = LpVariable.dicts("x", [(i, t) for i in range(self.I) for t in range(self.T)],
                             lowBound=0, cat='Integer')
        y = LpVariable.dicts("y", [(i, t) for i in range(self.I) for t in range(self.T)],
                             cat='Binary')
        s = LpVariable.dicts("s", [(i, t) for i in range(self.I) for t in range(self.T+1)],
                             lowBound=0, cat='Integer')
        n = LpVariable.dicts("n", [t for t in range(self.T)],
                             lowBound=0, cat='Integer')

        for i in range(self.I):
            model += s[(i, 0)] == self.initial_stock[i], f"InitialStock_{i}"

        for i in range(self.I):
            for t in range(self.T):
                model += x[(i, t)] + s[(i, t)] == self.demand[i, t] + s[(i, t+1)], f"FlowBalance_{i}_{t}"

        model += (1/self.T) * lpSum(s[(i, t+1)] for i in range(self.I) for t in range(self.T)) <= eps_stock, "AvgStock"

        model += (1/(self.T*self.I)) * lpSum(y[(i, t)] for i in range(self.I) for t in range(self.T)) >= eps_livraisons, "OnTimeDelivery"

        for t in range(self.T):

            model += lpSum(self.production_times[i] * x[(i, t)] for i in range(self.I)) <= self.shift_durations[t] * n[t], f"ProductionCapacity_{t}"

            model += lpSum(self.cutting_time * self.components_number[i] * x[(i, t)] for i in range(self.I)) <= self.shift_durations[t] * n[t], f"CuttingCapacity_{t}"

            model += lpSum(s[(i, t+1)] for i in range(self.I)) <= self.Cs, f"StorageCapacity_{t}"

            model += n[t] >= self.min_teams[t], f"MinTeams_{t}"
            model += n[t] <= self.max_teams[t], f"MaxTeams_{t}"

        for i in range(self.I):
            for t in range(self.T):
                model += lpSum(x[(i, k)] for k in range(t+1)) >= lpSum(self.demand[i, k] * y[(i, k)] for k in range(t+1)), f"Delivery_{i}_{t}"

        model += lpSum(n[t] for t in range(self.T)), "TotalShifts"

        solver = GLPK(msg=0)
        model.solve(solver)

        if LpStatus[model.status] == 'Optimal':
            total_shifts = sum(n[t].varValue for t in range(self.T))
            stock_moyen = (1/self.T) * sum(s[(i, t+1)].varValue for i in range(self.I) for t in range(self.T))
            livraisons_a_temps = (1/(self.T*self.I)) * sum(y[(i, t)].varValue for i in range(self.I) for t in range(self.T)) * 100

            matrice_x = pd.DataFrame([[x[(i, t)].varValue for i in range(self.I)] for t in range(self.T)])
            matrice_s = pd.DataFrame([[s[(i, t+1)].varValue for i in range(self.I)] for t in range(self.T)])
            shifts = pd.Series([n[t].varValue for t in range(self.T)])

            objectifs = {
                'shifts': total_shifts,
                'stock_moyen': stock_moyen,
                'livraisons': livraisons_a_temps
            }

            return objectifs, matrice_x, matrice_s, shifts

        return None

    def get_all_solutions(self, eps_stock_values, eps_livraisons_values):
        solutions = []
        start_time = time.time()

        for eps_stock, eps_livraisons in product(eps_stock_values, eps_livraisons_values):
            result = self.solve_model(eps_stock, eps_livraisons)
            if result:
                objectifs, x, s, shifts = result
                solutions.append({
                    'objectifs': objectifs, 
                    'x': x, 
                    's': s, 
                    'shifts': shifts,
                    'eps_stock': eps_stock,
                    'eps_livraisons': eps_livraisons
                })

        end_time = time.time()
        resolution_time = end_time - start_time
        print(f"Temps total de résolution GLPK : {resolution_time:.2f} secondes")
        return solutions
