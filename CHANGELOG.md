# Changelog

All notable changes to Production-DT are documented here.

## [1.0] - 2026-05-15

### Added
- Initial release of Production-DT
- Forecasting module with Prophet integration
- Optimization module supporting Gurobi, GLPK, and Simulated Annealing
- Streamlit web interface
- Multi-objective Pareto front analysis
- Data aggregation utilities
- Comprehensive documentation

### Features
- Automatic date format detection (daily/monthly/yearly)
- Multi-product demand forecasting
- Period-based aggregation (5, 10, 20 days)
- Unified solver manager for multiple backends
- 3D Pareto front visualization
- CSV export of all results

### Known Limitations
- Requires large datasets for accurate Prophet forecasting
- Gurobi requires commercial license
- Some visualizations require additional data files

---

## Future Roadmap

- [ ] REST API for production integration
- [ ] Real-time dashboard updates
- [ ] Advanced scheduling algorithms
- [ ] ML-based parameter optimization
- [ ] Docker containerization
- [ ] Multi-language UI support
