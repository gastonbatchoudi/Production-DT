import pandas as pd
import numpy as np
from gurobipy import Model, GRB, quicksum
from itertools import product
import time
from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting
import matplotlib.pyplot as plt

class LotSizingGurobiTeamsFinder:
    def __init__(self, demand, shift_durations, production_times, min_teams, max_teams, Cs, a,components_number,initial_stock,cutting_time):
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
        model = Model()
        model.Params.OutputFlag = 0  

        x = model.addVars(self.I, self.T, vtype=GRB.INTEGER, name="x")
        y = model.addVars(self.I, self.T, vtype=GRB.BINARY, name="y")
        s = model.addVars(self.I, self.T+1, vtype=GRB.INTEGER, name="s")
        n = model.addVars(self.T, vtype=GRB.INTEGER, name="n")

        for i in range(self.I):
            model.addConstr(s[i, 0] == self.initial_stock[i])

        for i in range(self.I):
            for t in range(self.T):
                model.addConstr(x[i, t] + s[i, t] == self.demand[i, t] + s[i, t+1])

        model.addConstr((1/self.T) * quicksum(s[i, t+1] for i in range(self.I) for t in range(self.T)) <= eps_stock)
        model.addConstr((1/(self.T*self.I)) * quicksum(y[i, t] for i in range(self.I) for t in range(self.T)) >= eps_livraisons)

        for t in range(self.T):
            model.addConstr(quicksum(self.production_times[i] * x[i, t] for i in range(self.I)) <= self.shift_durations[t] * n[t])
            model.addConstr(quicksum(self.cutting_time * self.components_number[i] * x[i, t] for i in range(self.I)) <= self.shift_durations[t] * n[t])
            model.addConstr(quicksum(s[i, t+1] for i in range(self.I)) <= self.Cs)
            model.addConstr(n[t] >= self.min_teams[t])
            model.addConstr(n[t] <= self.max_teams[t])

        for i in range(self.I):
            for t in range(self.T):
                model.addConstr(
                    quicksum(x[i, k] for k in range(t+1)) >= quicksum(self.demand[i, k] * y[i, k] for k in range(t+1))
                )

        model.setObjective(quicksum(n[t] for t in range(self.T)), GRB.MINIMIZE)

        model.optimize()

        if model.Status == GRB.OPTIMAL:
            total_shifts = sum(n[t].X for t in range(self.T))
            stock_moyen = (1/self.T) * sum(s[i, t+1].X for i in range(self.I) for t in range(self.T))
            livraisons_a_temps = (1/(self.T*self.I)) * sum(y[i, t].X for i in range(self.I) for t in range(self.T)) * 100

            matrice_x = pd.DataFrame([[x[i, t].X for i in range(self.I)] for t in range(self.T)])
            matrice_s = pd.DataFrame([[s[i, t+1].X for i in range(self.I)] for t in range(self.T)])
            shifts = pd.Series([n[t].X for t in range(self.T)])

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
        print(f"Temps total de résolution Gurobi : {resolution_time:.2f} secondes")
        return solutions
