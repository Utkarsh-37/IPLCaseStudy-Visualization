import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Loading cleaned dataset...")
df = pd.read_csv("cleaned_merged_ipl_data.csv")

print("\n--- Task 1: Total Runs per Match ---")

# Group by the unique match ID and sum up the total_runs for that match
runs_per_match = df.groupby('match_id')['total_runs'].sum().reset_index()

# Rename the column for better clarity in our final reports
runs_per_match.rename(columns={'total_runs': 'total_match_runs'}, inplace=True)

# Display the first few rows to verify
print(runs_per_match.head())

# Set visual style
sns.set_theme(style="whitegrid")

# Plotting the distribution of match scores
plt.hist(runs_per_match['total_match_runs'], bins=20, color='skyblue', edgecolor='black')
plt.title('Distribution of Total Runs per Match')
plt.xlabel('Total Runs')
plt.ylabel('Frequency')
plt.savefig('task_1_runs_distribution.png')