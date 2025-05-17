# Diabetes Data Processing

This project processes diabetes data from CSV files into nordpred-style output files.

## Requirements

- Python 3.x
- pandas
- numpy

## Setup

1. **Set up a Python environment** (if not already done):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

2. **Install Python dependencies**:
   ```bash
   pip install pandas numpy
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
   python NewScripts/read_diabetes_data.py <input_csv> --output-base <output_base>
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
python NewScripts/read_diabetes_data.py 18-groups-1991-2021-input-data/Nagaland-18groups-1991-2021.csv --output-base NewScripts/processed-files/nagaland_processed
```

To process the Global data:
```bash
python NewScripts/read_diabetes_data.py 18-groups-1991-2021-input-data/GlobalType1-18groups-1991-2021.csv --output-base NewScripts/processed-files/global_processed
```

## Notes

- The script automatically detects the CSV header format (multi-header or single-header) and extracts the year column accordingly.
- Confidence intervals in the data are handled by extracting the first value from each cell.
