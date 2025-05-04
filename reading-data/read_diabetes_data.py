import pandas as pd
import numpy as np

# Read the CSV file, skipping the second row (Male/Female labels)
df = pd.read_csv('DMForecastsNew-IndiaType1.csv', skiprows=[1])

# Function to split the values into value, lower bound, and upper bound
def split_values(value):
    try:
        # Split the string and convert to float
        # Format is: value UB LB
        value, ub, lb = map(float, str(value).split())
        return pd.Series([value, lb, ub])  # Return in order: value, LB, UB
    except:
        return pd.Series([np.nan, np.nan, np.nan])

# Process each age-gender column
processed_data = pd.DataFrame()
processed_data['Year'] = df['Prevalence-Rate']

# Get unique age groups
age_groups = ['0-5', '5-14', '15-39', '40-44', '45-49', '50-54', '55-59', 
              '60-64', '65-69', '70-74', '75-84', '85-89', '90-94', '95+']

for age in age_groups:
    male_col = f"{age}-Male"
    female_col = f"{age}-Female"
    
    if male_col in df.columns and female_col in df.columns:
        # Process male data
        male_values = df[male_col].apply(split_values)
        processed_data[f'{age}_Male_Value'] = male_values[0]  # Value
        processed_data[f'{age}_Male_LB'] = male_values[1]     # Lower bound
        processed_data[f'{age}_Male_UB'] = male_values[2]     # Upper bound
        
        # Process female data
        female_values = df[female_col].apply(split_values)
        processed_data[f'{age}_Female_Value'] = female_values[0]  # Value
        processed_data[f'{age}_Female_LB'] = female_values[1]     # Lower bound
        processed_data[f'{age}_Female_UB'] = female_values[2]     # Upper bound

# Save processed data
processed_data.to_csv('processed_diabetes_data.csv', index=False)

print("\nProcessed data has been saved to 'processed_diabetes_data.csv'")
print("\nProcessed data shape:", processed_data.shape)
print("\nProcessed columns:", processed_data.columns.tolist())

# Display a sample of the processed data
print("\nSample of processed data (first 5 rows):")
print(processed_data.head()) 