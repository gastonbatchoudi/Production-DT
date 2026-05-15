# Contributing Guidelines

We welcome contributions to Production-DT! Please follow these guidelines:

## Development Setup

1. Clone and create a feature branch
```bash
git clone https://github.com/gastonbatchoudi/Production-DT.git
cd Production-DT
git checkout -b feature/your-feature
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 on Windows
```

3. Install development dependencies
```bash
pip install -r Forecasting/requirements.txt
pip install -r Optim/Python/requirements.txt
pip install -r Interface/requirements.txt
pip install black pytest
```

## Code Style

- Use Black for formatting: `black .`
- Follow PEP 8 guidelines
- Write docstrings for all functions

## Testing

- Test forecast module: `python Forecasting/src/Forecast.py`
- Test optimization: `python Optim/Python/src/Main.py`
- Test interface: `streamlit run Interface/App.py`

## Pull Request Process

1. Ensure code is well-documented
2. Add test coverage for new features
3. Update README if needed
4. Submit PR with clear description

## Issues & Bugs

- Report issues on GitHub with:
  - Clear title and description
  - Steps to reproduce
  - Expected vs actual behavior
  - Python/package versions

---

**Thank you for contributing!**
