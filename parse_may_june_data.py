#!/usr/bin/env python3
"""
Script to parse monthly park data from May 25 and Jun 25 folders
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

def parse_excel_file(file_path):
    """Parse an Excel file and return park names with their values for the current year (2025)"""
    # Read Excel file, skipping first 8 rows (header is at row 8, index 8)
    # Structure: Row 8 has headers, Row 9+ has data
    # Column index 1 = Park name, Column index 7 = Current year value (MAY 2025 or JUN 2025)
    df = pd.read_excel(file_path, skiprows=8, header=None)
    
    result = {}
    
    for idx, row in df.iterrows():
        # Get park name from column index 1
        park_name = row.iloc[1] if len(row) > 1 else None
        if pd.isna(park_name) or str(park_name).strip() == '':
            continue
            
        park_name = str(park_name).strip()
        
        # Skip if it's "Park" or "Total" or empty
        if park_name.lower() in ['park', 'total', '']:
            continue
        
        # Only keep parks with "NP" in the name (National Parks)
        # Exclude NPRES (National Preserves)
        if 'NP' not in park_name or 'NPRES' in park_name:
            continue
        
        # Get current year value from column index 7 (MAY 2025 or JUN 2025)
        value = row.iloc[7] if len(row) > 7 else None
        if pd.isna(value):
            continue
            
        value = remove_commas_from_number(value)
        if value is not None:
            result[park_name] = value
    
    return result

def get_column_name_from_filename(filename):
    """Extract data type from filename and map to column name"""
    # Filename format: "Current Year Monthly and Annual Summary Report (1979 - Present)-may rec visits.xlsx"
    # Extract the part after the dash and before .xlsx
    filename_lower = filename.lower()
    
    # Remove the prefix and extension
    if '-' in filename_lower:
        data_type = filename_lower.split('-', 1)[1].replace('.xlsx', '').replace('.xls', '').strip()
        
        # Remove month prefix (may or jun)
        data_type = data_type.replace('may ', '').replace('jun ', '').replace('june ', '').strip()
    else:
        return None
    
    # Map to column names
    # Order matters! More specific patterns should come first
    filename_mappings = {
        'nonrec overnight stays': 'NonRecreationOvernightStays',
        'non rec overnight stays': 'NonRecreationOvernightStays',
        'nonrec visits': 'NonRecreationVisits',
        'non rec visits': 'NonRecreationVisits',
        'nonrec hours': 'NonRecreationHours',
        'non rec hours': 'NonRecreationHours',
        'misc overnight stays': 'MiscellaneousOvernightStays',
        'miscellaneous overnight stays': 'MiscellaneousOvernightStays',
        'rec visits': 'RecreationVisits',
        'rec hours': 'RecreationHours',
        'concessioner lodging': 'ConcessionerLodging',
        'concessioner camping': 'ConcessionerCamping',
        'tent campers': 'TentCampers',
        'rv campers': 'RVCampers',
        'backcountry campers': 'Backcountry'
    }
    
    for pattern, column_name in filename_mappings.items():
        if pattern in data_type:
            return column_name
    
    return None

def main():
    # Base directory
    base_dir = Path(__file__).parent / "Datasets"
    
    # Month folders
    months = {
        'may 25': {'month': 'May', 'month_num': 5, 'year': 2025},
        'june 25': {'month': 'June', 'month_num': 6, 'year': 2025}
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
        
        # Parse all Excel files in this folder
        for file in folder_path.glob("*.xlsx"):
            # Extract column name from filename
            column_name = get_column_name_from_filename(file.name)
            
            if column_name is None:
                print(f"  Skipping {file.name} - unknown data type")
                continue
            
            print(f"  Processing {file.name} -> {column_name}")
            
            # Parse the Excel file
            park_values = parse_excel_file(file)
            
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
    
    # Sort by Month (May first, then June) and ParkName
    month_order = {'May': 5, 'June': 6}
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
    output_file = Path(__file__).parent / 'May_Jun_2025_Report.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\n✓ Successfully created {output_file}")
    print(f"  Total records: {len(df)}")
    print(f"  Parks per month: ~{len(df) // 2}")
    print(f"\nFirst few rows:")
    print(df.head(10).to_string())

if __name__ == '__main__':
    main()


