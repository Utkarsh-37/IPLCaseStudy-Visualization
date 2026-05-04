import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
print("Loading cleaned dataset...")
df = pd.read_csv("cleaned_merged_ipl_data.csv")
print("\n--- Task 13: Death Overs Performance (Overs 16-20) ---")
# Filter for overs 16 through 20
death_overs_df = df[df['over'] >= 16]
death_total_runs = death_overs_df['total_runs'].sum()
print(f"Total runs scored in all Death Overs: {death_total_runs}")

# Best teams in death overs (Calculate average death over score per match)
death_team_runs = death_overs_df.groupby('batting_team')['total_runs'].sum().reset_index()
death_team_matches = death_overs_df.groupby('batting_team')['match_id'].nunique().reset_index()

death_team_analysis = pd.merge(death_team_runs, death_team_matches, on='batting_team')
death_team_analysis['avg_death_runs_per_match'] = (death_team_analysis['total_runs'] / death_team_analysis['match_id']).round(2)
best_death_teams = death_team_analysis.sort_values(by='avg_death_runs_per_match', ascending=False).head(5)
print("\nBest Teams in Death Overs (Average Runs per Match):")
print(best_death_teams)

# Best batters in death overs (Based on strike rate, minimum 50 balls faced)
death_batter_sr = death_overs_df.groupby('batter').agg(
    total_runs_scored=('batsman_runs', 'sum'), 
    balls_faced=('ball', 'count')
).reset_index()
death_batter_sr['strike_rate'] = ((death_batter_sr['total_runs_scored'] / death_batter_sr['balls_faced']) * 100).round(2)

best_death_batters = death_batter_sr[death_batter_sr['balls_faced'] > 50].sort_values(by='strike_rate', ascending=False).head(5)
print("\nMost Destructive Batters in Death Overs (Min 50 balls faced):")
print(best_death_batters)

sns.set_theme(style="whitegrid")

# Visualizing the most destructive finishers (Overs 16-20)
sns.barplot(x='strike_rate', y='batter', data=best_death_batters, palette='winter')
plt.title('Top 5 Death Over Batters by Strike Rate')
plt.xlabel('Strike Rate (Min 50 Balls)')
plt.ylabel('Batter')
plt.savefig('task_13_death_batters.png')