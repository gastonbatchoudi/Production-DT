# 🏭 Production-DT - Factory Planning System

> **Note**: This repository contains the **source code only**. Data files are excluded for privacy/size. See [Setup & Usage](#-setup--usage) below.

## Overview

**Production-DT** est un système complet de planification de production en trois étapes:

- 📈 **Forecasting**: Prévisions de demande avec Prophet
- 🎯 **Optimization**: Planification optimale avec Gurobi/GLPK
- 🖥️ **Interface**: Dashboard Streamlit pour visualisation et gestion

### Tech Stack
- **Python 3.10+**
- **Framework**: Streamlit (Web Interface)
- **ML**: Facebook Prophet (Forecasting)
- **Optimization**: Gurobi, GLPK (Exact solvers), Simulated Annealing (Heuristic)
- **Data**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib

---

## 📁 Project Structure

```
Production-DT/
├── README.md                          ← You are here
├── .gitignore                         ← Excludes data & outputs
│
├── Forecasting/                       # Demand Forecasting Module
│   ├── README.md                      # Detailed documentation
│   ├── requirements.txt               # Dependencies
│   └── src/
│       ├── Forecast.py               # Prophet forecasting class
│       └── Aggregated_data.py        # Data aggregation by periods
│
├── Optim/                             # Optimization Module
│   └── Python/
│       ├── requirements.txt           # Dependencies
│       └── src/
│           ├── config.py             # Centralized configuration
│           ├── Main.py               # CLI entry point
│           ├── Data.py               # Data loader
│           ├── UnifiedSolverManager.py    # Solver manager
│           ├── exactModel_Gurobi.py      # Gurobi solver
│           ├── exactModel_GLPK.py       # GLPK solver
│           ├── SimulatedAnnealing.py     # SA heuristic
│           └── pareto_solutions.py       # Pareto front analysis
│
├── Interface/                         # Streamlit Web Interface
│   ├── README.md                      # Usage guide
│   ├── requirements.txt               # Dependencies
│   ├── App.py                        # Main application
│   ├── translations.py               # UI translations
│   ├── run.ps1                       # Launch script (Windows)
│   ├── run.bat                       # Launch script (Windows)
│   └── Images/                       # UI assets
│
└── Simulation/                        # AMPL/GLPK Model Files
    ├── With_Regularization.mod
    ├── Without_Regularization.mod
    └── Commands_Generator.mod
```

---

## 🚀 Setup & Usage

### Prerequisites
- Python 3.10+ (Windows/Linux/macOS)
- ~2GB disk space for dependencies (excluding data)
- Optional: Gurobi license (or use free GLPK)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/Production-DT.git
cd Production-DT
```

### 2️⃣ Create Python Virtual Environment

**Windows (PowerShell)**:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/macOS**:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
# Forecasting module
cd Forecasting
pip install -r requirements.txt
cd ..

# Optimization module
cd Optim/Python
pip install -r requirements.txt
cd ../..

# Interface
cd Interface
pip install -r requirements.txt
cd ..
```

### 4️⃣ Prepare Your Data

Create a CSV/Excel file with demand data:
- **Format**: Columns = Products, Rows = Time periods (dates or periods)
- **Location**: Place in `data/` folder (create if needed)
- **Example**: `data/planif.csv` or `data/demand.xlsx`

### 5️⃣ Run the System

#### Option A: Web Interface (Recommended)

```bash
cd Interface
streamlit run App.py
```

Interface opens at: **http://localhost:8501**

#### Option B: CLI Mode

```bash
# 1. Generate forecasts
cd Forecasting/src
python Forecast.py

# 2. Aggregate data
python Aggregated_data.py

# 3. Run optimization
cd ../../Optim/Python/src
python Main.py
```

---

## 🔧 Available Solvers

| Solver | Type | License | Status |
|--------|------|---------|--------|
| **GLPK** | Exact (LP/MIP) | Free (GPL) | ✅ Recommended |
| **Gurobi** | Exact (LP/MIP) | Commercial | ✅ Supported |
| **Simulated Annealing** | Heuristic | Free | ✅ Included |

### Configuration

Edit `Optim/Python/src/config.py` to adjust:
- Default forecast file
- Cooling rate & temperature (SA)
- Storage capacity
- Team constraints

---

## 📊 Workflow

### Typical Production Planning Cycle:

1. **📥 Load Data** → Upload historical demand data
2. **📈 Forecast** → Generate demand predictions (Prophet)
3. **⚙️ Configure** → Set constraints & parameters
4. **🎯 Optimize** → Find Pareto-optimal production plans
5. **📊 Analyze** → Visualize solutions & trade-offs
6. **💾 Export** → Download results (CSV, charts)

---

## 📝 Configuration Files

### Key Configuration: `Optim/Python/src/config.py`

```python
DEFAULT_FORECAST_FILE = "forecast_aggregated_20days.csv"
DEFAULT_TEMP_INIT = 500
COOLING_RATE = 0.95
MAX_ITERATIONS = 100
STORAGE_CAPACITY = 80000
AVAILABLE_SOLVERS = ['Gurobi', 'GLPK']
```

---

## 🧪 Testing

### Test 1: Verify Imports
```bash
cd Optim/Python/src
python -c "from config import *; print('✅ Configuration OK')"
```

### Test 2: Run Forecasting
```bash
cd Forecasting/src
python Forecast.py
# Check: Forecasting/Outputs/Tables/ for CSV files
```

### Test 3: Run Full Optimization
```bash
cd Optim/Python/src
python Main.py
# Check: Optim/Python/Outputs/ for results
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
streamlit run Interface/App.py --server.port 8502
```

### Module Not Found
```bash
# Ensure venv is activated and dependencies installed
pip install -r Interface/requirements.txt
pip install -r Forecasting/requirements.txt
pip install -r Optim/Python/requirements.txt
```

### No Gurobi License
```
→ Use GLPK solver (free, works well for medium-sized problems)
→ No license key needed
```

### Optimization Too Slow
```
→ Try GLPK instead of Gurobi
→ Reduce epsilon tolerance parameters
→ Reduce problem size (fewer products/periods)
```

---

## 📚 Documentation

- [Forecasting Module](Forecasting/README.md) - Prophet setup & usage
- [Interface Guide](Interface/README.md) - Streamlit UI walkthrough
- [Optimization Details](Optim/Python/src/config.py) - Solver configuration

---

## 📋 License

**Production-DT** - Factory Planning System  
Copyright © 2024-2026 | All Rights Reserved

### Dependencies Licensing
- [Facebook Prophet](https://facebook.github.io/prophet/) - BSD 3-Clause
- [Gurobi](https://www.gurobi.com/) - Commercial (academic licenses available)
- [GLPK](https://www.gnu.org/software/glpk/) - GPL 3.0
- [Streamlit](https://streamlit.io/) - Apache 2.0
- [Pandas/NumPy](https://pandas.pydata.org/) - BSD 3-Clause
- [Plotly](https://plotly.com/) - MIT
- [Matplotlib](https://matplotlib.org/) - PSF

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📞 Support

For issues or questions:
1. Check [Troubleshooting](#-troubleshooting) section
2. Review [Documentation](#-documentation)
3. Check logs: `streamlit run App.py --logger.level=debug`
4. Open a GitHub issue with:
   - Python version
   - Error message
   - Steps to reproduce

---

**Version**: 1.0 (Source Code Release)  
**Status**: ✅ Production Ready  
**Last Updated**: May 2026
