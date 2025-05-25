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
3. **Set up R environment**:
   - Install R from [CRAN](https://cran.r-project.org/).
   - Install required R packages:
     ```bash
     Rscript -e "install.packages(c('dplyr', 'ggplot2', 'tidyr'), repos='https://cran.rstudio.com/')"
     ```

## Usage

1. **Navigate to the project directory**:
   ```bash
   cd /path/to/disease-analysis
   ```

2. **Run the script**:
   ```bash
   python reading-data/read_diabetes_data.py <input_csv> --output-base <output_base>
   ```
   - `<input_csv>`: Path to the input CSV file (e.g., `18-groups-1991-2021-input-data/Nagaland-18groups-1991-2021.csv`).
   - `<output_base>`: Base name for the output files (e.g., `NewScripts/processed-files/nagaland_processed`).

   If `--output-base` is not provided, the script will prompt you to enter a base name.

3. **Output**:
   - The script generates two files:
     - `<output_base>_male.txt`
     - `<output_base>_female.txt`
   - These files are in nordpred format (tab-separated text, years as columns, age groups as rows).

## Example

To process the Nagaland data:
```bash
python3 reading-data/read_diabetes_data.py 18-groups-1991-2021-input-data/Nagaland-18groups-1991-2021.csv --output-base NewScripts/processed-files/nagaland_processed
```

To process the Global data:
```bash
python3 reading-data/read_diabetes_data.py 18-groups-1991-2021-input-data/GlobalType1-18groups-1991-2021.csv --output-base NewScripts/processed-files/global_processed
```

## Notes

- The script automatically detects the CSV header format (multi-header or single-header) and extracts the year column accordingly.
- Confidence intervals in the data are handled by extracting the first value from each cell.


## Usage

The main script `process-population.py` processes population data for a specific state and gender. It takes census data from 1991, 2001, and 2011, interpolates the data for years in between, and forecasts future population.

### Input Data Format

The input CSV files should be named `1991.csv`, `2001.csv`, and `2011.csv` and should have the following format:
- A 'State' column containing state names
- Columns for each age group with gender (e.g., '0-4 Male', '5-9 Male', etc.)

### Running the Script

Basic usage:
```bash
python3 process-population.py --state "State Name" --gender Male
```

Full options:
```bash
python3 process-population.py \
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
python process-population.py3 --state "Nagaland" --gender Male --input-dir ../population-interpolation-forecast-scripts
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