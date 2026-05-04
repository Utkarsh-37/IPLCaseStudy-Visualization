import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
print("Loading cleaned dataset...")
df = pd.read_csv("cleaned_merged_ipl_data.csv")
print("\n--- Task 14: Run Distribution per Inning ---")
# Compare total runs scored in 1st innings vs 2nd innings
inning_runs = df.groupby('inning')['total_runs'].sum().reset_index()

# Filter out super overs (innings 3, 4, etc.) to keep the analysis clean
standard_innings = inning_runs[inning_runs['inning'].isin([1, 2])]
print(standard_innings)

# Comparing total runs across standard innings
labels = ['1st Innings', '2nd Innings']
plt.pie(standard_innings['total_runs'], labels=labels, autopct='%1.1f%%', colors=['#ff9999','#66b3ff'], startangle=140)
plt.title('Total Run Distribution: 1st vs 2nd Innings')
plt.savefig('task_14_innings_distribution.png')