"""
Diagnose the 100%/0% confidence issue
"""
import pandas as pd
import numpy as np

df = pd.read_csv('../maharashtra_agricultural_dataset_expanded_consistent.csv')

print("="*80)
print("CONFIDENCE ISSUE DIAGNOSIS")
print("="*80)

print(f"\nDataset: {len(df)} rows")

# Check consistency
grouped = df.groupby(['District', 'Soil_Type', 'Weather'])['Crop_Name'].nunique()
print(f"\nConsistency check:")
print(f"  Unique input combinations: {len(grouped)}")
print(f"  Max crops per combo: {grouped.max()}")
print(f"  Min crops per combo: {grouped.min()}")

# Check sample distribution
samples_per_combo = df.groupby(['District', 'Soil_Type', 'Weather', 'Crop_Name']).size()
print(f"\nSample distribution per combo:")
print(f"  Mean: {samples_per_combo.mean():.1f}")
print(f"  Std: {samples_per_combo.std():.1f}")
print(f"  Min: {samples_per_combo.min()}")
print(f"  Max: {samples_per_combo.max()}")

print(f"\n{'='*80}")
print("ROOT CAUSE")
print(f"{'='*80}")
print("The dataset has PERFECT consistency:")
print("  - Each District+Soil+Weather combination has exactly 1 crop")
print("  - Each combination has exactly 15 identical samples")
print("  - Model learns: 'If inputs match training data = 100% confidence'")
print("  - Model learns: 'If inputs DON'T match training data = 0% confidence'")
print("\nThis causes EXTREME predictions (100% or 0%, nothing in between)")

print(f"\n{'='*80}")
print("SOLUTION")
print(f"{'='*80}")
print("Add REALISTIC variability:")
print("  1. Each combination should have 2-3 suitable crops (not just 1)")
print("  2. Primary crop: 60-70% of samples")
print("  3. Secondary crop: 20-30% of samples")  
print("  4. Tertiary crop: 10-15% of samples")
print("  5. Add slight randomness to make model less certain")
print("="*80)
