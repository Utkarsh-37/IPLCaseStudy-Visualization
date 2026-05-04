import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
print("Loading cleaned dataset...")
df = pd.read_csv("cleaned_merged_ipl_data.csv")
matches_df = df.drop_duplicates(subset=['match_id']).rename(columns={'match_id': 'id'})
match_team_runs = df.groupby(['match_id', 'batting_team'])['total_runs'].sum().reset_index()

# Programmatically find the team with the maximum runs per match
calculated_winners = match_team_runs.loc[match_team_runs.groupby('match_id')['total_runs'].idxmax()]
calculated_winners = calculated_winners.rename(columns={'batting_team': 'calculated_winner'})
actual_winners = df[['match_id', 'winner', 'method']].drop_duplicates()

winner_comparison = pd.merge(calculated_winners[['match_id', 'calculated_winner']], actual_winners, on='match_id')

winner_comparison['match_status'] = winner_comparison['calculated_winner'] == winner_comparison['winner']
matches_without_dls = winner_comparison[winner_comparison['method'] != 'D/L']

accuracy = (matches_without_dls['match_status'].sum() / len(matches_without_dls)) * 100
print(f"Accuracy of determining the winner purely by max runs (excluding D/L method): {accuracy:.2f}%")

# Visualizing the accuracy of the winning team calculation
labels = ['Correct Prediction', 'Incorrect (D/L or Other)']
sizes = [accuracy, 100 - accuracy]
colors = ['#4CAF50', '#F44336']

plt.figure(figsize=(7, 7))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90, explode=(0.1, 0))
plt.title('Accuracy of Determining Winner via Max Runs')
plt.savefig('task_20_prediction_accuracy.png')