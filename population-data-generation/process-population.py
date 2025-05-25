#!/usr/bin/env python3

import argparse
import os
from utils import process_census_data, interpolate_population, forecast_population, save_data, create_visualizations

def main():
    parser = argparse.ArgumentParser(description='Process population data for a specific state and gender.')
    parser.add_argument('--state', type=str, required=True, help='Name of the state to process')
    parser.add_argument('--gender', type=str, required=True, choices=['Male', 'Female'], help='Gender to process')
    parser.add_argument('--input-dir', type=str, required=True, help='Directory containing input population CSV files')
    parser.add_argument('--output-dir', type=str, default='output', help='Directory to save output files (default: output)')
    parser.add_argument('--start-year', type=int, default=1990, help='Start year for interpolation (default: 1990)')
    parser.add_argument('--end-year', type=int, default=2021, help='End year for interpolation (default: 2021)')
    parser.add_argument('--forecast-years', type=str, default='2025,2030,2035,2040', 
                       help='Comma-separated list of years to forecast (default: 2025,2030,2035,2040)')
    args = parser.parse_args()

    # Parse forecast years
    forecast_years = [int(year.strip()) for year in args.forecast_years.split(',')]

    # Define the census years and corresponding CSV files
    census_years = [1991, 2001, 2011]
    csv_files = [os.path.join(args.input_dir, f'{year}.csv') for year in census_years]

    # Process census data
    print(f"Processing census data for {args.state} - {args.gender}...")
    processed_data = process_census_data(csv_files, args.state, args.gender)

    # Interpolate population data
    print(f"Interpolating population data from {args.start_year} to {args.end_year}...")
    interpolated_data = interpolate_population(processed_data, args.start_year, args.end_year)

    # Forecast population
    print(f"Forecasting population for years {forecast_years}...")
    forecast_data = forecast_population(interpolated_data, forecast_years)

    # Save data
    print("Saving data...")
    os.makedirs(args.output_dir, exist_ok=True)
    save_data(interpolated_data, f'{args.output_dir}/population-{args.gender.lower()}-{args.state.lower()}.txt')
    save_data(forecast_data, f'{args.output_dir}/population-{args.gender.lower()}-{args.state.lower()}-pred.txt')

    # Create visualizations
    print("Creating visualizations...")
    create_visualizations(interpolated_data, forecast_data, args.output_dir)

    print("Processing completed successfully!")

if __name__ == '__main__':
    main() 