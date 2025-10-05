"""
Fix AI-generated dataset inconsistencies
Problem: Same District+Soil+Weather maps to multiple crops (up to 9!)
Solution: Keep only the most suitable/common crop per combination
"""

import pandas as pd
import numpy as np
from validation import validate_prediction, DISTRICT_TO_REGION

print("="*80)
print("DATASET ANALYSIS & FIXING")
print("="*80)

# Load dataset
df = pd.read_csv('../maharashtra_agricultural_dataset_10000_research_based.csv')
print(f"\nOriginal dataset: {len(df)} rows")

# Analyze inconsistencies
grouped = df.groupby(['District', 'Soil_Type', 'Weather'])['Crop_Name'].nunique()
print(f"\nInconsistency analysis:")
print(f"  Unique crops per combination - Min: {grouped.min()}, Max: {grouped.max()}, Mean: {grouped.mean():.2f}")
print(f"  Total combinations: {len(grouped)}")
print(f"  Single crop combos: {(grouped == 1).sum()} ({(grouped == 1).sum()/len(grouped)*100:.1f}%)")
print(f"  Multi-crop combos: {(grouped > 1).sum()} ({(grouped > 1).sum()/len(grouped)*100:.1f}%)")

print("\n" + "="*80)
print("STRATEGY 1: Keep Most Common Crop Per Combination")
print("="*80)

# Strategy 1: Keep the most frequent crop for each combination
def get_most_common_crop(group):
    """Return row with most common crop in this group"""
    crop_counts = group['Crop_Name'].value_counts()
    most_common_crop = crop_counts.index[0]
    
    # Get first row with this crop
    return group[group['Crop_Name'] == most_common_crop].iloc[0]

df_fixed1 = df.groupby(['District', 'Soil_Type', 'Weather'], as_index=False).apply(get_most_common_crop)
df_fixed1 = df_fixed1.reset_index(drop=True)

print(f"\nFixed dataset (Strategy 1): {len(df_fixed1)} rows")
print(f"Reduction: {len(df) - len(df_fixed1)} rows ({(1 - len(df_fixed1)/len(df))*100:.1f}%)")

# Verify no duplicates
duplicates = df_fixed1.groupby(['District', 'Soil_Type', 'Weather'])['Crop_Name'].nunique()
print(f"Duplicate check: Max crops per combo = {duplicates.max()}")

print("\n" + "="*80)
print("STRATEGY 2: Keep Validated Crop (Scientific Accuracy)")
print("="*80)

# Strategy 2: For each combination, keep only validated crops
def get_validated_crop(group):
    """Return row with validated crop, prefer most common"""
    district = group.iloc[0]['District']
    soil = group.iloc[0]['Soil_Type']
    weather = group.iloc[0]['Weather']
    
    # Try each crop in order of frequency
    crop_counts = group['Crop_Name'].value_counts()
    
    for crop in crop_counts.index:
        validation = validate_prediction(district, soil, crop, weather)
        if validation['is_valid']:
            # Return first row with this validated crop
            return group[group['Crop_Name'] == crop].iloc[0]
    
    # If no valid crop found, return most common anyway
    most_common_crop = crop_counts.index[0]
    return group[group['Crop_Name'] == most_common_crop].iloc[0]

df_fixed2 = df.groupby(['District', 'Soil_Type', 'Weather'], as_index=False).apply(get_validated_crop)
df_fixed2 = df_fixed2.reset_index(drop=True)

print(f"\nFixed dataset (Strategy 2): {len(df_fixed2)} rows")

# Validate the fixed dataset
print("\nValidating fixed dataset...")
validation_errors = 0
sample_size = min(500, len(df_fixed2))
sample = df_fixed2.sample(n=sample_size, random_state=42)

for idx, row in sample.iterrows():
    validation = validate_prediction(row['District'], row['Soil_Type'], row['Crop_Name'], row['Weather'])
    if not validation['is_valid']:
        validation_errors += 1

print(f"Validation on {sample_size} samples:")
print(f"  Valid: {sample_size - validation_errors} ({(sample_size - validation_errors)/sample_size*100:.1f}%)")
print(f"  Invalid: {validation_errors} ({validation_errors/sample_size*100:.1f}%)")

print("\n" + "="*80)
print("SAVING CLEANED DATASETS")
print("="*80)

# Save both versions
output1 = '../maharashtra_agricultural_dataset_cleaned_v1.csv'
output2 = '../maharashtra_agricultural_dataset_cleaned_v2_validated.csv'

df_fixed1.to_csv(output1, index=False)
print(f"✓ Strategy 1 (Most Common): {output1}")
print(f"  {len(df_fixed1)} rows")

df_fixed2.to_csv(output2, index=False)
print(f"✓ Strategy 2 (Validated): {output2}")
print(f"  {len(df_fixed2)} rows")

# Crop distribution comparison
print("\n" + "="*80)
print("CROP DISTRIBUTION COMPARISON")
print("="*80)

print("\nOriginal dataset:")
orig_crops = df['Crop_Name'].value_counts().head(10)
for crop, count in orig_crops.items():
    print(f"  {crop:20s}: {count:4d} ({count/len(df)*100:5.1f}%)")

print("\nCleaned dataset (Strategy 2):")
clean_crops = df_fixed2['Crop_Name'].value_counts().head(10)
for crop, count in clean_crops.items():
    print(f"  {crop:20s}: {count:4d} ({count/len(df_fixed2)*100:5.1f}%)")

print("\n" + "="*80)
print("RECOMMENDATION")
print("="*80)
print("\nUse Strategy 2 (Validated) for best results:")
print(f"  File: {output2}")
print(f"  Update config.py: DATASET_PATH = '{output2.replace('../', '')}'")
print(f"  Expected accuracy: 80-90%+")
print("="*80 + "\n")
