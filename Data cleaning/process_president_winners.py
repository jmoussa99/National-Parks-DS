import pandas as pd

# Read the CSV file
df = pd.read_csv('Datasets/1976-2020-president.csv')

print(f"Original data shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}\n")

# Group by year and state to find the winner (candidate with max votes)
# We'll use idx to get the index of the max candidatevotes for each group
idx = df.groupby(['year', 'state'])['candidatevotes'].idxmax()

# Create a new dataframe with only the winning candidates
winners_df = df.loc[idx].copy()

# Add a 'winner' column with the candidate name
winners_df['winner'] = winners_df['candidate']

# Sort by year and state for better readability
winners_df = winners_df.sort_values(['year', 'state'])

# Reset index
winners_df = winners_df.reset_index(drop=True)

print(f"Processed data shape: {winners_df.shape}")
print(f"\nSample of winners data:")
print(winners_df[['year', 'state', 'candidate', 'candidatevotes', 'totalvotes', 'winner']].head(10))

# Save to a new CSV file
output_file = 'Datasets/president_winners.csv'
winners_df.to_csv(output_file, index=False)
print(f"\nWinners data saved to: {output_file}")

# Display some statistics
print(f"\nStatistics:")
print(f"Total number of elections (year-state combinations): {len(winners_df)}")
print(f"Years covered: {winners_df['year'].min()} - {winners_df['year'].max()}")
print(f"Number of unique states: {winners_df['state'].nunique()}")
print(f"\nWinners by party:")
print(winners_df['party_simplified'].value_counts())

