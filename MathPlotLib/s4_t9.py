import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
print("Loading cleaned dataset...")
df = pd.read_csv("cleaned_merged_ipl_data.csv")
batter_runs = df.groupby('batter')['batsman_runs'].sum().reset_index()
print("\n--- Task 9: Boundary Percentage ---")
# Calculate the total amount of RUNS a player has scored exclusively from 4s and 6s
boundary_runs = df[df['batsman_runs'].isin([4, 6])].groupby('batter')['batsman_runs'].sum().reset_index()
boundary_runs.rename(columns={'batsman_runs': 'runs_from_boundaries'}, inplace=True)

# Merge back with their total runs
boundary_pct_df = pd.merge(batter_runs, boundary_runs, on='batter', how='left').fillna(0)
boundary_pct_df['boundary_percentage'] = ((boundary_pct_df['runs_from_boundaries'] / boundary_pct_df['batsman_runs']) * 100).round(2)

# Filter for batters with at least 500 total runs
top_boundary_pct = boundary_pct_df[boundary_pct_df['batsman_runs'] >= 500].sort_values(by='boundary_percentage', ascending=False).head(10)
print(top_boundary_pct)

sns.set_theme(style="whitegrid")

# Visualizing players with the highest percentage of runs from boundaries
sns.barplot(x='boundary_percentage', y='batter', data=top_boundary_pct, palette='YlOrBr')
plt.title('Top 10 Batters by Boundary Percentage (Min 500 Runs)')
plt.xlabel('Percentage of Runs from Boundaries (%)')
plt.ylabel('Batter')
plt.savefig('task_9_boundary_percentage.png')