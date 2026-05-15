# Forecasting Module Documentation

## Overview

The Forecasting module uses Facebook Prophet to generate demand predictions from historical data.

## Features

- **Automatic date format detection**: Supports daily, monthly, and yearly granularity
- **Multi-product forecasting**: Handles multiple products simultaneously
- **Error metrics**: Calculates MAE, MSE, RMSE for each product
- **PDF report generation**: Creates visualizations of all forecasts
- **Data aggregation**: Supports period-based aggregation (5, 10, 20 days)

## Usage

### Standalone CLI

```bash
cd Forecasting/src
python Forecast.py
```

### From Code

```python
from Forecast import ForecastModel

forecaster = ForecastModel(
    file_path="data/demand.xlsx",
    sheet_name="All_Data",
    date_column="Date",
    output_file="Forecasting/Outputs/Tables/forecast.csv",
    pdf_file="Forecasting/Outputs/graphs/forecast.pdf"
)

forecaster.load_data()
forecaster.train_and_forecast(periods=30)
forecaster.decumulate_forecasts()
forecaster.save_results()
forecaster.plot_forecasts_and_save_pdf()
```

## Data Aggregation

For optimization, aggregate forecasts into planning periods:

```bash
cd Forecasting/src
python Aggregated_data.py
```

This generates:
- `forecast_aggregated_5days.csv` (weekly)
- `forecast_aggregated_10days.csv` (biweekly)
- `forecast_aggregated_20days.csv` (monthly)

## Output Files

```
Forecasting/Outputs/
├── Tables/
│   ├── forecast_all.csv           # Complete predictions with intervals
│   ├── forecast_only.csv          # Forecast values only
│   ├── forecast_errors.csv        # MAE/MSE/RMSE per product
│   ├── forecast_aggregated_*.csv  # Aggregated by period
│   └──
└── graphs/
    ├── forecast_*.png             # Product forecasts (PNG)
    └── forecast.pdf               # All forecasts (PDF)
```

## Configuration

Key parameters in `Forecast.py`:
- `periods`: Number of periods to forecast (default: 30)
- `frequency`: Auto-detected as 'D' (daily), 'M' (monthly), 'Y' (yearly)

## Troubleshooting

**Error: FileNotFoundError**
- Verify the input file path exists
- Check sheet name matches exactly
- Verify date column name is correct

**Poor forecast accuracy**
- Ensure enough historical data (>30 periods recommended)
- Check for outliers in the data
- Consider seasonal patterns
