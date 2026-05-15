# Simulation Module - AMPL Models

This folder contains AMPL (A Modeling Language for Mathematical Programming) model files for the factory planning problem.

## Files

### 1. `With_Regularization.mod`
- **Purpose**: Exact model with regularization
- **Type**: Binary AMPL model (compiled)
- **Use**: Solve the lot-sizing problem with regularization constraints
- **Solver**: GLPK or Gurobi

### 2. `Without_Regularization.mod`
- **Purpose**: Exact model without regularization
- **Type**: Binary AMPL model (compiled)
- **Use**: Solve the lot-sizing problem without regularization
- **Solver**: GLPK or Gurobi

### 3. `Commands_Generator.mod`
- **Purpose**: Model for generating optimization commands
- **Type**: Binary AMPL model (compiled)
- **Use**: Auxiliary model for command generation
- **Solver**: GLPK or Gurobi

## How to Use

These AMPL models can be used with AMPL solvers:

```bash
# Example with GLPK
ampl
model Simulation/With_Regularization.mod;
solve;
display solution;
exit;
```

## Mathematical Formulation

The models implement a multi-objective lot-sizing problem:

**Objectives:**
- Minimize total teams/shifts
- Minimize average stock
- Maximize on-time delivery rate

**Constraints:**
- Production capacity (shifts × duration)
- Storage capacity
- Demand satisfaction
- Team availability (min/max per period)

## Integration with Python

The Python modules (Gurobi and GLPK solvers) implement equivalent models and can be used for optimization without requiring AMPL.

Refer to:
- `Optim/Python/src/exactModel_Gurobi.py`
- `Optim/Python/src/exactModel_GLPK.py`

## References

- [AMPL Documentation](https://ampl.com/)
- [GLPK Documentation](https://www.gnu.org/software/glpk/)
- [Gurobi Documentation](https://www.gurobi.com/documentation/)
