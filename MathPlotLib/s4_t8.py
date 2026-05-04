import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
print("Loading cleaned dataset...")
df = pd.read_csv("cleaned_merged_ipl_data.csv")
print("\n--- Task 8: Boundary Analysis ---")
# Overall totals
total_4s = len(df[df['batsman_runs'] == 4])
total_6s = len(df[df['batsman_runs'] == 6])
print(f"Total 4s hit in IPL history: {total_4s}")
print(f"Total 6s hit in IPL history: {total_6s}\n")

# Top players by boundaries
boundaries_df = df[df['batsman_runs'].isin([4, 6])]
top_boundary_hitters = boundaries_df.groupby('batter')['batsman_runs'].count().reset_index()
top_boundary_hitters.rename(columns={'batsman_runs': 'total_boundaries'}, inplace=True)
top_boundary_hitters = top_boundary_hitters.sort_values(by='total_boundaries', ascending=False).head(10)
print("Top 10 Players by Total Boundaries:")
print(top_boundary_hitters)

sns.set_theme(style="whitegrid")

# Visualizing top boundary hitters
sns.barplot(x='total_boundaries', y='batter', data=top_boundary_hitters, palette='rocket')
plt.title('Top 10 Players by Total Boundaries (4s + 6s)')
plt.xlabel('Total Boundaries Hit')
plt.ylabel('Batter')
plt.savefig('task_8_boundary_hitters.png')