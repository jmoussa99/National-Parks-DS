#!/usr/bin/env python3
"""
Script to parse monthly park data from Jan 25 and Feb 25 folders
and output a CSV in the same format as Jul_Aug 2025 Report.xlsx
"""

import pandas as pd
import os
from pathlib import Path

def remove_commas_from_number(value):
    """Remove commas from number strings and convert to numeric"""
    if pd.isna(value):
        return None
    if isinstance(value, str):
        # Remove commas and convert to number
        value = value.replace(',', '').strip()
        if value == '' or value == '0':
            return 0
        try:
            return float(value)
        except:
            return None
    return value

def parse_csv_file(file_path):
    """Parse a CSV file and return park names with their values for the current year (2025)"""
    df = pd.read_csv(file_path)
    
    # The first column is Park name, and we need to find the 2025 column
    park_col = df.columns[0]
    
    # Find the column that contains 2025 data (usually second occurrence)
    # Looking at the files, the structure is: Park, empty cols, OLD_YEAR, NEW_YEAR (2025)
    # The 2025 value is typically in column 6 (index 6)
    value_col_idx = 6  # This should be the 2025 monthly value
    
    result = {}
    for idx, row in df.iterrows():
        park_name = row[park_col]
        if pd.notna(park_name) and park_name.strip() != '' and park_name != 'Park':
            value = remove_commas_from_number(row.iloc[value_col_idx]) if len(row) > value_col_idx else 0
            result[park_name] = value
    
    return result

def main():
    # Base directory
    base_dir = Path("/Users/jamalmoussa/Documents/DS/National Parks/Datasets")
    
    # Month folders
    months = {
        'jan 25': {'month': 'January', 'month_num': 1, 'year': 2025},
        'feb 25': {'month': 'February', 'month_num': 2, 'year': 2025}
    }
    
    # File mappings - maps CSV filename patterns to DataFrame column names
    # Order matters! More specific patterns should come first
    file_mappings = {
        'non recreation visits': 'NonRecreationVisits',
        'non recreation hours': 'NonRecreationHours',
        'non recreation overnight stays': 'NonRecreationOvernightStays',
        'recreation visits': 'RecreationVisits',
        'recreation hours': 'RecreationHours',
        'concessioner lodging': 'ConcessionerLodging',
        'concessioner camping': 'ConcessionerCamping',
        'tent campers': 'TentCampers',
        'rv campers': 'RVCampers',
        'backcountry campers': 'Backcountry',
        'miscellaneous overnight stays': 'MiscellaneousOvernightStays'
    }
    
    # Collect all data
    all_data = []
    
    for folder, month_info in months.items():
        folder_path = base_dir / folder
        
        if not folder_path.exists():
            print(f"Warning: Folder {folder_path} does not exist")
            continue
        
        print(f"Processing {folder}...")
        
        # Initialize data dictionary for parks
        month_data = {}
        
        # Parse all CSV files in this folder
        for file in folder_path.glob("*.csv"):
            file_name = file.stem.lower()
            
            # Find matching column name
            column_name = None
            for pattern, col in file_mappings.items():
                if pattern in file_name:
                    column_name = col
                    break
            
            if column_name is None:
                print(f"  Skipping {file.name} - no matching column")
                continue
            
            print(f"  Processing {file.name} -> {column_name}")
            
            # Parse the file
            park_values = parse_csv_file(file)
            
            # Add values to month_data
            for park, value in park_values.items():
                if park not in month_data:
                    # Initialize park entry
                    month_data[park] = {
                        'ParkName': park,
                        'Year': month_info['year'],
                        'Month': month_info['month']
                    }
                month_data[park][column_name] = value
        
        # Convert to list of dictionaries
        for park, data in month_data.items():
            all_data.append(data)
    
    # Create DataFrame
    df = pd.DataFrame(all_data)
    
    # Ensure all expected columns exist
    expected_columns = [
        'ParkName', 'UnitCode', 'ParkType', 'Region', 'State', 
        'Year', 'Month', 'RecreationVisits', 'NonRecreationVisits',
        'RecreationHours', 'NonRecreationHours', 'ConcessionerLodging',
        'ConcessionerCamping', 'TentCampers', 'RVCampers', 'Backcountry',
        'NonRecreationOvernightStays', 'MiscellaneousOvernightStays'
    ]
    
    for col in expected_columns:
        if col not in df.columns:
            df[col] = None
    
    # Reorder columns to match expected format
    df = df[expected_columns]
    
    # Sort by Month (January first, then February) and ParkName
    month_order = {'January': 1, 'February': 2}
    df['MonthOrder'] = df['Month'].map(month_order)
    df = df.sort_values(['MonthOrder', 'ParkName'])
    df = df.drop('MonthOrder', axis=1)
    
    # Save to CSV
    output_file = base_dir.parent / 'Jan_Feb_2025_Report.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\n✓ Successfully created {output_file}")
    print(f"  Total records: {len(df)}")
    print(f"  Parks per month: ~{len(df) // 2}")
    print(f"\nFirst few rows:")
    print(df.head(10).to_string())

if __name__ == '__main__':
    main()

