"""
Diagnose data quality issues in the dataset
"""

import pandas as pd
import numpy as np
from config import DATASET_PATH

def diagnose_dataset():
    """Analyze dataset quality"""
    print("="*70)
    print("DATASET QUALITY DIAGNOSTIC REPORT")
    print("="*70)
    
    df = pd.read_excel(DATASET_PATH)
    
    print(f"\n📊 Basic Statistics:")
    print(f"Total Rows: {len(df)}")
    print(f"Total Columns: {len(df.columns)}")
    print(f"Missing Values: {df.isnull().sum().sum()}")
    
    print(f"\n🌾 Crop Distribution:")
    crop_counts = df['Crop_Name'].value_counts()
    print(crop_counts)
    print(f"\nMin samples per crop: {crop_counts.min()}")
    print(f"Max samples per crop: {crop_counts.max()}")
    print(f"Imbalance ratio: {crop_counts.max() / crop_counts.min():.2f}x")
    
    print(f"\n🏘️ District Distribution:")
    district_counts = df['District'].value_counts()
    print(f"Districts: {district_counts.shape[0]}")
    print(f"Samples per district (avg): {district_counts.mean():.1f}")
    
    print(f"\n🌍 Soil Type Distribution:")
    print(df['Soil_Type'].value_counts())
    
    print(f"\n🌤️ Weather Distribution:")
    print(df['Weather'].value_counts())
    
    # Check for contradictions
    print(f"\n⚠️ Checking for contradictions...")
    grouping_cols = ['District', 'Soil_Type', 'Weather']
    grouped = df.groupby(grouping_cols)['Crop_Name'].nunique()
    contradictions = grouped[grouped > 1]
    
    if len(contradictions) > 0:
        print(f"❌ FOUND {len(contradictions)} contradictory patterns!")
        print("Same input conditions produce different crops:")
        print(contradictions.head(10))
    else:
        print("✅ No contradictions found")
    
    # Check class balance for fertilizers
    print(f"\n💊 Fertilizer Distribution:")
    print(df['Fertilizer'].value_counts())
    
    print("\n" + "="*70)
    print("DIAGNOSIS COMPLETE")
    print("="*70)

if __name__ == "__main__":
    diagnose_dataset()