import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from scipy.optimize import curve_fit

def forecast_population():
    """
    Forecast population for both male and female age groups for the years 2025, 2030, 2035, and 2040
    using the interpolated data as a base.
    """
    # Load the interpolated data
    try:
        male_data = pd.read_csv('processed-files/nordpred_male_population_interpolated.txt')
        female_data = pd.read_csv('processed-files/nordpred_female_population_interpolated.txt')
        print(f"Successfully loaded interpolated data with {len(male_data)} age groups.")
    except FileNotFoundError:
        print("Error: Interpolated population files not found in processed-files folder. Please run the interpolation scripts first.")
        return
    
    # Define the years to forecast
    forecast_years = [2025, 2030, 2035, 2040]
    
    # Create dataframes for the forecasts
    male_forecast = pd.DataFrame({'row.names': male_data['row.names']})
    female_forecast = pd.DataFrame({'row.names': female_data['row.names']})
    
    # Define a function for exponential growth with saturation
    def growth_model(x, a, b, c):
        """Exponential growth with saturation model"""
        return a * (1 - np.exp(-b * (x - 1990))) + c
    
    # For each age group, forecast the population
    for age_group in male_data['row.names']:
        print(f"Forecasting data for age group: {age_group}")
        
        # Get the interpolated values for male
        male_years = np.array([int(year) for year in male_data.columns if year != 'row.names'])
        male_values = np.array([int(male_data.loc[male_data['row.names'] == age_group, str(year)].values[0]) 
                               for year in male_years])
        
        # Get the interpolated values for female
        female_years = np.array([int(year) for year in female_data.columns if year != 'row.names'])
        female_values = np.array([int(female_data.loc[female_data['row.names'] == age_group, str(year)].values[0]) 
                                 for year in female_years])
        
        # Fit the growth model to the male data
        try:
            male_popt, _ = curve_fit(growth_model, male_years, male_values, 
                                     p0=[male_values[-1], 0.01, male_values[0]], 
                                     maxfev=10000)
            
            # Forecast male population
            for year in forecast_years:
                forecast_value = int(growth_model(year, *male_popt))
                male_forecast.loc[male_forecast['row.names'] == age_group, str(year)] = forecast_value
        except:
            # If curve fitting fails, use linear extrapolation
            print(f"  Warning: Curve fitting failed for male {age_group}, using linear extrapolation")
            slope = (male_values[-1] - male_values[-5]) / 5
            for year in forecast_years:
                years_ahead = year - male_years[-1]
                forecast_value = int(male_values[-1] + slope * years_ahead)
                male_forecast.loc[male_forecast['row.names'] == age_group, str(year)] = forecast_value
        
        # Fit the growth model to the female data
        try:
            female_popt, _ = curve_fit(growth_model, female_years, female_values, 
                                       p0=[female_values[-1], 0.01, female_values[0]], 
                                       maxfev=10000)
            
            # Forecast female population
            for year in forecast_years:
                forecast_value = int(growth_model(year, *female_popt))
                female_forecast.loc[female_forecast['row.names'] == age_group, str(year)] = forecast_value
        except:
            # If curve fitting fails, use linear extrapolation
            print(f"  Warning: Curve fitting failed for female {age_group}, using linear extrapolation")
            slope = (female_values[-1] - female_values[-5]) / 5
            for year in forecast_years:
                years_ahead = year - female_years[-1]
                forecast_value = int(female_values[-1] + slope * years_ahead)
                female_forecast.loc[female_forecast['row.names'] == age_group, str(year)] = forecast_value
    
    # Save the forecast data
    male_forecast.to_csv('processed-files/nordpred_male_population_forecast.txt', index=False)
    female_forecast.to_csv('processed-files/nordpred_female_population_forecast.txt', index=False)
    print("Population forecasts saved to processed-files/nordpred_male_population_forecast.txt and processed-files/nordpred_female_population_forecast.txt")
    
    # Display the forecast data
    print("\nMale population forecast (all values are integers):")
    pd.set_option('display.float_format', lambda x: '{:.0f}'.format(x))
    print(male_forecast)
    
    print("\nFemale population forecast (all values are integers):")
    print(female_forecast)
    
    # Create visualizations of the forecasts
    # Create a figure with two subplots - one for male, one for female
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 20))
    
    # Get all age groups
    all_age_groups = male_data['row.names'].tolist()
    
    # Define a color map for the age groups
    colors = plt.cm.tab20(np.linspace(0, 1, len(all_age_groups)))
    
    # Plot male forecasts
    for i, age_group in enumerate(all_age_groups):
        # Get historical data
        historical_years = [int(year) for year in male_data.columns if year != 'row.names']
        historical_values = [int(male_data.loc[male_data['row.names'] == age_group, str(year)].values[0]) 
                           for year in historical_years]
        
        # Get forecast data
        forecast_values = [int(male_forecast.loc[male_forecast['row.names'] == age_group, str(year)].values[0]) 
                         for year in forecast_years]
        
        # Plot historical data
        ax1.plot(historical_years, historical_values, marker='o', label=age_group, color=colors[i], linewidth=2)
        
        # Plot forecast data with different style
        ax1.plot(forecast_years, forecast_values, marker='s', linestyle='--', color=colors[i], linewidth=2)
        ax1.scatter(forecast_years, forecast_values, s=100, color='green', zorder=5)
    
    ax1.set_title('Male Population Forecast (1990-2040)', fontsize=16)
    ax1.set_xlabel('Year', fontsize=14)
    ax1.set_ylabel('Population', fontsize=14)
    ax1.legend(loc='upper left', fontsize=12)
    ax1.grid(True)
    
    # Plot female forecasts
    for i, age_group in enumerate(all_age_groups):
        # Get historical data
        historical_years = [int(year) for year in female_data.columns if year != 'row.names']
        historical_values = [int(female_data.loc[female_data['row.names'] == age_group, str(year)].values[0]) 
                           for year in historical_years]
        
        # Get forecast data
        forecast_values = [int(female_forecast.loc[female_forecast['row.names'] == age_group, str(year)].values[0]) 
                         for year in forecast_years]
        
        # Plot historical data
        ax2.plot(historical_years, historical_values, marker='o', label=age_group, color=colors[i], linewidth=2)
        
        # Plot forecast data with different style
        ax2.plot(forecast_years, forecast_values, marker='s', linestyle='--', color=colors[i], linewidth=2)
        ax2.scatter(forecast_years, forecast_values, s=100, color='green', zorder=5)
    
    ax2.set_title('Female Population Forecast (1990-2040)', fontsize=16)
    ax2.set_xlabel('Year', fontsize=14)
    ax2.set_ylabel('Population', fontsize=14)
    ax2.legend(loc='upper left', fontsize=12)
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig('plots/population_forecast.png', dpi=300)
    print("Visualization saved to plots/population_forecast.png")
    
    # Create a second visualization with log scale
    plt.figure(figsize=(15, 10))
    
    # Plot selected age groups for both male and female
    selected_age_groups = ['0-5', '15-39', '40-44', '70-74', '95+']
    
    for age_group in selected_age_groups:
        # Get male historical data
        male_historical_years = [int(year) for year in male_data.columns if year != 'row.names']
        male_historical_values = [int(male_data.loc[male_data['row.names'] == age_group, str(year)].values[0]) 
                                for year in male_historical_years]
        
        # Get male forecast data
        male_forecast_values = [int(male_forecast.loc[male_forecast['row.names'] == age_group, str(year)].values[0]) 
                              for year in forecast_years]
        
        # Get female historical data
        female_historical_years = [int(year) for year in female_data.columns if year != 'row.names']
        female_historical_values = [int(female_data.loc[female_data['row.names'] == age_group, str(year)].values[0]) 
                                  for year in female_historical_years]
        
        # Get female forecast data
        female_forecast_values = [int(female_forecast.loc[female_forecast['row.names'] == age_group, str(year)].values[0]) 
                                for year in forecast_years]
        
        # Plot male data
        plt.plot(male_historical_years, male_historical_values, marker='o', 
                label=f'Male {age_group}', linewidth=2, linestyle='-')
        plt.plot(forecast_years, male_forecast_values, marker='s', 
                linewidth=2, linestyle='--', color=plt.gca().lines[-1].get_color())
        plt.scatter(forecast_years, male_forecast_values, s=100, color='green', zorder=5)
        
        # Plot female data
        plt.plot(female_historical_years, female_historical_values, marker='o', 
                label=f'Female {age_group}', linewidth=2, linestyle='-')
        plt.plot(forecast_years, female_forecast_values, marker='s', 
                linewidth=2, linestyle='--', color=plt.gca().lines[-1].get_color())
        plt.scatter(forecast_years, female_forecast_values, s=100, color='green', zorder=5)
    
    plt.title('Population Forecast by Gender and Age Group (1990-2040) - Log Scale', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Population (Log Scale)', fontsize=14)
    plt.yscale('log')
    plt.legend(loc='upper left', fontsize=12)
    plt.grid(True)
    plt.savefig('plots/population_forecast_log_scale.png', dpi=300)
    print("Visualization saved to plots/population_forecast_log_scale.png")
    
    return male_forecast, female_forecast

if __name__ == "__main__":
    forecast_population() 