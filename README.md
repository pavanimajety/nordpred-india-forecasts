# Nordpred India Forecasts

This package contains scripts for processing, interpolating, and forecasting population data from census years.

## Requirements

- Python 3.6+
- Required packages:
  - pandas
  - numpy
  - scipy
  - matplotlib

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install required packages:
```bash
pip install pandas numpy scipy matplotlib
```

## Usage

The main script `process-population.py` processes population data for a specific state and gender. It takes census data from 1991, 2001, and 2011, interpolates the data for years in between, and forecasts future population.

### Input Data Format

The input CSV files should be named `1991.csv`, `2001.csv`, and `2011.csv` and should have the following format:
- A 'State' column containing state names
- Columns for each age group with gender (e.g., '0-4 Male', '5-9 Male', etc.)

### Running the Script

Basic usage:
```bash
python process-population.py --state "State Name" --gender Male
```

Full options:
```bash
python process-population.py \
    --state "State Name" \
    --gender Male \
    --input-dir /path/to/input \
    --output-dir /path/to/output \
    --start-year 1991 \
    --end-year 2021 \
    --forecast-years 2025 2030 2035 2040
```

### Output Files

The script generates the following output files in the specified output directory:

1. `{gender}-{state}.txt`: Contains interpolated population data from 1991 to 2021
2. `{gender}-{state}-pred.txt`: Contains forecasted population data for future years
3. `population_forecast.png`: Visualization of population trends
4. `population_forecast_log_scale.png`: Log-scale visualization of population trends

## Example

To process male population data for Nagaland:
```bash
python process-population.py --state "Nagaland" --gender Male --input-dir ../population-interpolation-forecast-scripts
```

This will create:
- `male-nagaland.txt`: Interpolated data from 1991-2021
- `male-nagaland-pred.txt`: Forecast data for 2025-2040
- Visualizations in the output directory

## Notes

- The script uses cubic spline interpolation for years between census data
- For forecasting, it uses cubic spline or linear interpolation
- All population values are rounded to integers
- Negative values are not allowed in the output 

## License

This project is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0). See the [LICENSE](LICENSE) file for details.

You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:
- Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. 