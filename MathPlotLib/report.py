import pandas as pd
import numpy as np
import os

# --- Setup ---
# Load the datasets
matches = pd.read_csv('matches.csv')
deliveries = pd.read_csv('deliveries.csv')

# Create the output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

# --- Stage 6: Reporting (Data Structuring & Cleaning) ---

# 1. runs_per_match
runs_per_match = deliveries.groupby('match_id')['total_runs'].sum().reset_index()
runs_per_match.columns = ['match_id', 'total_match_runs']
runs_per_match = runs_per_match.sort_values(by='total_match_runs', ascending=False)

# 2. top_batters (Consistency & Volume)
batter_match_runs = deliveries.groupby(['match_id', 'batter'])['batsman_runs'].sum().reset_index()
top_batters = batter_match_runs.groupby('batter').agg(
    total_runs=('batsman_runs', 'sum'),
    innings_played=('match_id', 'nunique'),
    average_runs=('batsman_runs', 'mean'),
    std_dev_runs=('batsman_runs', 'std')
).reset_index()
# Filter for regular batters and calculate consistency (Coefficient of Variation)
top_batters = top_batters[top_batters['total_runs'] > 1000]
top_batters['consistency_score'] = top_batters['std_dev_runs'] / top_batters['average_runs']
top_batters = top_batters.sort_values(by='total_runs', ascending=False)

# 3. strike_rate
balls_faced = deliveries[~deliveries['extras_type'].isin(['wides'])].groupby('batter')['ball'].count().reset_index()
balls_faced.columns = ['batter', 'balls_faced']
strike_rate = top_batters.merge(balls_faced, on='batter', how='inner')
strike_rate['career_strike_rate'] = (strike_rate['total_runs'] / strike_rate['balls_faced']) * 100
strike_rate = strike_rate[['batter', 'total_runs', 'career_strike_rate']].sort_values(by='career_strike_rate', ascending=False)

# 4. economy (Bowlers)
bowler_runs = deliveries.groupby('bowler')['total_runs'].sum().reset_index()
# Filter out wides and no-balls for legal delivery count
legal_balls = deliveries[~deliveries['extras_type'].isin(['wides', 'noballs'])].groupby('bowler')['ball'].count().reset_index()
economy = pd.merge(bowler_runs, legal_balls, on='bowler')
economy.columns = ['bowler', 'runs_conceded', 'legal_deliveries']
economy['overs_bowled'] = economy['legal_deliveries'] / 6
economy = economy[economy['overs_bowled'] > 50] # Filter for minimum 50 overs bowled
economy['economy_rate'] = economy['runs_conceded'] / economy['overs_bowled']
economy = economy.sort_values(by='economy_rate', ascending=True)

# 5. team_scores (Venue Scoring Trends)
match_scores = deliveries.groupby(['match_id', 'inning', 'batting_team'])['total_runs'].sum().reset_index()
match_venue = match_scores.merge(matches[['id', 'venue']], left_on='match_id', right_on='id')
team_scores = match_venue.groupby('venue').agg(
    average_innings_score=('total_runs', 'mean'),
    total_innings_played=('match_id', 'count')
).reset_index()
team_scores = team_scores[team_scores['total_innings_played'] > 10]
team_scores = team_scores.sort_values(by='average_innings_score', ascending=False)

# 6. death_overs (Overs 16-20 Analysis)
# 'over' is 0-indexed in most IPL datasets, so 15 corresponds to the 16th over
death_over_deliveries = deliveries[deliveries['over'] >= 15]
death_overs = death_over_deliveries.groupby('batting_team').agg(
    death_runs_scored=('total_runs', 'sum'),
    death_balls_faced=('ball', 'count')
).reset_index()
death_overs['death_over_run_rate'] = (death_overs['death_runs_scored'] / death_overs['death_balls_faced']) * 6
death_overs = death_overs.sort_values(by='death_over_run_rate', ascending=False)


# --- Stage 7: Data Export ---

print("Saving individual CSV files to /output directory...")
runs_per_match.to_csv('output/runs_per_match.csv', index=False)
top_batters.to_csv('output/top_batters.csv', index=False)
strike_rate.to_csv('output/strike_rate.csv', index=False)
economy.to_csv('output/economy.csv', index=False)
team_scores.to_csv('output/team_scores.csv', index=False)
death_overs.to_csv('output/death_overs.csv', index=False)

print("Compiling all sheets into ipl_analysis.xlsx...")
with pd.ExcelWriter("output/ipl_analysis.xlsx") as writer:
    runs_per_match.to_excel(writer, sheet_name="Runs per Match", index=False)
    top_batters.to_excel(writer, sheet_name="Top Batters", index=False)
    strike_rate.to_excel(writer, sheet_name="Strike Rate", index=False)
    economy.to_excel(writer, sheet_name="Economy", index=False)
    team_scores.to_excel(writer, sheet_name="Venue Scores", index=False)
    death_overs.to_excel(writer, sheet_name="Death Overs", index=False)

print("Export complete. Deliverables are ready.")