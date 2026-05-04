import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
print("Loading cleaned dataset...")
df = pd.read_csv("cleaned_merged_ipl_data.csv")
matches_df = df.drop_duplicates(subset=['match_id']).rename(columns={'match_id': 'id'})
print("\n--- Task 17: Venue-wise Analysis ---")
venue_matches = matches_df['venue'].value_counts().reset_index()
venue_matches.columns = ['venue', 'total_matches']

venue_runs = df.groupby('venue')['total_runs'].sum().reset_index()
venue_analysis = pd.merge(venue_matches, venue_runs, on='venue')
venue_analysis['avg_runs_per_match'] = (venue_analysis['total_runs'] / venue_analysis['total_matches']).round(2)

print("Venue Analysis (Top 5 Most Played Venues):")
print(venue_analysis.head())

sns.set_theme(style="whitegrid")

# Visualizing top 5 most played venues by average score
# Corrected the x-axis column name to 'avg_runs_per_match'
sns.barplot(x='avg_runs_per_match', y='venue', data=venue_analysis.head(5), palette='plasma')
plt.title('Average Runs per Match at Top 5 Most Played Venues')
plt.xlabel('Average Runs')
plt.ylabel('Venue')
plt.savefig('task_17_venue_scores.png')