import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
print("Loading cleaned dataset...")
df = pd.read_csv("cleaned_merged_ipl_data.csv")
print("\n--- Task 10: Dot Ball Analysis ---")
# Count dot balls where NO runs were scored off the delivery (total_runs == 0)
dot_balls = df[df['total_runs'] == 0]
print(f"Total dot balls bowled: {len(dot_balls)}\n")

# Identify bowlers with the most dot balls
top_dot_bowlers = dot_balls.groupby('bowler')['ball'].count().reset_index()
top_dot_bowlers.rename(columns={'ball': 'dot_balls_bowled'}, inplace=True)
top_dot_bowlers = top_dot_bowlers.sort_values(by='dot_balls_bowled', ascending=False).head(10)
print("Top 10 Bowlers by Dot Balls Bowled:")
print(top_dot_bowlers)

sns.set_theme(style="whitegrid")

# Visualizing bowlers with the most dot balls
sns.barplot(x='dot_balls_bowled', y='bowler', data=top_dot_bowlers, palette='mako')
plt.title('Top 10 Bowlers by Total Dot Balls Bowled')
plt.xlabel('Number of Dot Balls')
plt.ylabel('Bowler')
plt.savefig('task_10_dot_balls.png')