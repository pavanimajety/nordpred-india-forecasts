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
   - Copy the `nordpred.s` file to your working directory (required for nordpred analysis)

## Disease Data Processing: Usage

Note:  use `python3` in place of `python` based on your
installed python. It is suggested to add an alias for your
python for ease of use. 

1. **Navigate to the project directory**:
   ```bash
   cd <workspace>/nordpred-india-forecasts
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
- Ensure that the age-groups match between what the script expects and what is in your csv file. To see what the script expects, visit `nordpred-india-forecasts/reading-data/read_diabetes_data.py` and check `age_map`.

## Population file generation: Usage

### Population Data Processing

The population processing script (`process-population.py`) processes census data and generates population predictions.

#### Required Files
1. **Census Data Files**:
   - `1991.csv`: 1991 census data
   - `2001.csv`: 2001 census data
   - `2011.csv`: 2011 census data
   - These files should be in the input directory
   - CSV format with columns: State, Age, Males, Females

#### Running the Script
```bash
python NewPopulationScripts/process-population.py --state <state> --gender <gender> --input-dir <directory> --output-dir <directory>
```

#### Running the Script
```bash
python NewPopulationScripts/process-population.py --state <state> --gender <gender> --input-dir <directory> --output-dir <directory> [--start-year <year>] [--end-year <year>] [--forecast-years <years>]
```

Options:
- `--state`: State name (e.g., Goa)
- `--gender`: Gender (Male/Female)
- `--input-dir`: Directory containing census CSV files
- `--output-dir`: Directory to save output files (default: "output")
- `--start-year`: Start year for interpolation (default: 1990)
- `--end-year`: End year for interpolation (default: 2021)
- `--forecast-years`: Comma-separated list of years to forecast (default: "2025,2030,2035,2040")

#### Output Files
1. **Historical Population**: `population-{gender}-{state}.txt`
   - Contains interpolated population data from 1991 to 2021
   - Space-separated values
   - Years as columns, age groups as rows
   - Example: `population-male-goa.txt`

2. **Predicted Population**: `population-{gender}-{state}-pred.txt`
   - Contains population predictions for 2025-2040
   - Space-separated values
   - Years as columns, age groups as rows
   - Example: `population-male-goa-pred.txt`

3. **Visualization**: `population_forecast.png`
   - Shows historical and predicted population trends
   - Includes all age groups
   - Historical data (solid lines) and predictions (dashed lines)

#### Example
```bash
python NewPopulationScripts/process-population.py --state Goa --gender Male --input-dir NewPopulationScripts --output-dir output
```

This will:
1. Read census data from `NewPopulationScripts/1991.csv`, `2001.csv`, and `2011.csv`
2. Process data for Goa, male population
3. Generate interpolated data (1991-2021)
4. Create population predictions (2025-2040)
5. Save output files in the `output` directory
6. Create visualization of the population trends

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

This will:
1. Read census data from `NewPopulationScripts/1991.csv`, `2001.csv`, and `2011.csv`
2. Process data for {state}, {gender} population
3. Generate interpolated data from 1995 to 2020
4. Create population predictions for 2025-2045
5. Save output files in the `output` directory
6. Create visualization of the population trends


## Notes

- The script uses cubic spline interpolation for years between census data
- For forecasting, it uses cubic spline or linear interpolation
- All population values are rounded to integers
- Negative values are not allowed in the output 


### Nordpred Analysis

The nordpred analysis script (`run-nordpred-analysis.R`) performs age-standardized rate predictions using the nordpred package.

#### Required Files
1. **Cases file**: `{state}-t1_{gender}.txt`
   - Contains incidence data
   - Space-separated values
   - Years as columns, age groups as rows
   - Example: `goa-t1_male.txt`

2. **Historical Population**: `population-{gender}-{state}.txt`
   - Contains historical population data
   - Space-separated values
   - Years as columns, age groups as rows
   - Example: `population-male-goa.txt`

3. **Predicted Population**: `population-{gender}-{state}-pred.txt`
   - Contains future population predictions
   - Space-separated values
   - Years as columns, age groups as rows
   - Example: `population-male-goa-pred.txt`

#### Running the Analysis
```bash
Rscript run-nordpred-analysis.R --input-dir <directory> --state <state> --gender <gender> --plot-type <type>
```

Options:
- `--input-dir`: Directory containing input files (default: "test")
- `--state`: State name (e.g., goa)
- `--gender`: Gender (male/female)
- `--plot-type`: Type of plot to generate
  - `main`: Main prediction plot (default)
  - `trends`: Trend scenarios plot
  - `both`: Generate both plots

#### Trend Scenarios
The trends plot shows three different prediction scenarios:
1. **No trend** (solid black line): Assumes no change in rates
2. **Full trend** (dashed red line): Uses the full observed trend
3. **Recent trend** (dotted blue line): Uses a weighted trend, giving more weight to recent years

#### Output
- `nordpred_plot_{state}_{gender}.png`: Main prediction plot
- `nordpred_trends_{state}_{gender}.png`: Trend scenarios plot
- `nordpred_predictions_{state}_{gender}.csv`: Predicted rates

## Example

To process the Nagaland data:
```bash
python3 reading_data/read_diabetes_data.py 18-groups-1991-2021-input-data/Nagaland-18groups-1991-2021.csv --output-base nagaland_type1
```

To process the Global data:
```bash
python3 NewScripts/read_diabetes_data.py 18-groups-1991-2021-input-data/GlobalType1-18groups-1991-2021.csv --output-base NewScripts/processed-files/global_processed
```

To run nordpred analysis for Goa:
```bash
Rscript run-nordpred-analysis.R --input-dir test --state goa --gender male --plot-type both
```

## License

This project is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0). See the [LICENSE](LICENSE) file for details.

You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:
- Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. 