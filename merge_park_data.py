"""
Script to merge yearly_park_data.csv with historic_park_data.csv
- Sums columns from "Recreation Visits" to "Misc. Overnight Stays" in yearly_park_data.csv
- Creates a Total column
- Concatenates with historic_park_data.csv
- Orders by ParkName and Year
"""

import pandas as pd
import os

def merge_park_data(yearly_file='Datasets/yearly_park_data.csv',
                   historic_file='Datasets/historic_park_data.csv',
                   output_file='Datasets/historic_park_data.csv'):
    """
    Merge yearly park data with historic park data
    
    Args:
        yearly_file: Path to yearly_park_data.csv
        historic_file: Path to historic_park_data.csv
        output_file: Path to save the merged CSV file
    """
    
    print(f"Reading yearly park data from: {yearly_file}")
    df_yearly = pd.read_csv(yearly_file, low_memory=False)
    
    print(f"Reading historic park data from: {historic_file}")
    df_historic = pd.read_csv(historic_file, low_memory=False)
    
    print(f"\nYearly data shape: {df_yearly.shape}")
    print(f"Historic data shape: {df_historic.shape}")
    
    # Identify columns to sum (from "Recreation Visits" to "Misc. Overnight Stays")
    print("\n[1] Identifying columns to sum...")
    columns_to_sum = []
    start_col = "Recreation Visits"
    end_col = "Misc. Overnight Stays"
    
    # Find the index of start and end columns
    col_list = df_yearly.columns.tolist()
    start_idx = col_list.index(start_col) if start_col in col_list else None
    end_idx = col_list.index(end_col) if end_col in col_list else None
    
    if start_idx is not None and end_idx is not None:
        columns_to_sum = col_list[start_idx:end_idx + 1]
        print(f"    Columns to sum: {columns_to_sum}")
    else:
        print(f"    ERROR: Could not find start or end column")
        print(f"    Available columns: {col_list}")
        return None
    
    # Convert columns to numeric (removing commas)
    print("\n[2] Converting columns to numeric...")
    for col in columns_to_sum:
        if df_yearly[col].dtype == 'object':
            # Remove commas and convert to numeric
            df_yearly[col] = df_yearly[col].astype(str).str.replace(',', '')
            df_yearly[col] = pd.to_numeric(df_yearly[col], errors='coerce').fillna(0)
    
    # Sum the columns for each row
    print("\n[3] Calculating totals...")
    df_yearly['Total'] = df_yearly[columns_to_sum].sum(axis=1)
    
    # Format Total as string with commas
    df_yearly['Total'] = df_yearly['Total'].apply(lambda x: f"{int(x):,}")
    
    # Rename columns to match historic_park_data.csv format
    print("\n[4] Renaming columns to match historic format...")
    column_mapping = {
        'Park': 'ParkName',
        'Unit Code': 'UnitCode',
        'Park Type': 'ParkType',
        'Region': 'Region',
        'State': 'State',
        'Year': 'Year',
        'Total': 'Total'
    }
    
    df_yearly_renamed = df_yearly[list(column_mapping.keys())].rename(columns=column_mapping)
    
    # Ensure historic data has the same column order
    df_historic = df_historic[['ParkName', 'UnitCode', 'ParkType', 'Region', 'State', 'Year', 'Total']]
    
    # Concatenate the dataframes
    print("\n[5] Concatenating dataframes...")
    df_merged = pd.concat([df_historic, df_yearly_renamed], ignore_index=True)
    print(f"    Merged shape: {df_merged.shape}")
    
    # Sort by ParkName and Year
    print("\n[6] Sorting by ParkName and Year...")
    df_merged = df_merged.sort_values(by=['ParkName', 'Year'], ascending=[True, True])
    
    # Remove duplicates if any (same park, year combination)
    print("\n[7] Removing duplicates...")
    initial_rows = len(df_merged)
    df_merged = df_merged.drop_duplicates(subset=['ParkName', 'Year'], keep='last')
    duplicates_removed = initial_rows - len(df_merged)
    if duplicates_removed > 0:
        print(f"    Removed {duplicates_removed} duplicate rows")
    else:
        print("    No duplicates found")
    
    # Save the merged data
    print(f"\n[8] Saving merged data to: {output_file}")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df_merged.to_csv(output_file, index=False)
    
    print(f"\n✓ Merge complete!")
    print(f"  Final shape: {df_merged.shape}")
    print(f"  Number of unique parks: {df_merged['ParkName'].nunique()}")
    print(f"  Year range: {df_merged['Year'].min()} - {df_merged['Year'].max()}")
    print(f"  Data is sorted by ParkName (alphabetically) and Year (chronologically)")
    
    return df_merged

if __name__ == "__main__":
    # Run the merge process
    merged_df = merge_park_data()
    
    # Display first few rows
    print("\n" + "="*80)
    print("Sample of merged data (first 20 rows):")
    print("="*80)
    print(merged_df.head(20))
    print("\n" + "="*80)
    print("Sample of merged data (last 20 rows):")
    print("="*80)
    print(merged_df.tail(20))
    print("\n" + "="*80)

