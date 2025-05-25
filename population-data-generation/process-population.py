#!/usr/bin/env python3
"""
Population Data Processing Script

This script processes population data for a specific state and gender, interpolates missing years,
and generates forecasts using the Nordpred method.

License: Creative Commons Attribution 4.0 International License (CC BY 4.0)
See LICENSE file for details.
"""

import argparse
import os
from utils import process_census_data, interpolate_population, forecast_population, save_data, create_visualizations

def main():
    parser = argparse.ArgumentParser(description='Process population data for a specific state and gender.')
    parser.add_argument('--state', type=str, required=True, help='Name of the state to process')
    parser.add_argument('--gender', type=str, required=True, choices=['Male', 'Female'], help='Gender to process')
    args = parser.parse_args()

    # Define the census years and corresponding CSV files
    census_years = [1991, 2001, 2011]
    csv_files = [f'{year}.csv' for year in census_years]

    # Process census data
    print(f"Processing census data for {args.state} - {args.gender}...")
    processed_data = process_census_data(csv_files, args.state, args.gender)

    # Interpolate population data
    print("Interpolating population data from 1991 to 2021...")
    interpolated_data = interpolate_population(processed_data)

    # Forecast population
    print("Forecasting population for years [2025, 2030, 2035, 2040]...")
    forecast_data = forecast_population(interpolated_data)

    # Save data
    print("Saving data...")
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    save_data(interpolated_data, f'{output_dir}/{args.gender.lower()}-{args.state.lower()}.txt')
    save_data(forecast_data, f'{output_dir}/{args.gender.lower()}-{args.state.lower()}-pred.txt')

    # Create visualizations
    print("Creating visualizations...")
    create_visualizations(interpolated_data, forecast_data, output_dir)

    print("Processing completed successfully!")

if __name__ == '__main__':
    main() 