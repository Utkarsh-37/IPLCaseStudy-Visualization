import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
print("Loading cleaned dataset...")
df = pd.read_csv("cleaned_merged_ipl_data.csv")
print("\n--- Task 3: Top 10 Batters ---")
top_10_batters = df.groupby('batter')['batsman_runs'].sum().reset_index()
top_10_batters = top_10_batters.sort_values(by='batsman_runs', ascending=False).head(10)
print(top_10_batters)

sns.set_theme(style="whitegrid")
# Ranking the top 10 batters
sns.barplot(x='batsman_runs', y='batter', data=top_10_batters, palette='viridis')
plt.title('Top 10 Run Scorers in IPL History')
plt.xlabel('Total Career Runs')
plt.ylabel('Batter')
plt.savefig('task_3_top_batters.png')