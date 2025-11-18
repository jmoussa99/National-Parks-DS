"""
Script to organize historic_park_data.csv by ParkName and Year
Sorts data alphabetically by park name, then chronologically by year
"""

import pandas as pd
import os

def organize_historic_park_data(input_file='Datasets/historic_park_data.csv',
                                output_file='Datasets/historic_park_data.csv'):
    """
    Organize the historic park data by ParkName and Year
    
    Args:
        input_file: Path to the original CSV file
        output_file: Path to save the organized CSV file (default: overwrites original)
    """
    
    print(f"Reading data from: {input_file}")
    
    # Read the CSV
    df = pd.read_csv(input_file, low_memory=False)
    
    print(f"Original shape: {df.shape}")
    print(f"Number of unique parks: {df['ParkName'].nunique()}")
    print(f"Year range: {df['Year'].min()} - {df['Year'].max()}")
    
    # Sort by ParkName (alphabetically) and then by Year (chronologically)
    print("\n[1] Sorting data by ParkName and Year...")
    df_sorted = df.sort_values(by=['ParkName', 'Year'], ascending=[True, True])
    
    print(f"    Sorted {len(df_sorted)} rows")
    
    # Display summary of sorting
    print("\n[2] Verifying sort order...")
    print(f"    First park: {df_sorted.iloc[0]['ParkName']} ({df_sorted.iloc[0]['Year']})")
    print(f"    Last park: {df_sorted.iloc[-1]['ParkName']} ({df_sorted.iloc[-1]['Year']})")
    
    # Check if data is properly sorted
    parks = df_sorted['ParkName'].unique()
    print(f"\n[3] Sample of park order (first 10):")
    for i, park in enumerate(parks[:10], 1):
        years = df_sorted[df_sorted['ParkName'] == park]['Year'].tolist()
        print(f"    {i}. {park}: {years[0]}-{years[-1]} ({len(years)} years)")
    
    # Save organized data
    print(f"\n[4] Saving organized data to: {output_file}")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df_sorted.to_csv(output_file, index=False)
    
    print(f"\n✓ Organization complete!")
    print(f"  Final shape: {df_sorted.shape}")
    print(f"  Data is now sorted by ParkName (alphabetically) and Year (chronologically)")
    
    return df_sorted

if __name__ == "__main__":
    # Run the organization process
    organized_df = organize_historic_park_data()
    
    # Display first few rows
    print("\n" + "="*80)
    print("Sample of organized data (first 20 rows):")
    print("="*80)
    print(organized_df.head(20))
    print("\n" + "="*80)

