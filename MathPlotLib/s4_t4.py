import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
print("Loading cleaned dataset...")
df = pd.read_csv("cleaned_merged_ipl_data.csv")
print("\n--- Task 4: Strike Rate of Batters ---")
# Logic: Wides do not count as a ball faced by the batter
valid_balls = df[df['extras_type'] != 'wides']
balls_faced = valid_balls.groupby('batter')['ball'].count().reset_index()
balls_faced.rename(columns={'ball': 'balls_faced'}, inplace=True)

batter_runs = df.groupby('batter')['batsman_runs'].sum().reset_index()

# Merge runs and balls faced
strike_rate_df = pd.merge(batter_runs, balls_faced, on='batter')
strike_rate_df['strike_rate'] = (strike_rate_df['batsman_runs'] / strike_rate_df['balls_faced']) * 100
strike_rate_df['strike_rate'] = strike_rate_df['strike_rate'].round(2)

# Filter for batters with > 100 balls faced to filter out tail-enders with inflated stats
top_strike_rates = strike_rate_df[strike_rate_df['balls_faced'] > 100].sort_values(by='strike_rate', ascending=False).head(10)
print(top_strike_rates)

sns.set_theme(style="whitegrid")
sns.barplot(x='strike_rate', y='batter', data=top_strike_rates, palette='magma')
plt.title('Top 10 Highest Strike Rates (Min 100 Balls Faced)')
plt.xlabel('Strike Rate')
plt.ylabel('Batter')
plt.savefig('task_4_strike_rates.png')