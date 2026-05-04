import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
print("Loading cleaned dataset...")
df = pd.read_csv("cleaned_merged_ipl_data.csv")
print("\n--- Task 15: Toss Impact Analysis ---")
# We need to drop duplicates on match_id because the merged df has 260,000 rows
# We only need 1 row per match to check the toss outcome
unique_matches = df.drop_duplicates(subset=['match_id']).copy()

# Filter out matches with no winner (No Result / Abandoned)
valid_matches = unique_matches.dropna(subset=['winner', 'toss_winner'])

# Check if toss_winner is the same as the match winner
toss_and_match_winner = valid_matches[valid_matches['toss_winner'] == valid_matches['winner']]

toss_advantage_pct = (len(toss_and_match_winner) / len(valid_matches)) * 100
print(f"Percentage of matches won by the team that won the toss: {toss_advantage_pct:.2f}%")

# Visualizing the percentage of matches won by the toss winner
labels = ['Toss Winner Won', 'Toss Winner Lost']
sizes = [toss_advantage_pct, 100 - toss_advantage_pct]
colors = ['#99ff99', '#ffcc99']

plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90, explode=(0.1, 0))
plt.title('Toss Impact on Match Results')
plt.axis('equal') # Ensures pie is a circle
plt.savefig('task_15_toss_impact.png')