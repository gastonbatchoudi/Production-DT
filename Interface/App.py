# AVOSDIM Factory Planning - Streamlit Interface

# This is the main Streamlit application file for the web interface
# It provides an interactive dashboard for:
# - Data loading and visualization
# - Demand forecasting with Prophet
# - Production optimization with multiple solvers
# - Pareto front analysis and visualization

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os
import tempfile

# Add module paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Forecasting', 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Optim', 'Python', 'src'))

try:
    from Forecast import ForecastModel
    from Aggregated_data import AggregatedData
    from Data import Data
    from exactModel_Gurobi import LotSizingGurobiTeamsFinder
    from exactModel_GLPK import LotSizingGLPKTeamsFinder
    from pareto_solutions import ParetoFront, ParetoFrontVisualizer
    from UnifiedSolverManager import UnifiedSolverManager
except ImportError as e:
    st.error(f"Import Error: {e}. Make sure all dependencies are installed.")

# Page configuration
st.set_page_config(
    page_title="AVOSDIM Factory",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Session state initialization
if 'forecast_results' not in st.session_state:
    st.session_state.forecast_results = None
if 'optimization_results' not in st.session_state:
    st.session_state.optimization_results = None
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'historical_data' not in st.session_state:
    st.session_state.historical_data = None
if 'forecast_df' not in st.session_state:
    st.session_state.forecast_df = None

# Main title
st.title("🏭 AVOSDIM Factory Planning System")

# Sidebar navigation
with st.sidebar:
    st.image(os.path.join(os.path.dirname(__file__), "Images", "Logo-Avosdim.jpg") if os.path.exists(os.path.join(os.path.dirname(__file__), "Images", "Logo-Avosdim.jpg")) else None, use_container_width=True)
    
    st.divider()
    st.header("📍 Navigation")
    page = st.radio(
        "Select Section:",
        ["🏠 Home", "📊 Analysis", "⚙️ Parameters", "📈 Forecasting", "🎯 Optimization"]
    )
    
    st.divider()
    st.subheader("📥 Data Loading")
    uploaded_file = st.file_uploader("Upload Excel/CSV", type=['xlsx', 'xls', 'csv'])
    
    if uploaded_file:
        st.info("File uploaded. Process in relevant section.")

# Page: Home
if page == "🏠 Home":
    st.header("🏠 Welcome to AVOSDIM Factory")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### About the System
        AVOSDIM is an integrated production planning system:
        1. **📈 Forecasting** - Demand predictions with Prophet
        2. **🎯 Optimization** - Multi-objective planning (Gurobi/GLPK)
        3. **📊 Visualization** - Interactive analysis dashboard
        """)
    
    with col2:
        st.markdown("### System Status")
        if st.session_state.data_loaded:
            st.success("✅ Data loaded")
        else:
            st.warning("⚠️ No data loaded")
        
        if st.session_state.forecast_results:
            st.success("✅ Forecasting done")
        else:
            st.info("ℹ️ No forecasts")

# Page: Analysis
elif page == "📊 Analysis":
    st.header("📊 Data Analysis")
    st.info("Load data from the sidebar to begin analysis.")

# Page: Parameters
elif page == "⚙️ Parameters":
    st.header("⚙️ Configuration")
    st.info("Configure production parameters and constraints here.")

# Page: Forecasting
elif page == "📈 Forecasting":
    st.header("📈 Demand Forecasting")
    st.info("Upload data and configure forecasting parameters.")

# Page: Optimization
elif page == "🎯 Optimization":
    st.header("🎯 Production Optimization")
    st.info("Select solver and optimization parameters.")
    
    col1, col2 = st.columns(2)
    with col1:
        solver = st.selectbox("Choose Solver:", ["GLPK (Free)", "Gurobi (Commercial)"])
    with col2:
        st.button("🚀 Run Optimization", disabled=not st.session_state.data_loaded)

st.divider()
st.caption("AVOSDIM v1.0 | Factory Planning System")
