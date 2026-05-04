import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
print("Loading cleaned dataset...")
df = pd.read_csv("cleaned_merged_ipl_data.csv")
matches_df = df.drop_duplicates(subset=['match_id']).rename(columns={'match_id': 'id'})
print("\n--- Task 16: Player of Match Contribution ---")
# 1. Extract unique match data directly from the merged df
pom_df = df[['match_id', 'player_of_match']].drop_duplicates().dropna()

# 2. Find the highest run scorer for every match
match_batters = df.groupby(['match_id', 'batter'])['batsman_runs'].sum().reset_index()
highest_scorers = match_batters.loc[match_batters.groupby('match_id')['batsman_runs'].idxmax()]

# 3. Merge and calculate
pom_impact = pd.merge(highest_scorers, pom_df, on='match_id')
pom_impact['is_highest_scorer'] = pom_impact['batter'] == pom_impact['player_of_match']

pom_highest_scorer_pct = (pom_impact['is_highest_scorer'].sum() / len(pom_impact)) * 100
print(f"Percentage of times the Player of the Match was the highest run scorer: {pom_highest_scorer_pct:.2f}%")

# Visualizing POM and highest scorer correlation
labels = ['POM is Highest Scorer', 'Other Performance']
sizes = [pom_highest_scorer_pct, 100 - pom_highest_scorer_pct]
colors = ['#ffcc00', '#eeeeee']

plt.figure(figsize=(7, 7))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140, explode=(0.1, 0))
plt.title('How Often the Highest Scorer wins Player of the Match?')
plt.savefig('task_16_pom_impact.png')