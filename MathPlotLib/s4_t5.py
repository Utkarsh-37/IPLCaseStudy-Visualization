import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
print("Loading cleaned dataset...")
df = pd.read_csv("cleaned_merged_ipl_data.csv")
print("\n--- Task 5: Top 10 Bowlers by Economy ---")
# Logic: Legal balls exclude wides and no-balls
bowler_runs = df.groupby('bowler')['total_runs'].sum().reset_index() 
legal_balls = df[~df['extras_type'].isin(['wides', 'noballs'])].groupby('bowler')['ball'].count().reset_index()
legal_balls.rename(columns={'ball': 'legal_balls_bowled'}, inplace=True)

economy_df = pd.merge(bowler_runs, legal_balls, on='bowler')
economy_df['overs_bowled'] = economy_df['legal_balls_bowled'] / 6
economy_df['economy_rate'] = (economy_df['total_runs'] / economy_df['overs_bowled']).round(2)

# Filter for bowlers who have bowled at least 10 overs (60 balls) to get realistic stats
top_economy = economy_df[economy_df['legal_balls_bowled'] >= 60].sort_values(by='economy_rate', ascending=True).head(10)
print(top_economy)

sns.set_theme(style="whitegrid")
sns.barplot(x='economy_rate', y='bowler', data=top_economy, palette='coolwarm')
plt.title('Top 10 Most Economical Bowlers (Min 10 Overs)')
plt.xlabel('Economy Rate')
plt.ylabel('Bowler')
plt.savefig('task_5_bowler_economy.png')