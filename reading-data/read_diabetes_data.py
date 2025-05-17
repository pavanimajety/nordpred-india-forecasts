import pandas as pd
import numpy as np
import os
import argparse
import sys

def process_file(input_csv, output_base):
    # Try reading as multi-header, fallback to single header
    try:
        df = pd.read_csv(input_csv, header=[0, 1])
        multi_header = True
    except Exception:
        df = pd.read_csv(input_csv)
        multi_header = False

    # Detect year column
    if multi_header:
        # Try to find a column with 'Prevalence Rate' or use the first column
        if ('Type 1', 'Prevalence Rate') in df.columns:
            years = df[('Type 1', 'Prevalence Rate')].astype(str).tolist()
        else:
            # Use the first column
            years = df[df.columns[0]].astype(str).tolist()
    else:
        # Use the first column
        years = df[df.columns[0]].astype(str).tolist()

    # Age groups in nordpred order
    age_groups = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34',
                  '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69',
                  '70-74', '75-79', '80-84', '85+']
    age_map = {
        '0-4': '<5 years',
        '5-9': '5-9 Years',
        '10-14': '5-14 Years',
        '15-19': '15-19 years',
        '20-24': '20-24 Years',
        '25-29': '25-29 Years',
        '30-34': '30-34 Years',
        '35-39': '35-39 Years',
        '40-44': '40-44 years',
        '45-49': '45-49 years',
        '50-54': '50-54 Years',
        '55-59': '55-59 Years',
        '60-64': '60-64 Years',
        '65-69': '65-69 Years',
        '70-74': '70-74 Years',
        '75-79': '75-84 Years',
        '80-84': '75-84 Years',
        '85+': '85+ years'
    }
    
    # Prepare output data
    data = {'male': [], 'female': []}
    columns = list(df.columns)
    for age in age_groups:
        age_col = age_map[age]
        # Find male column
        male_col = None
        female_col = None
        if multi_header:
            for c in columns:
                if c[0].lower() == age_col.lower() and c[1].strip().lower().startswith('male'):
                    male_col = c
                    break
            found_male = False
            for c in columns:
                if c == male_col:
                    found_male = True
                elif found_male and c[1].strip().lower().startswith('female'):
                    female_col = c
                    break
            if not male_col:
                for c in columns:
                    if c[0].lower() == age_col.lower() and 'male' in c[1].lower():
                        male_col = c
                        break
            if not female_col:
                for c in columns:
                    if c[0].lower() == age_col.lower() and 'female' in c[1].lower():
                        female_col = c
                        break
        else:
            # Single header: find columns by name
            for c in columns:
                if age_col.lower() in c.lower() and 'male' in c.lower():
                    male_col = c
                if age_col.lower() in c.lower() and 'female' in c.lower():
                    female_col = c
        # Extract values, handling confidence intervals if present
        def extract_value(cell):
            if pd.isnull(cell):
                return ''
            return str(cell).split()[0]
        male_values = [extract_value(v) for v in df[male_col]] if male_col else [''] * len(df)
        female_values = [extract_value(v) for v in df[female_col]] if female_col else [''] * len(df)
        data['male'].append([age] + male_values)
        data['female'].append([age] + female_values)
    # Write output files
    header = [''] + years
    for gender in ['male', 'female']:
        out_file = f"{output_base}_{gender}.txt"
        with open(out_file, 'w') as f:
            f.write('\t'.join(header) + '\n')
            for row in data[gender]:
                f.write('\t'.join(map(str, row)) + '\n')
        print(f"Wrote {out_file}")

def main():
    parser = argparse.ArgumentParser(description='Process diabetes data and generate nordpred-style files')
    parser.add_argument('input_csv', help='Input CSV file')
    parser.add_argument('--output-base', help='Base name for output files (without _male.txt/_female.txt)', required=False)
    args = parser.parse_args()
    output_base = args.output_base
    if not output_base:
        output_base = input('Enter base name for output files (e.g., processed_diabetes): ').strip()
        if not output_base:
            print('No output base name provided. Exiting.')
            sys.exit(1)
    process_file(args.input_csv, output_base)

if __name__ == '__main__':
    main() 