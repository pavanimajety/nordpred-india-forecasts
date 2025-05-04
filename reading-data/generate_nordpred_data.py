import pandas as pd
import numpy as np

def generate_nordpred_data(df, gender):
    """
    Generate nordpred data for the specified gender.
    
    Args:
        df: DataFrame containing the diabetes data
        gender: String, either 'Male' or 'Female'
    
    Returns:
        DataFrame in nordpred format
    """
    # Define age groups in the correct order
    age_groups = ['0-5', '5-14', '15-39', '40-44', '50-54', '55-59', '60-64', 
                  '65-69', '70-74', '75-84', '85-89', '90-94', '95+']

    # Create a new dataframe for the nordpred format
    nordpred_data = pd.DataFrame()

    # Set the row names (age groups)
    nordpred_data['row.names'] = age_groups

    # Extract years from the data
    years = df['Year'].unique()

    # For each year, create a column with the prevalence rates
    for year in years:
        # Create a list to store the prevalence rates for this year
        prevalence_rates = []
        
        # For each age group, get the prevalence rate
        for age in age_groups:
            # Get the value for this age group and year
            value = df[df['Year'] == year][f'{age}_{gender}_Value'].values[0]
            prevalence_rates.append(value)
        
        # Add the year column with the prevalence rates
        nordpred_data[str(year)] = prevalence_rates

    # Format the prevalence rates to 2 decimal places
    for col in nordpred_data.columns:
        if col != 'row.names':
            nordpred_data[col] = nordpred_data[col].apply(lambda x: f"{x:.2f}")
            
    return nordpred_data

def main():
    # Read the processed diabetes data
    df = pd.read_csv('processed_diabetes_data.csv')
    
    # Generate and save male data
    male_data = generate_nordpred_data(df, 'Male')
    male_data.to_csv('nordpred_male.txt', sep='\t', index=False)
    print("\nnordpred_male.txt has been generated successfully.")
    print(f"Shape of the male data: {male_data.shape}")
    print("\nFirst few rows of the male data:")
    print(male_data.head())
    
    # Generate and save female data
    female_data = generate_nordpred_data(df, 'Female')
    female_data.to_csv('nordpred_female.txt', sep='\t', index=False)
    print("\nnordpred_female.txt has been generated successfully.")
    print(f"Shape of the female data: {female_data.shape}")
    print("\nFirst few rows of the female data:")
    print(female_data.head())

if __name__ == "__main__":
    main() 