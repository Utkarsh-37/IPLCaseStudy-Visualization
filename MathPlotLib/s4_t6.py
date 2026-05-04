import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
print("Loading cleaned dataset...")
df = pd.read_csv("cleaned_merged_ipl_data.csv")
print("\n--- Task 6: Most Consistent Batters ---")
# Consistency measured by average runs per match (total runs / total matches played)
matches_played = df.groupby('batter')['match_id'].nunique().reset_index()
matches_played.rename(columns={'match_id': 'matches_played'}, inplace=True)

# Using batter_runs calculated previously in Task 4, or recalculating:
batter_runs = df.groupby('batter')['batsman_runs'].sum().reset_index()

consistency_df = pd.merge(batter_runs, matches_played, on='batter')
consistency_df['average_runs'] = (consistency_df['batsman_runs'] / consistency_df['matches_played']).round(2)

# Filter for a minimum of 30 matches played to ensure a reliable sample size
consistent_batters = consistency_df[consistency_df['matches_played'] >= 30].sort_values(by='average_runs', ascending=False).head(10)
print(consistent_batters)

sns.set_theme(style="whitegrid")
# Visualizing batting consistency (Average runs per match)
sns.barplot(x='average_runs', y='batter', data=consistent_batters, palette='flare')
plt.title('Top 10 Most Consistent Batters (Min 30 Matches)')
plt.xlabel('Average Runs per Match')
plt.ylabel('Batter')
plt.savefig('task_6_consistency.png')