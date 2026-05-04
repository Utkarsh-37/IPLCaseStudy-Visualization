import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
print("Loading cleaned dataset...")
df = pd.read_csv("cleaned_merged_ipl_data.csv")
matches_df = df.drop_duplicates(subset=['match_id']).rename(columns={'match_id': 'id'})
print("\n--- Task 18: City-wise Scoring Trends ---")
city_matches = matches_df['city'].value_counts().reset_index()
city_matches.columns = ['city', 'total_matches']

city_runs = df.groupby('city')['total_runs'].sum().reset_index()
city_analysis = pd.merge(city_matches, city_runs, on='city')
city_analysis['avg_runs_per_match'] = (city_analysis['total_runs'] / city_analysis['total_matches']).round(2)

# Filter for a minimum of 10 matches to avoid skewed data from one-off high scoring games
high_scoring_cities = city_analysis[city_analysis['total_matches'] >= 10].sort_values('avg_runs_per_match', ascending=False)
print("Highest Scoring Cities (Minimum 10 Matches):")
print(high_scoring_cities.head())

sns.set_theme(style="whitegrid")

# Visualizing scoring trends in major cities
sns.barplot(x='avg_runs_per_match', y='city', data=high_scoring_cities.head(10), palette='viridis')
plt.title('Top 10 Highest Scoring Cities (Min 10 Matches)')
plt.xlabel('Average Runs per Match')
plt.ylabel('City')
plt.savefig('task_18_city_trends.png')