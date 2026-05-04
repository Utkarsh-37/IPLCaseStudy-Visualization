import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
print("Loading cleaned dataset...")
df = pd.read_csv("cleaned_merged_ipl_data.csv")
print("\n--- Task 11: Runs per Over Analysis ---")
# Calculate total runs scored in each specific over (1 through 20)
over_runs = df.groupby('over')['total_runs'].sum().reset_index()
over_balls = df.groupby('over')['ball'].count().reset_index()

# Merge to calculate the average runs per over (Economy rate of that specific over)
over_analysis = pd.merge(over_runs, over_balls, on='over')
# Divide balls by 6 to get total number of actual overs bowled
over_analysis['avg_runs_per_over'] = (over_analysis['total_runs'] / (over_analysis['ball'] / 6)).round(2)

high_scoring_overs = over_analysis.sort_values(by='avg_runs_per_over', ascending=False)
print("Average Runs Scored in Each Over (Ranked by Highest):")
print(high_scoring_overs.head(20))

sns.set_theme(style="whitegrid")

# Visualizing the scoring trend across 20 overs
plt.plot(over_analysis['over'], over_analysis['avg_runs_per_over'], marker='o', color='darkviolet', linewidth=2)
plt.title('Average Runs Scored in Each Over (1-20)')
plt.xlabel('Over Number')
plt.ylabel('Average Runs')
plt.xticks(range(1, 21))
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('task_11_runs_per_over.png')