import pandas as pd

# Load dataset
df = pd.read_csv('../maharashtra_agricultural_dataset_realistic.csv')

# Check Ratnagiri data
print("="*60)
print("Checking Ratnagiri district data...")
print("="*60)

# All Ratnagiri data
ratnagiri = df[df['District'] == 'Ratnagiri']
print(f"\nTotal Ratnagiri records: {len(ratnagiri)}")
print(f"Unique crops in Ratnagiri: {ratnagiri['Crop_Name'].nunique()}")
print(f"Crops: {sorted(ratnagiri['Crop_Name'].unique().tolist())}")

# Soil types in Ratnagiri
print(f"\nSoil types in Ratnagiri: {sorted(ratnagiri['Soil_Type'].unique().tolist())}")

# Weather conditions in Ratnagiri
print(f"Weather conditions in Ratnagiri: {sorted(ratnagiri['Weather'].unique().tolist())}")

# Specific combination: Ratnagiri + Black + Monsoon
filtered = df[(df['District'] == 'Ratnagiri') & (df['Soil_Type'] == 'Black') & (df['Weather'] == 'Monsoon')]
print("\n" + "="*60)
print("Ratnagiri + Black Soil + Monsoon combination:")
print("="*60)
print(f"Total records: {len(filtered)}")
print(f"Unique crops: {filtered['Crop_Name'].nunique() if len(filtered) > 0 else 0}")
if len(filtered) > 0:
    print(f"Crops: {sorted(filtered['Crop_Name'].unique().tolist())}")
else:
    print("NO CROPS FOUND for this combination!")
    
# Check what soil + weather combinations exist for Ratnagiri
print("\n" + "="*60)
print("All Ratnagiri combinations:")
print("="*60)
combinations = ratnagiri.groupby(['Soil_Type', 'Weather'])['Crop_Name'].apply(lambda x: sorted(x.unique().tolist())).reset_index()
for idx, row in combinations.iterrows():
    print(f"\nSoil: {row['Soil_Type']}, Weather: {row['Weather']}")
    print(f"Crops ({len(row['Crop_Name'])}): {row['Crop_Name']}")
