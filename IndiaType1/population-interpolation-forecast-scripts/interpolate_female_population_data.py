import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

def interpolate_female_population_data():
    """
    Read the nordpred_female_population.txt file and interpolate data for all years
    from 1990 to 2021 using cubic spline interpolation. All population values are
    converted to integers and saved as a CSV file.
    """
    # Read the existing population data
    try:
        female_data = pd.read_csv('nordpred_female_population.txt', sep='\t')
        print(f"Successfully loaded female population data with {len(female_data)} age groups.")
    except FileNotFoundError:
        print("Error: nordpred_female_population.txt not found.")
        return
    
    # Define all years to interpolate
    all_years = np.array(list(range(1990, 2022)))
    census_years = [1991, 2001, 2011]
    
    # Create a new dataframe with all years
    interpolated_data = pd.DataFrame({'row.names': female_data['row.names']})
    
    # For each age group, interpolate the population for all years
    for age_group in female_data['row.names']:
        print(f"Interpolating data for age group: {age_group}")
        
        # Get the known values for census years
        known_years = []
        known_values = []
        
        for year in census_years:
            if str(year) in female_data.columns:
                known_years.append(year)
                known_values.append(int(female_data.loc[female_data['row.names'] == age_group, str(year)].values[0]))
        
        # Convert to numpy arrays for interpolation
        known_years = np.array(known_years)
        known_values = np.array(known_values)
        
        # Create cubic spline interpolator
        cs = CubicSpline(known_years, known_values)
        
        # Interpolate for all years
        interpolated_values = cs(all_years)
        
        # Ensure values are positive integers
        interpolated_values = np.maximum(interpolated_values, 0)
        interpolated_values = np.round(interpolated_values).astype(int)
        
        # Store the interpolated values
        for i, year in enumerate(all_years):
            interpolated_data.loc[interpolated_data['row.names'] == age_group, str(year)] = interpolated_values[i]
    
    # Convert all numeric columns to integers
    for col in interpolated_data.columns:
        if col != 'row.names':
            interpolated_data[col] = interpolated_data[col].astype(int)
    
    # Save the interpolated data as CSV
    interpolated_data.to_csv('nordpred_female_population_interpolated.csv', index=False)
    print("Interpolated female population data saved to nordpred_female_population_interpolated.csv")
    
    # Display the interpolated data
    print("\nInterpolated female population data (all values are integers):")
    # Set display option to show integers without decimals
    pd.set_option('display.float_format', lambda x: '{:.0f}'.format(x))
    print(interpolated_data)
    
    # Create visualizations of the interpolation for all age groups
    # Create a figure with two subplots - one for all age groups, one for selected groups
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 20))
    
    # Get all age groups
    all_age_groups = interpolated_data['row.names'].tolist()
    
    # Define a color map for the age groups
    colors = plt.cm.tab20(np.linspace(0, 1, len(all_age_groups)))
    
    # Plot all age groups in the first subplot
    for i, age_group in enumerate(all_age_groups):
        # Get the data for this age group
        age_data = interpolated_data.loc[interpolated_data['row.names'] == age_group].iloc[0, 1:].astype(int)
        
        # Plot the interpolated data
        ax1.plot(all_years, age_data, marker='o', label=age_group, color=colors[i], linewidth=2)
        
        # Highlight the census years
        for year in census_years:
            ax1.scatter(year, age_data[str(year)], s=100, color='red', zorder=5)
    
    ax1.set_title('All Age Groups: Interpolated Female Population (1990-2021)', fontsize=16)
    ax1.set_xlabel('Year', fontsize=14)
    ax1.set_ylabel('Population', fontsize=14)
    ax1.legend(loc='upper left', fontsize=12)
    ax1.grid(True)
    
    # Plot selected age groups in the second subplot for better visibility
    # Select a few representative age groups
    selected_age_groups = ['0-5', '15-39', '40-44', '70-74', '95+']
    
    for age_group in selected_age_groups:
        # Get the data for this age group
        age_data = interpolated_data.loc[interpolated_data['row.names'] == age_group].iloc[0, 1:].astype(int)
        
        # Plot the interpolated data
        ax2.plot(all_years, age_data, marker='o', label=age_group, linewidth=2)
        
        # Highlight the census years
        for year in census_years:
            ax2.scatter(year, age_data[str(year)], s=100, color='red', zorder=5)
    
    ax2.set_title('Selected Age Groups: Interpolated Female Population (1990-2021)', fontsize=16)
    ax2.set_xlabel('Year', fontsize=14)
    ax2.set_ylabel('Population', fontsize=14)
    ax2.legend(loc='upper left', fontsize=12)
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig('female_population_interpolation_all_groups.png', dpi=300)
    print("Visualization saved to female_population_interpolation_all_groups.png")
    
    # Create a second visualization with log scale for better comparison of different age groups
    plt.figure(figsize=(15, 10))
    
    for i, age_group in enumerate(all_age_groups):
        # Get the data for this age group
        age_data = interpolated_data.loc[interpolated_data['row.names'] == age_group].iloc[0, 1:].astype(int)
        
        # Plot the interpolated data
        plt.plot(all_years, age_data, marker='o', label=age_group, color=colors[i], linewidth=2)
        
        # Highlight the census years
        for year in census_years:
            plt.scatter(year, age_data[str(year)], s=100, color='red', zorder=5)
    
    plt.title('All Age Groups: Interpolated Female Population (1990-2021) - Log Scale', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Population (Log Scale)', fontsize=14)
    plt.yscale('log')
    plt.legend(loc='upper left', fontsize=12)
    plt.grid(True)
    plt.savefig('female_population_interpolation_log_scale.png', dpi=300)
    print("Visualization saved to female_population_interpolation_log_scale.png")
    
    return interpolated_data

if __name__ == "__main__":
    interpolate_female_population_data() 