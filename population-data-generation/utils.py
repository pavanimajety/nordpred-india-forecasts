import pandas as pd
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import os

def clean_column_name(col_name):
    """Clean column name by removing BOM and other special characters."""
    return col_name.replace('\ufeff', '')

def get_age_value(age_str):
    """Convert age string to numeric value for comparison."""
    if age_str == 'All ages':
        return -1
    elif age_str == 'Age not stated':
        return float('inf')
    elif age_str.endswith('+'):
        return int(age_str[:-1])
    elif '-' in age_str:
        return int(age_str.split('-')[0])
    else:
        return int(age_str)

def process_census_data(csv_files, state_name, gender):
    """
    Process census data from multiple CSV files for a specific state and gender.
    
    Args:
        csv_files (list): List of CSV file paths for different census years
        state_name (str): Name of the state to process
        gender (str): Gender to process ('Male' or 'Female')
    
    Returns:
        pd.DataFrame: Processed data with age groups as rows and years as columns
    """
    # Define the target age groups
    target_age_groups = [
        '0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39',
        '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79',
        '80-84', '85+'
    ]
    
    # Create empty dataframe with age groups
    processed_data = pd.DataFrame({'row.names': target_age_groups})
    
    # Process each census year
    for csv_file in csv_files:
        # Extract year from filename
        year = int(os.path.basename(csv_file).split('.')[0])  # Extract year from filename
        
        # Read the CSV file
        df = pd.read_csv(csv_file)
        
        # Convert state names to lowercase for case-insensitive matching
        df['State'] = df['State'].str.lower()
        state_name_lower = state_name.lower()
        
        # Filter for the specific state
        df_state = df[df['State'] == state_name_lower]
        
        if df_state.empty:
            raise ValueError(f"No data found for state: {state_name} in {csv_file}")
        
        # Process each target age group
        for target_age_group in target_age_groups:
            # Parse target age range
            if target_age_group.endswith('+'):
                min_age = int(target_age_group[:-1])
                max_age = float('inf')
            else:
                min_age, max_age = map(int, target_age_group.split('-'))
            
            matching_rows = []
            for _, row in df_state.iterrows():
                age_str = row['Age']
                # For '0-4' output group, accept both '0-4' and '0-6' from input
                if target_age_group == '0-4' and age_str in ['0-4', '0-6']:
                    matching_rows.append(row)
                    continue
                age_value = get_age_value(age_str)
                if age_str == 'All ages' or age_str == 'Age not stated':
                    continue
                # Handle age ranges in the data
                if '-' in age_str:
                    data_min, data_max = map(int, age_str.split('-'))
                    if data_min >= min_age and data_max <= max_age:
                        matching_rows.append(row)
                # Handle individual ages
                elif age_value >= min_age and age_value <= max_age:
                    matching_rows.append(row)
                # Handle 80+ case
                elif age_str.endswith('+') and min_age >= 80:
                    matching_rows.append(row)
            
            # Calculate total population for this age group
            total_population = sum(int(row[gender + 's']) for row in matching_rows)
            
            # Store the total population
            processed_data.loc[processed_data['row.names'] == target_age_group, str(year)] = total_population
    
    return processed_data

def interpolate_population(processed_data, start_year=1990, end_year=2021):
    """
    Interpolate population data for years between census years.
    
    Args:
        processed_data (pd.DataFrame): Processed census data
        start_year (int): Start year for interpolation
        end_year (int): End year for interpolation
    
    Returns:
        pd.DataFrame: Interpolated data for all years
    """
    # Get census years from the data
    census_years = [int(col) for col in processed_data.columns if col != 'row.names']
    
    # Create array of all years to interpolate
    all_years = np.array(list(range(start_year, end_year + 1)))
    
    # Create new dataframe for interpolated data
    interpolated_data = pd.DataFrame({'row.names': processed_data['row.names']})
    
    # For each age group, interpolate the population
    for age_group in processed_data['row.names']:
        # Get known values for census years
        known_years = []
        known_values = []
        
        for year in census_years:
            if str(year) in processed_data.columns:
                known_years.append(year)
                known_values.append(int(processed_data.loc[processed_data['row.names'] == age_group, str(year)].values[0]))
        
        # Convert to numpy arrays
        known_years = np.array(known_years)
        known_values = np.array(known_values)
        
        # For older age groups (70+), use linear interpolation
        is_older_age = any(age in age_group for age in ['70', '75', '80', '85'])
        if is_older_age:
            # Linear interpolation
            interpolated_values = np.interp(all_years, known_years, known_values)
        else:
            try:
                # Try cubic spline interpolation
                cs = CubicSpline(known_years, known_values)
                interpolated_values = cs(all_years)
                
                # Check if interpolation produced negative values
                if np.any(interpolated_values < 0):
                    # Fall back to linear interpolation
                    interpolated_values = np.interp(all_years, known_years, known_values)
            except:
                # Fall back to linear interpolation if cubic spline fails
                interpolated_values = np.interp(all_years, known_years, known_values)
        
        # Ensure values are positive integers
        interpolated_values = np.maximum(interpolated_values, 0)
        interpolated_values = np.round(interpolated_values).astype(int)
        
        # Store interpolated values
        for i, year in enumerate(all_years):
            interpolated_data.loc[interpolated_data['row.names'] == age_group, str(year)] = interpolated_values[i]
    
    return interpolated_data

def forecast_population(interpolated_data, forecast_years=[2025, 2030, 2035, 2040]):
    """
    Forecast population for future years using interpolated data.
    
    Args:
        interpolated_data (pd.DataFrame): Interpolated population data
        forecast_years (list): List of years to forecast
    
    Returns:
        pd.DataFrame: Forecast data for future years
    """
    # Create dataframe for forecasts
    forecast_data = pd.DataFrame({'row.names': interpolated_data['row.names']})
    
    age_groups = list(interpolated_data['row.names'])
    
    # First pass: calculate all forecasts
    for idx, age_group in enumerate(age_groups):
        years = np.array([int(year) for year in interpolated_data.columns if year != 'row.names'])
        values = np.array([int(interpolated_data.loc[interpolated_data['row.names'] == age_group, str(year)].values[0]) 
                          for year in years])
        
        # Use the same interpolation function as in interpolate_population
        try:
            cs = CubicSpline(years, values)
            for year in forecast_years:
                forecast_value = int(cs(year))
                forecast_data.loc[forecast_data['row.names'] == age_group, str(year)] = forecast_value
        except:
            # Fall back to linear interpolation if cubic spline fails
            for year in forecast_years:
                forecast_value = int(np.interp(year, years, values))
                forecast_data.loc[forecast_data['row.names'] == age_group, str(year)] = forecast_value
    
    return forecast_data

def save_data(data, filename):
    """Save data to a file with space separator and integer values."""
    # Make a copy to avoid modifying the original DataFrame
    data_to_save = data.copy()
    # Convert all columns except 'row.names' to int
    for col in data_to_save.columns:
        if col != 'row.names':
            data_to_save[col] = data_to_save[col].astype(int)
    data_to_save.to_csv(filename, index=False, sep=' ')

def create_visualizations(interpolated_data, forecast_data, output_dir):
    """
    Create visualizations of the population data and forecasts.
    
    Args:
        interpolated_data (pd.DataFrame): Interpolated population data
        forecast_data (pd.DataFrame): Forecast population data
        output_dir (str): Directory to save visualizations
    """
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 20))
    
    # Get all age groups
    all_age_groups = interpolated_data['row.names'].tolist()
    
    # Define colors
    colors = plt.cm.tab20(np.linspace(0, 1, len(all_age_groups)))
    
    # Plot historical and interpolated data
    historical_years = [int(year) for year in interpolated_data.columns if year != 'row.names']
    forecast_years = [int(year) for year in forecast_data.columns if year != 'row.names']
    
    for i, age_group in enumerate(all_age_groups):
        # Get historical data
        historical_values = [int(interpolated_data.loc[interpolated_data['row.names'] == age_group, str(year)].values[0]) 
                           for year in historical_years]
        
        # Get forecast data
        forecast_values = [int(forecast_data.loc[forecast_data['row.names'] == age_group, str(year)].values[0]) 
                         for year in forecast_years]
        
        # Plot historical data
        ax1.plot(historical_years, historical_values, marker='o', label=age_group, color=colors[i], linewidth=2)
        
        # Plot forecast data
        ax1.plot(forecast_years, forecast_values, marker='s', linestyle='--', color=colors[i], linewidth=2)
        ax1.scatter(forecast_years, forecast_values, s=100, color='green', zorder=5)
    
    ax1.set_title('Population Forecast (1991-2040)', fontsize=16)
    ax1.set_xlabel('Year', fontsize=14)
    ax1.set_ylabel('Population', fontsize=14)
    ax1.legend(loc='upper left', fontsize=12)
    ax1.grid(True)
    
    # Create log scale plot
    plt.figure(figsize=(15, 10))
    
    # Plot selected age groups
    selected_age_groups = ['0-4', '15-19', '40-44', '70-74', '85+']
    
    for age_group in selected_age_groups:
        # Get historical data
        historical_values = [int(interpolated_data.loc[interpolated_data['row.names'] == age_group, str(year)].values[0]) 
                           for year in historical_years]
        
        # Get forecast data
        forecast_values = [int(forecast_data.loc[forecast_data['row.names'] == age_group, str(year)].values[0]) 
                         for year in forecast_years]
        
        # Plot data
        plt.plot(historical_years, historical_values, marker='o', label=age_group, linewidth=2)
        plt.plot(forecast_years, forecast_values, marker='s', linestyle='--', 
                color=plt.gca().lines[-1].get_color(), linewidth=2)
        plt.scatter(forecast_years, forecast_values, s=100, color='green', zorder=5)
    
    plt.title('Population Forecast by Age Group (1991-2040) - Log Scale', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Population (Log Scale)', fontsize=14)
    plt.yscale('log')
    plt.legend(loc='upper left', fontsize=12)
    plt.grid(True)
    
    # Save the plot
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'population_forecast.png'), dpi=300, bbox_inches='tight')
    plt.close() 