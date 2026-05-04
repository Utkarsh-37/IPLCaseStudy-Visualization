import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
print("Loading cleaned dataset...")
df = pd.read_csv("cleaned_merged_ipl_data.csv")
print("\n--- Task 2: Runs per Team per Match ---")
team_runs_per_match = df.groupby(['match_id', 'batting_team'])['total_runs'].sum().reset_index()
print(team_runs_per_match.head())

sns.set_theme(style="whitegrid")
# Visualizing team scoring consistency
sns.boxplot(x='total_runs', y='batting_team', data=team_runs_per_match, palette='Set2')
plt.title('Team-wise Run Scoring Distribution')
plt.xlabel('Total Runs in a Match')
plt.ylabel('Team')
plt.savefig('task_2_team_boxplot.png')