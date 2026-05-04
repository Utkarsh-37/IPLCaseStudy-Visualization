import pandas as pd
import numpy as np

# ==========================================
# STAGE 1: Data Ingestion
# ==========================================
print("--- Stage 1: Data Ingestion ---")

# Load datasets into Pandas DataFrames
# Assuming the CSV files are in the same directory as your script
deliveries_df = pd.read_csv("deliveries.csv")
matches_df = pd.read_csv("matches.csv")

# Inspect shape, columns, and data types
print(f"Deliveries shape: {deliveries_df.shape}")
print(f"Matches shape: {matches_df.shape}")
print("\nDeliveries Columns:", list(deliveries_df.columns))
print("Matches Columns:", list(matches_df.columns))


# ==========================================
# STAGE 2: Data Cleaning & Validation
# ==========================================
print("\n--- Stage 2: Data Cleaning & Validation ---")

# Check for missing values (filtering to only show columns that actually have missing data)
missing_deliveries = deliveries_df.isnull().sum()
print("Missing values in Deliveries:\n", missing_deliveries[missing_deliveries > 0])

missing_matches = matches_df.isnull().sum()
print("\nMissing values in Matches:\n", missing_matches[missing_matches > 0])

# Validate match IDs alignment between datasets
delivery_match_ids = set(deliveries_df['match_id'].unique())
matches_ids = set(matches_df['id'].unique())

unmatched_ids = delivery_match_ids - matches_ids
if len(unmatched_ids) == 0:
    print("\nValidation Passed: All match IDs in deliveries perfectly align with matches metadata.")
else:
    print(f"\nWarning: Found {len(unmatched_ids)} match IDs in deliveries without matching metadata.")


# ==========================================
# STAGE 3: Data Transformation
# ==========================================
print("\n--- Stage 3: Data Transformation ---")

# 1. Create new columns: Total runs per ball
# standard IPL datasets usually have 'batsman_runs' and 'extra_runs'
if 'total_runs' not in deliveries_df.columns:
    if 'batsman_runs' in deliveries_df.columns and 'extra_runs' in deliveries_df.columns:
        deliveries_df['total_runs'] = deliveries_df['batsman_runs'] + deliveries_df['extra_runs']
        print("Calculated and created 'total_runs' column.")

# 2. Standardize columns: Ensure consistent naming (snake_case, lowercased, stripped spaces)
deliveries_df.columns = [col.strip().lower().replace(" ", "_") for col in deliveries_df.columns]
matches_df.columns = [col.strip().lower().replace(" ", "_") for col in matches_df.columns]
print("Standardized column names to snake_case.")

# 3. Merge datasets
# Merging ball-by-ball delivery data with match metadata
merged_df = deliveries_df.merge(
    matches_df, 
    left_on="match_id", 
    right_on="id", 
    how="inner",
    suffixes=('_delivery', '_match') # In case of overlapping column names (like 'umpire1')
)

print(f"\nMerge successful! Unified DataFrame shape: {merged_df.shape}")

# Save the transformed dataset as a checkpoint
merged_df.to_csv("cleaned_merged_ipl_data.csv", index=False)
print("Saved transformed data to 'cleaned_merged_ipl_data.csv'")
# The merged_df is now ready for Stage 4