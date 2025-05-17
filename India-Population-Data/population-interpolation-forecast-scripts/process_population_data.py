import pandas as pd
import numpy as np
import csv

def clean_column_name(col_name):
    """Clean column name by removing BOM and other special characters."""
    return col_name.replace('\ufeff', '')

def process_population_data():
    """
    Process population data for all three years (1991, 2001, 2011) and create age bins as specified.
    Add male and female data as new columns to existing population files.
    """
    # Define the target age groups
    target_age_groups = [
        '0-5', '5-14', '15-39', '40-44', '50-54', '55-59', '60-64', '65-69',
        '70-74', '75-84', '85-89', '90-94', '95+'
    ]
    
    # Define the years to process
    years = [1991, 2001, 2011]
    
    # Read existing population files
    try:
        male_data = pd.read_csv('nordpred_male_population.txt', sep='\t')
        female_data = pd.read_csv('nordpred_female_population.txt', sep='\t')
        print("Successfully loaded existing population files.")
    except FileNotFoundError:
        # If files don't exist, create new dataframes
        male_data = pd.DataFrame({'row.names': target_age_groups})
        female_data = pd.DataFrame({'row.names': target_age_groups})
        print("Created new dataframes for population data.")
    
    # Process each year
    for year in years:
        print(f"\n{'='*50}")
        print(f"Processing {year} data...")
        print(f"{'='*50}")
        
        # Read the year data with a more robust approach
        try:
            # First try to read with pandas
            df_year = pd.read_csv(f'{year}-M-F.csv')
            print(f"Successfully loaded {year}-M-F.csv with {len(df_year)} rows")
        except Exception as e:
            print(f"Error reading {year}-M-F.csv with pandas: {e}")
            print("Attempting to read with csv module...")
            
            # If pandas fails, use csv module to read the file
            rows = []
            with open(f'{year}-M-F.csv', 'r') as f:
                csv_reader = csv.reader(f)
                headers = next(csv_reader)  # Get headers
                headers = [clean_column_name(h) for h in headers]  # Clean headers
                
                # Process each row, handling extra commas
                for row in csv_reader:
                    # Skip 'Age not stated' and 'Total Population' rows
                    if row[0] in ['Age not stated', 'Total Population']:
                        continue
                    # Take only the first three elements if there are more
                    if len(row) > 3:
                        row = row[:3]
                    # Convert empty strings to 0
                    row = [0 if v == '' else v for v in row]
                    rows.append(row)
            
            # Create DataFrame from the processed rows
            df_year = pd.DataFrame(rows, columns=headers)
            print(f"Successfully loaded {year}-M-F.csv with {len(df_year)} rows using csv module")
        
        # Clean column names
        df_year.columns = [clean_column_name(col) for col in df_year.columns]
        
        # Debug: Print column names
        print(f"Column names in {year} data:")
        print(df_year.columns.tolist())
        
        # Debug: Print unique age groups in this year's data
        print(f"\nAge groups in {year} data:")
        print(df_year['Age-Group'].unique())
        
        # Verify column names
        expected_columns = [f'{year}-Male', f'{year}-Female']
        missing_columns = [col for col in expected_columns if col not in df_year.columns]
        if missing_columns:
            print(f"Error: Missing columns in {year} data: {missing_columns}")
            print(f"Available columns: {df_year.columns.tolist()}")
            continue
        
        # Convert numeric columns to float
        df_year[f'{year}-Male'] = pd.to_numeric(df_year[f'{year}-Male'], errors='coerce')
        df_year[f'{year}-Female'] = pd.to_numeric(df_year[f'{year}-Female'], errors='coerce')
        
        # Process each target age group
        for age_group in target_age_groups:
            print(f"\n--- Processing age group: {age_group} ---")
            
            if age_group == '0-5':
                if year == 1991:
                    # For 1991, use 0-4 data directly
                    row_0_4 = df_year[df_year['Age-Group'] == '0-4']
                    if not row_0_4.empty:
                        male_value = int(row_0_4[f'{year}-Male'].values[0])
                        female_value = int(row_0_4[f'{year}-Female'].values[0])
                        print(f"Used 0-4 for {age_group}: Male={male_value}, Female={female_value}")
                    else:
                        print(f"Error: Could not find 0-4 age group in {year} data")
                        continue
                else:
                    # For 2001 and 2011, use half of 0-9 group
                    row_0_9 = df_year[df_year['Age-Group'] == '0-9']
                    if not row_0_9.empty:
                        male_value = int(row_0_9[f'{year}-Male'].values[0] * 0.5)
                        female_value = int(row_0_9[f'{year}-Female'].values[0] * 0.5)
                        print(f"Estimated 0-5 from 0-9 for {age_group}:")
                        print(f"  Original 0-9: Male={int(row_0_9[f'{year}-Male'].values[0])}, Female={int(row_0_9[f'{year}-Female'].values[0])}")
                        print(f"  Estimated 0-5 (50%): Male={male_value}, Female={female_value}")
                    else:
                        print(f"Error: Could not find 0-9 age group in {year} data")
                        continue
                
                # Verify values are positive
                if male_value <= 0 or female_value <= 0:
                    print(f"Warning: Invalid values for {age_group}: Male={male_value}, Female={female_value}")
                    continue
                
                male_data.loc[male_data['row.names'] == age_group, str(year)] = male_value
                female_data.loc[female_data['row.names'] == age_group, str(year)] = female_value
            
            elif age_group == '5-14':
                if year == 1991:
                    # For 1991, combine half of 5-9 and full 10-14
                    row_5_9 = df_year[df_year['Age-Group'] == '5-9']
                    row_10_14 = df_year[df_year['Age-Group'] == '10-14']
                    if not row_5_9.empty and not row_10_14.empty:
                        male_5_9 = int(row_5_9[f'{year}-Male'].values[0])
                        female_5_9 = int(row_5_9[f'{year}-Female'].values[0])
                        male_10_14 = int(row_10_14[f'{year}-Male'].values[0])
                        female_10_14 = int(row_10_14[f'{year}-Female'].values[0])
                        
                        male_value = int(male_5_9 * 0.5 + male_10_14)
                        female_value = int(female_5_9 * 0.5 + female_10_14)
                        
                        print(f"Combined half of 5-9 and full 10-14 for {age_group}:")
                        print(f"  5-9: Male={male_5_9}, Female={female_5_9}")
                        print(f"  10-14: Male={male_10_14}, Female={female_10_14}")
                        print(f"  Half of 5-9: Male={int(male_5_9 * 0.5)}, Female={int(female_5_9 * 0.5)}")
                        print(f"  Total: Male={male_value}, Female={female_value}")
                    else:
                        print(f"Error: Could not find 5-9 or 10-14 age group in {year} data")
                        print(f"5-9 found: {not row_5_9.empty}, 10-14 found: {not row_10_14.empty}")
                        continue
                elif year == 2001:
                    # For 2001, use 10-14 data (labeled as 14-Oct in the CSV)
                    row_10_14 = df_year[df_year['Age-Group'] == '14-Oct']
                    if not row_10_14.empty:
                        male_value = int(row_10_14[f'{year}-Male'].values[0])
                        female_value = int(row_10_14[f'{year}-Female'].values[0])
                        print(f"Used 14-Oct for {age_group}: Male={male_value}, Female={female_value}")
                    else:
                        print(f"Error: Could not find 14-Oct age group in {year} data")
                        continue
                else:
                    # For 2011, use 10-14 data
                    row_10_14 = df_year[df_year['Age-Group'] == '10-14']
                    if not row_10_14.empty:
                        male_value = int(row_10_14[f'{year}-Male'].values[0])
                        female_value = int(row_10_14[f'{year}-Female'].values[0])
                        print(f"Used 10-14 for {age_group}: Male={male_value}, Female={female_value}")
                    else:
                        print(f"Error: Could not find 10-14 age group in {year} data")
                        continue
                
                # Verify values are positive
                if male_value <= 0 or female_value <= 0:
                    print(f"Warning: Invalid values for {age_group}: Male={male_value}, Female={female_value}")
                    continue
                
                male_data.loc[male_data['row.names'] == age_group, str(year)] = male_value
                female_data.loc[female_data['row.names'] == age_group, str(year)] = female_value
            
            elif age_group == '15-39':
                # Sum 15-19, 20-24, 25-29, 30-34, 35-39
                age_groups = ['15-19', '20-24', '25-29', '30-34', '35-39']
                male_sum = 0
                female_sum = 0
                
                print(f"Summing age groups for {age_group}:")
                for ag in age_groups:
                    row = df_year[df_year['Age-Group'] == ag]
                    if not row.empty:
                        male_value = int(row[f'{year}-Male'].values[0])
                        female_value = int(row[f'{year}-Female'].values[0])
                        male_sum += male_value
                        female_sum += female_value
                        print(f"  {ag}: Male={male_value}, Female={female_value}")
                    else:
                        print(f"  Warning: Could not find {ag} age group in {year} data")
                
                print(f"  Total for {age_group}: Male={male_sum}, Female={female_sum}")
                
                # Verify values are positive
                if male_sum <= 0 or female_sum <= 0:
                    print(f"Warning: Invalid values for {age_group}: Male={male_sum}, Female={female_sum}")
                    continue
                
                male_data.loc[male_data['row.names'] == age_group, str(year)] = male_sum
                female_data.loc[female_data['row.names'] == age_group, str(year)] = female_sum
            
            elif age_group == '75-84':
                # For all years, combine 75-79 and 40% of 80+
                row_75_79 = df_year[df_year['Age-Group'] == '75-79']
                
                # Check for different possible age group names for 80+
                row_80_plus = None
                age_name_found = None
                for age_name in ['80+', '80-84', '80 and above']:
                    row = df_year[df_year['Age-Group'] == age_name]
                    if not row.empty:
                        row_80_plus = row
                        age_name_found = age_name
                        break
                
                if not row_75_79.empty and row_80_plus is not None:
                    male_75_79 = int(row_75_79[f'{year}-Male'].values[0])
                    female_75_79 = int(row_75_79[f'{year}-Female'].values[0])
                    male_80_plus = int(row_80_plus[f'{year}-Male'].values[0])
                    female_80_plus = int(row_80_plus[f'{year}-Female'].values[0])
                    
                    male_sum = int(male_75_79 + (male_80_plus * 0.4))
                    female_sum = int(female_75_79 + (female_80_plus * 0.4))
                    
                    print(f"Combined 75-79 and 40% of {age_name_found} for {age_group}:")
                    print(f"  75-79: Male={male_75_79}, Female={female_75_79}")
                    print(f"  {age_name_found}: Male={male_80_plus}, Female={female_80_plus}")
                    print(f"  40% of {age_name_found}: Male={int(male_80_plus * 0.4)}, Female={int(female_80_plus * 0.4)}")
                    print(f"  Total: Male={male_sum}, Female={female_sum}")
                    
                    # Verify values are positive
                    if male_sum <= 0 or female_sum <= 0:
                        print(f"Warning: Invalid values for {age_group}: Male={male_sum}, Female={female_sum}")
                        continue
                    
                    male_data.loc[male_data['row.names'] == age_group, str(year)] = male_sum
                    female_data.loc[female_data['row.names'] == age_group, str(year)] = female_sum
                else:
                    print(f"Warning: Could not find 75-79 or 80+ data for {year}")
                    print(f"75-79 found: {not row_75_79.empty}")
                    print(f"80+ found: {row_80_plus is not None}")
            
            elif age_group in ['85-89', '90-94', '95+']:
                # For all years, calculate from 80+
                row_80_plus = None
                age_name_found = None
                for age_name in ['80+', '80-84', '80 and above']:
                    row = df_year[df_year['Age-Group'] == age_name]
                    if not row.empty:
                        row_80_plus = row
                        age_name_found = age_name
                        break
                
                if row_80_plus is not None:
                    male_80_plus = int(row_80_plus[f'{year}-Male'].values[0])
                    female_80_plus = int(row_80_plus[f'{year}-Female'].values[0])
                    
                    if age_group == '85-89':
                        percentage = 0.3
                    elif age_group == '90-94':
                        percentage = 0.2
                    else:  # 95+
                        percentage = 0.1
                    
                    male_value = int(male_80_plus * percentage)
                    female_value = int(female_80_plus * percentage)
                    
                    print(f"Used {int(percentage * 100)}% of {age_name_found} for {age_group}:")
                    print(f"  {age_name_found}: Male={male_80_plus}, Female={female_80_plus}")
                    print(f"  {int(percentage * 100)}%: Male={male_value}, Female={female_value}")
                    
                    # Verify values are positive
                    if male_value <= 0 or female_value <= 0:
                        print(f"Warning: Invalid values for {age_group}: Male={male_value}, Female={female_value}")
                        continue
                    
                    male_data.loc[male_data['row.names'] == age_group, str(year)] = male_value
                    female_data.loc[female_data['row.names'] == age_group, str(year)] = female_value
                else:
                    print(f"Warning: Could not find 80+ data for {year}")
            
            else:
                # Direct match for other age groups
                row = df_year[df_year['Age-Group'] == age_group]
                
                if not row.empty:
                    male_value = int(row[f'{year}-Male'].values[0])
                    female_value = int(row[f'{year}-Female'].values[0])
                    
                    print(f"Direct match for {age_group}: Male={male_value}, Female={female_value}")
                    
                    # Verify values are positive
                    if male_value <= 0 or female_value <= 0:
                        print(f"Warning: Invalid values for {age_group}: Male={male_value}, Female={female_value}")
                        continue
                    
                    male_data.loc[male_data['row.names'] == age_group, str(year)] = male_value
                    female_data.loc[female_data['row.names'] == age_group, str(year)] = female_value
                else:
                    print(f"Warning: Could not find {age_group} age group in {year} data")
    
    # Verify data completeness
    print("\nVerifying data completeness...")
    for year in years:
        year_str = str(year)
        male_missing = male_data[year_str].isna().sum()
        female_missing = female_data[year_str].isna().sum()
        
        if male_missing > 0 or female_missing > 0:
            print(f"Warning: Missing data for {year}:")
            print(f"  Male: {male_missing} missing values")
            print(f"  Female: {female_missing} missing values")
            
            # Print which age groups are missing
            if male_missing > 0:
                missing_male = male_data[male_data[year_str].isna()]['row.names'].tolist()
                print(f"  Missing male age groups: {missing_male}")
            
            if female_missing > 0:
                missing_female = female_data[female_data[year_str].isna()]['row.names'].tolist()
                print(f"  Missing female age groups: {missing_female}")
        else:
            print(f"All data complete for {year}")
    
    # Save the data to separate txt files
    male_data.to_csv('nordpred_male_population.txt', sep='\t', index=False)
    female_data.to_csv('nordpred_female_population.txt', sep='\t', index=False)
    print("\nMale data saved to nordpred_male_population.txt")
    print("Female data saved to nordpred_female_population.txt")
    
    # Display the processed data
    print("\nMale data:")
    print(male_data)
    print("\nFemale data:")
    print(female_data)

if __name__ == "__main__":
    process_population_data() 