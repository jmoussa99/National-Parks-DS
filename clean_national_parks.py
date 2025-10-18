"""
Script to clean the national_parks.csv dataset
Handles: commas in numbers, empty columns, whitespace, and data type conversions
"""

import pandas as pd
import os

def clean_national_parks_data(input_file='Datasets/national_parks.csv', 
                              output_file='Datasets/national_parks_cleaned.csv'):
    """
    Clean the national parks dataset
    
    Args:
        input_file: Path to the original CSV file
        output_file: Path to save the cleaned CSV file
    """
    
    print(f"Reading data from: {input_file}")
    
    # Read the CSV
    df = pd.read_csv(input_file, low_memory=False)
    
    print(f"Original shape: {df.shape}")
    print(f"Original columns: {len(df.columns)}")
    
    # 1. Remove empty/unnamed columns
    print("\n[1] Removing empty columns...")
    original_cols = len(df.columns)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.dropna(axis=1, how='all')
    removed_cols = original_cols - len(df.columns)
    print(f"    Removed {removed_cols} empty columns")
    
    # 2. Strip whitespace from all string columns
    print("\n[2] Stripping whitespace from text columns...")
    string_columns = df.select_dtypes(include=['object']).columns
    for col in string_columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.strip()
    
    # 3. Convert numeric columns with commas to proper numeric types
    print("\n[3] Converting numeric columns (removing commas)...")
    numeric_cols = ['RecreationVisits', 'NonRecreationVisits', 'RecreationHours', 
                    'NonRecreationHours', 'ConcessionerLodging', 'ConcessionerCamping',
                    'TentCampers', 'RVCampers', 'Backcountry', 
                    'NonRecreationOvernightStays', 'MiscellaneousOvernightStays',
                    'MiscellaneousOvernightStaysTotal']
    
    for col in numeric_cols:
        if col in df.columns:
            # Remove commas and convert to numeric
            df[col] = df[col].astype(str).str.replace(',', '')
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
            print(f"    Converted {col}")
    
    # 4. Handle duplicate/redundant columns
    print("\n[4] Checking for duplicate columns...")
    if 'MiscellaneousOvernightStaysTotal' in df.columns:
        if 'MiscellaneousOvernightStays' in df.columns:
            # Check if they're identical
            if df['MiscellaneousOvernightStaysTotal'].equals(df['MiscellaneousOvernightStays']):
                df = df.drop('MiscellaneousOvernightStaysTotal', axis=1)
                print("    Removed duplicate 'MiscellaneousOvernightStaysTotal' column")
            else:
                print("    Kept both columns (they contain different data)")
    
    # 5. Remove columns with only zero values
    print("\n[5] Removing columns with only zero values...")
    zero_cols = []
    for col in df.columns:
        # Only check numeric columns
        if pd.api.types.is_numeric_dtype(df[col]):
            if (df[col] == 0).all() or df[col].sum() == 0:
                zero_cols.append(col)
    
    if zero_cols:
        df = df.drop(columns=zero_cols)
        print(f"    Removed {len(zero_cols)} columns with only zeros:")
        for col in zero_cols:
            print(f"      - {col}")
    else:
        print("    No columns with only zeros found")
    
    # 5b. Remove specific unwanted columns
    print("\n[5b] Removing specific unwanted columns...")
    cols_to_remove = ['ConcessionerLodging', 'ConcessionerCamping', 
                      'NonRecreationOvernightStays', 'MiscellaneousOvernightStays',
                      'MiscellaneousOvernightStaysTotal']
    
    cols_removed = []
    for col in cols_to_remove:
        if col in df.columns:
            cols_removed.append(col)
    
    if cols_removed:
        df = df.drop(columns=cols_removed)
        print(f"    Removed {len(cols_removed)} columns:")
        for col in cols_removed:
            print(f"      - {col}")
    else:
        print("    No unwanted columns found")
    
    # 6. Basic data quality checks
    print("\n[6] Data quality summary:")
    print(f"    Total rows: {len(df):,}")
    print(f"    Date range: {df['Year'].min()} - {df['Year'].max()}")
    print(f"    Number of parks: {df['ParkName'].nunique()}")
    print(f"    Duplicate rows: {df.duplicated().sum()}")
    print(f"    Missing values per column:")
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(missing[missing > 0])
    else:
        print("    No missing values!")
    
    # 7. Save cleaned data
    print(f"\n[7] Saving cleaned data to: {output_file}")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)
    
    print(f"\n✓ Cleaning complete!")
    print(f"  Final shape: {df.shape}")
    print(f"  Final columns: {list(df.columns)}")
    
    return df

if __name__ == "__main__":
    # Run the cleaning process
    cleaned_df = clean_national_parks_data()
    
    # Display first few rows
    print("\n" + "="*80)
    print("Sample of cleaned data:")
    print("="*80)
    print(cleaned_df.head())
    print("\n" + "="*80)
    print("Data types:")
    print("="*80)
    print(cleaned_df.dtypes)

