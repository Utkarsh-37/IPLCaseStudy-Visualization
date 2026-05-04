import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
print("Loading cleaned dataset...")
df = pd.read_csv("cleaned_merged_ipl_data.csv")
print("\n--- Task 12: Powerplay Performance (Overs 1-6) ---")
# Filter for overs 1 through 6
powerplay_df = df[df['over'] <= 6]
pp_total_runs = powerplay_df['total_runs'].sum()
print(f"Total runs scored in all Powerplays: {pp_total_runs}")

# Best teams in powerplay (Calculate average powerplay score per match)
pp_team_runs = powerplay_df.groupby('batting_team')['total_runs'].sum().reset_index()
pp_team_matches = powerplay_df.groupby('batting_team')['match_id'].nunique().reset_index()

pp_team_analysis = pd.merge(pp_team_runs, pp_team_matches, on='batting_team')
pp_team_analysis['avg_pp_runs_per_match'] = (pp_team_analysis['total_runs'] / pp_team_analysis['match_id']).round(2)
best_pp_teams = pp_team_analysis.sort_values(by='avg_pp_runs_per_match', ascending=False).head(5)
print("\nBest Teams in Powerplay (Average Runs per Match):")
print(best_pp_teams)

sns.set_theme(style="whitegrid")

# Visualizing the highest-scoring teams in the Powerplay
sns.barplot(x='avg_pp_runs_per_match', y='batting_team', data=best_pp_teams, palette='autumn')
plt.title('Top 5 Teams: Best Powerplay Average')
plt.xlabel('Average Runs in Powerplay')
plt.ylabel('Team')
plt.savefig('task_12_powerplay_teams.png')