"""
Create REALISTIC dataset with proper confidence distribution
- Multiple valid crops per District+Soil+Weather (2-3 crops)
- Primary crop: 60%, Secondary: 30%, Tertiary: 10%
- This will give realistic confidence scores (60-70%, 20-30%, 5-15%)
"""

import pandas as pd
import numpy as np
import random
from validation import validate_prediction, get_alternative_crops, DISTRICT_TO_REGION

np.random.seed(42)
random.seed(42)

print("="*80)
print("CREATING REALISTIC DATASET WITH PROPER CONFIDENCE DISTRIBUTION")
print("="*80)

# Load base cleaned dataset
df_base = pd.read_csv('../maharashtra_agricultural_dataset_cleaned_v2_validated.csv')
print(f"\nBase dataset: {len(df_base)} unique combinations")

realistic_data = []
samples_per_combo = 25  # More samples for better distribution

print(f"\nGenerating realistic multi-crop samples...")

for idx, base_row in df_base.iterrows():
    district = base_row['District']
    soil = base_row['Soil_Type']
    weather = base_row['Weather']
    primary_crop = base_row['Crop_Name']
    
    # Get all valid crops for this combination
    valid_crops = get_alternative_crops(district, soil, weather)
    
    if len(valid_crops) == 0:
        continue
    
    # Ensure primary crop is in valid list
    if primary_crop not in valid_crops:
        primary_crop = valid_crops[0] if valid_crops else primary_crop
    
    # Select 2-3 crops for this combination
    if len(valid_crops) >= 3:
        # Select primary + 2 others
        other_crops = [c for c in valid_crops if c != primary_crop]
        selected_crops = [primary_crop] + random.sample(other_crops, min(2, len(other_crops)))
    elif len(valid_crops) == 2:
        selected_crops = valid_crops
    else:
        selected_crops = [primary_crop]
    
    # Distribution: Primary (60%), Secondary (30%), Tertiary (10%)
    if len(selected_crops) == 3:
        crop_distribution = [
            (selected_crops[0], 15),  # 60% primary
            (selected_crops[1], 7),   # 28% secondary
            (selected_crops[2], 3)    # 12% tertiary
        ]
    elif len(selected_crops) == 2:
        crop_distribution = [
            (selected_crops[0], 17),  # 68% primary
            (selected_crops[1], 8)    # 32% secondary
        ]
    else:
        crop_distribution = [
            (selected_crops[0], 25)   # 100% (only option)
        ]
    
    # Generate samples for each crop
    for crop, count in crop_distribution:
        for _ in range(count):
            new_row = base_row.copy()
            new_row['Crop_Name'] = crop
            
            # Add variations to nutrients
            new_row['N_kg_ha'] = max(1, base_row['N_kg_ha'] * np.random.uniform(0.80, 1.20))
            new_row['P2O5_kg_ha'] = max(1, base_row['P2O5_kg_ha'] * np.random.uniform(0.80, 1.20))
            new_row['K2O_kg_ha'] = max(1, base_row['K2O_kg_ha'] * np.random.uniform(0.80, 1.20))
            new_row['Zn_kg_ha'] = max(0.5, base_row['Zn_kg_ha'] * np.random.uniform(0.85, 1.15))
            new_row['S_kg_ha'] = max(0.5, base_row['S_kg_ha'] * np.random.uniform(0.85, 1.15))
            
            # Vary pH slightly
            new_row['Recommended_pH'] = np.clip(
                base_row['Recommended_pH'] + np.random.uniform(-0.4, 0.4),
                5.0, 8.5
            )
            
            # Vary water parameters
            new_row['Turbidity_NTU'] = max(1, base_row['Turbidity_NTU'] * np.random.uniform(0.80, 1.20))
            new_row['Water_Temp_C'] = np.clip(
                base_row['Water_Temp_C'] + np.random.uniform(-3, 3),
                25, 38
            )
            
            # Round values
            new_row['N_kg_ha'] = round(new_row['N_kg_ha'], 1)
            new_row['P2O5_kg_ha'] = round(new_row['P2O5_kg_ha'], 1)
            new_row['K2O_kg_ha'] = round(new_row['K2O_kg_ha'], 1)
            new_row['Zn_kg_ha'] = round(new_row['Zn_kg_ha'], 1)
            new_row['S_kg_ha'] = round(new_row['S_kg_ha'], 1)
            new_row['Recommended_pH'] = round(new_row['Recommended_pH'], 1)
            new_row['Turbidity_NTU'] = round(new_row['Turbidity_NTU'], 1)
            new_row['Water_Temp_C'] = round(new_row['Water_Temp_C'], 1)
            
            realistic_data.append(new_row.to_dict())
    
    if (idx + 1) % 50 == 0:
        print(f"  Processed {idx + 1}/{len(df_base)} combinations...")

# Create DataFrame
df_realistic = pd.DataFrame(realistic_data)

# Shuffle
df_realistic = df_realistic.sample(frac=1, random_state=42).reset_index(drop=True)

print(f"\n✓ Generated {len(df_realistic)} rows")

# Analyze distribution
print(f"\n{'='*80}")
print("DISTRIBUTION ANALYSIS")
print(f"{'='*80}")

combos_with_crops = df_realistic.groupby(['District', 'Soil_Type', 'Weather'])['Crop_Name'].nunique()
print(f"Crops per combination:")
print(f"  Min: {combos_with_crops.min()}")
print(f"  Max: {combos_with_crops.max()}")
print(f"  Mean: {combos_with_crops.mean():.2f}")

print(f"\nDistribution breakdown:")
print(f"  1 crop: {(combos_with_crops == 1).sum()} ({(combos_with_crops == 1).sum()/len(combos_with_crops)*100:.1f}%)")
print(f"  2 crops: {(combos_with_crops == 2).sum()} ({(combos_with_crops == 2).sum()/len(combos_with_crops)*100:.1f}%)")
print(f"  3 crops: {(combos_with_crops == 3).sum()} ({(combos_with_crops == 3).sum()/len(combos_with_crops)*100:.1f}%)")

# Check a sample combination
sample_combo = df_realistic.groupby(['District', 'Soil_Type', 'Weather']).first().iloc[10]
sample_district = sample_combo.name[0]
sample_soil = sample_combo.name[1]
sample_weather = sample_combo.name[2]

sample_data = df_realistic[
    (df_realistic['District'] == sample_district) &
    (df_realistic['Soil_Type'] == sample_soil) &
    (df_realistic['Weather'] == sample_weather)
]

print(f"\nSample combination: {sample_district} + {sample_soil} + {sample_weather}")
crop_counts = sample_data['Crop_Name'].value_counts()
print(f"Crop distribution:")
for crop, count in crop_counts.items():
    pct = (count / len(sample_data)) * 100
    print(f"  {crop:20s}: {count:2d} samples ({pct:5.1f}%)")

# Validate
print(f"\n{'='*80}")
print("VALIDATION CHECK")
print(f"{'='*80}")

sample_size = min(300, len(df_realistic))
sample = df_realistic.sample(n=sample_size, random_state=42)

valid_count = 0
for idx, row in sample.iterrows():
    validation = validate_prediction(row['District'], row['Soil_Type'], row['Crop_Name'], row['Weather'])
    if validation['is_valid']:
        valid_count += 1

print(f"Validation on {sample_size} samples:")
print(f"  Valid: {valid_count} ({valid_count/sample_size*100:.1f}%)")
print(f"  Invalid: {sample_size - valid_count} ({(sample_size - valid_count)/sample_size*100:.1f}%)")

# Statistics
print(f"\n{'='*80}")
print("DATASET STATISTICS")
print(f"{'='*80}")
print(f"Total rows: {len(df_realistic)}")
print(f"Districts: {df_realistic['District'].nunique()}")
print(f"Crops: {df_realistic['Crop_Name'].nunique()}")
print(f"Unique combinations: {len(df_realistic.groupby(['District', 'Soil_Type', 'Weather']))}")

print(f"\nTop 10 Crops:")
for crop, count in df_realistic['Crop_Name'].value_counts().head(10).items():
    print(f"  {crop:20s}: {count:4d} ({count/len(df_realistic)*100:5.1f}%)")

# Save
output_file = '../maharashtra_agricultural_dataset_realistic.csv'
df_realistic.to_csv(output_file, index=False)

print(f"\n{'='*80}")
print("SAVED REALISTIC DATASET")
print(f"{'='*80}")
print(f"✓ File: {output_file}")
print(f"✓ Rows: {len(df_realistic)}")
print(f"✓ Multi-crop combinations: {(combos_with_crops > 1).sum()} ({(combos_with_crops > 1).sum()/len(combos_with_crops)*100:.1f}%)")
print(f"✓ Validation accuracy: {valid_count/sample_size*100:.1f}%")

print(f"\n{'='*80}")
print("EXPECTED CONFIDENCE SCORES")
print(f"{'='*80}")
print("With this realistic distribution:")
print("  Primary crop: 55-70% confidence (most samples)")
print("  Secondary crop: 25-35% confidence")
print("  Tertiary crop: 8-15% confidence")
print("\nNO MORE 100% or 0% extremes!")
print(f"{'='*80}\n")
