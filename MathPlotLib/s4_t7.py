import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
print("Loading cleaned dataset...")
df = pd.read_csv("cleaned_merged_ipl_data.csv")
print("\n--- Task 7: Highest Individual Score in a Match ---")
# Group by both match and batter to find the highest score in a single inning
highest_score_df = df.groupby(['match_id', 'batter'])['batsman_runs'].sum().reset_index()
top_individual_scores = highest_score_df.sort_values(by='batsman_runs', ascending=False).head(10)
print(top_individual_scores)

sns.set_theme(style="whitegrid")

# Visualizing the highest individual scores in a single match
sns.barplot(x='batsman_runs', y='batter', data=top_individual_scores, palette='crest')
plt.title('Top 10 Highest Individual Scores in a Single Match')
plt.xlabel('Runs Scored')
plt.ylabel('Batter')
plt.savefig('task_7_highest_scores.png')