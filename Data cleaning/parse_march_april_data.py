#!/usr/bin/env python3
"""
Script to parse monthly park data from Mar 25 and Apr 25 folders
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
    # Read CSV starting from row 4 (index 3) which has the headers
    df = pd.read_csv(file_path, skiprows=3, header=0)
    
    result = {}
    
    # The CSV structure is:
    # Field1: "MAR 2024", Field2: "MAR 2025", Field3: "YTD 2024", Field4: "YTD 2025"
    # Field6: NaN, Field7: Park Name, Field8: MAR 2024 value, Field9: MAR 2025 value
    # So Field7 = Park Name, Field9 = MAR 2025 value (what we want)
    
    for idx, row in df.iterrows():
        # Get park name from Field7 - skip rows where Field7 is NaN (those are header rows)
        park_name = row.get('Field7', None)
        if pd.isna(park_name) or str(park_name).strip() == '':
            continue
            
        park_name = str(park_name).strip()
        
        # Skip if it's "Total" or "Park"
        if park_name.lower() in ['total', 'park']:
            continue
        
        # Skip if park name is purely numeric (likely a total value)
        # Remove commas and check if it's all digits
        park_name_no_commas = park_name.replace(',', '').strip()
        if park_name_no_commas.replace('.', '').replace('-', '').isdigit():
            continue
        
        # Only keep parks with "NP" in the name (National Parks)
        # Exclude NPRES (National Preserves)
        if 'NP' not in park_name or 'NPRES' in park_name:
            continue
        
        # Get MAR 2025 value from Field9 (column index 7)
        mar2025_value = row.get('Field9', None)
        if pd.isna(mar2025_value):
            continue
            
        mar2025_value = remove_commas_from_number(mar2025_value)
        if mar2025_value is not None:
            result[park_name] = mar2025_value
    
    return result

def get_column_name_from_title(title):
    """Map a title from line 2 to the appropriate DataFrame column name"""
    title_lower = title.lower()
    
    # Title mapping - maps title keywords to column names
    # Order matters! More specific patterns should come first
    title_mappings = {
        'nonrecreation overnight stays': 'NonRecreationOvernightStays',
        'non recreation overnight stays': 'NonRecreationOvernightStays',
        'nonrecreation visits': 'NonRecreationVisits',
        'non recreation visits': 'NonRecreationVisits',
        'nonrecreation hours': 'NonRecreationHours',
        'non recreation hours': 'NonRecreationHours',
        'miscellaneous overnight stays': 'MiscellaneousOvernightStays',
        'misc overnight stays': 'MiscellaneousOvernightStays',
        'recreation visits': 'RecreationVisits',
        'recreation hours': 'RecreationHours',
        'concessioner lodging': 'ConcessionerLodging',
        'concessioner camping': 'ConcessionerCamping',
        'tent campers': 'TentCampers',
        'rv campers': 'RVCampers',
        'backcountry campers': 'Backcountry'
    }
    
    for keyword, column_name in title_mappings.items():
        if keyword in title_lower:
            return column_name
    
    return None

def main():
    # Base directory
    base_dir = Path(__file__).parent / "Datasets"
    
    # Month folders
    months = {
        'march 25': {'month': 'March', 'month_num': 3, 'year': 2025},
        'april 25': {'month': 'April', 'month_num': 4, 'year': 2025}
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
            # Read line 2 to get the title
            with open(file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if len(lines) < 2:
                    print(f"  Skipping {file.name} - no title found")
                    continue
                title = lines[1].strip()
            
            # Map title to column name
            column_name = get_column_name_from_title(title)
            
            if column_name is None:
                print(f"  Skipping {file.name} - unknown title: {title}")
                continue
            
            print(f"  Processing {file.name} -> {column_name} (from title: {title})")
            
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
    
    # Sort by Month (March first, then April) and ParkName
    month_order = {'March': 3, 'April': 4}
    df['MonthOrder'] = df['Month'].map(month_order)
    df = df.sort_values(['MonthOrder', 'ParkName'])
    df = df.drop('MonthOrder', axis=1)
    
    # Convert numeric columns to integers (nullable Int64 type to handle NaN)
    numeric_columns = ['Year', 'RecreationVisits', 'NonRecreationVisits', 'RecreationHours', 
                      'NonRecreationHours', 'ConcessionerLodging', 'ConcessionerCamping', 
                      'TentCampers', 'RVCampers', 'Backcountry', 'NonRecreationOvernightStays', 
                      'MiscellaneousOvernightStays']
    for col in numeric_columns:
        if col in df.columns:
            # Convert to nullable integer type (handles NaN properly)
            df[col] = df[col].astype('Int64')
    
    # Save to CSV
    output_file = Path(__file__).parent / 'Mar_Apr_2025_Report.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\n✓ Successfully created {output_file}")
    print(f"  Total records: {len(df)}")
    print(f"  Parks per month: ~{len(df) // 2}")
    print(f"\nFirst few rows:")
    print(df.head(10).to_string())

if __name__ == '__main__':
    main()


