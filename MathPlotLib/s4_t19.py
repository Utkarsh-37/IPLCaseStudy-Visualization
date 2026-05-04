import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
print("Loading cleaned dataset...")
df = pd.read_csv("cleaned_merged_ipl_data.csv")
matches_df = df.drop_duplicates(subset=['match_id']).rename(columns={'match_id': 'id'})
print("\n--- Task 19: Season-wise Run Trends ---")
season_runs = df.groupby('season')['total_runs'].sum().reset_index()

# Get unique matches per season
season_matches = df.drop_duplicates(subset=['match_id'])['season'].value_counts().reset_index()
season_matches.columns = ['season', 'total_matches']

season_analysis = pd.merge(season_runs, season_matches, on='season')
season_analysis['avg_runs_per_match'] = (season_analysis['total_runs'] / season_analysis['total_matches']).round(2)
season_analysis['season'] = season_analysis['season'].astype(str)

print("Historical Run Scoring Trends by Season:")
print(season_analysis.sort_values('season'))

sns.set_theme(style="whitegrid")

# Tracking how IPL scoring has changed over the years
plt.figure(figsize=(10, 6))
sns.lineplot(x='season', y='avg_runs_per_match', data=season_analysis.sort_values('season'), marker='o', color='red')
plt.title('IPL Scoring Trends: Average Runs per Match by Season')
plt.xlabel('Season')
plt.ylabel('Average Runs')
plt.xticks(rotation=45)
plt.savefig('task_19_season_trends.png')