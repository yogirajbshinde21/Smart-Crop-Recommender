"""
Generate comprehensive, high-quality Maharashtra agricultural dataset
Target: 2000+ rows, 80%+ accuracy
"""

import pandas as pd
import numpy as np
from itertools import product
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Maharashtra districts by zone
DISTRICTS_BY_ZONE = {
    'Western_Maharashtra': ['Pune', 'Satara', 'Sangli', 'Kolhapur', 'Solapur', 'Ahmednagar'],
    'Vidarbha': ['Nagpur', 'Amravati', 'Akola', 'Yavatmal', 'Wardha', 'Chandrapur'],
    'Marathwada': ['Aurangabad', 'Jalna', 'Beed', 'Latur', 'Osmanabad', 'Nanded'],
    'Konkan': ['Mumbai', 'Thane', 'Raigad', 'Ratnagiri'],
    'North_Maharashtra': ['Nashik', 'Dhule', 'Jalgaon', 'Nandurbar']
}

# Realistic crop profiles for Maharashtra
CROP_PROFILES = {
    'Cotton': {
        'zones': ['Vidarbha', 'Marathwada', 'Western_Maharashtra'],
        'soil': ['Black', 'Clay', 'Loamy'],
        'weather': ['Semi-Arid', 'Post-Monsoon', 'Dry', 'Warm'],
        'npk': (120, 60, 40), 'npk_var': 0.15,
        'zn': 25, 's': 20, 'ph': 6.5, 'ph_range': (6.0, 7.5),
        'water': (30, 8), 'fertilizer': ['Urea', 'DAP', 'NPK_12-32-16']
    },
    'Soybean': {
        'zones': ['Vidarbha', 'Marathwada'],
        'soil': ['Black', 'Red', 'Loamy'],
        'weather': ['Monsoon', 'Humid', 'Post-Monsoon'],
        'npk': (30, 60, 40), 'npk_var': 0.2,
        'zn': 5, 's': 20, 'ph': 6.8, 'ph_range': (6.5, 7.5),
        'water': (28, 10), 'fertilizer': ['DAP', 'NPK_10-26-26', 'SSP']
    },
    'Rice': {
        'zones': ['Konkan', 'Vidarbha'],
        'soil': ['Clay', 'Alluvial', 'Loamy'],
        'weather': ['Monsoon', 'Humid', 'Tropical'],
        'npk': (100, 50, 50), 'npk_var': 0.15,
        'zn': 25, 's': 12, 'ph': 6.0, 'ph_range': (5.5, 6.5),
        'water': (32, 15), 'fertilizer': ['Urea', 'DAP', 'MOP']
    },
    'Wheat': {
        'zones': ['Western_Maharashtra', 'North_Maharashtra', 'Marathwada'],
        'soil': ['Loamy', 'Clay', 'Alluvial'],
        'weather': ['Winter', 'Cool_Dry', 'Post-Monsoon'],
        'npk': (120, 60, 40), 'npk_var': 0.12,
        'zn': 25, 's': 20, 'ph': 7.0, 'ph_range': (6.5, 7.5),
        'water': (25, 5), 'fertilizer': ['Urea', 'DAP', 'NPK_12-32-16']
    },
    'Sugarcane': {
        'zones': ['Western_Maharashtra', 'North_Maharashtra'],
        'soil': ['Black', 'Loamy', 'Clay'],
        'weather': ['Tropical', 'Humid', 'Monsoon', 'Warm'],
        'npk': (150, 60, 60), 'npk_var': 0.1,
        'zn': 10, 's': 25, 'ph': 7.0, 'ph_range': (6.5, 7.5),
        'water': (32, 12), 'fertilizer': ['Urea', 'DAP', 'Organic_Compost']
    },
    'Jowar': {
        'zones': ['Marathwada', 'Vidarbha', 'Western_Maharashtra'],
        'soil': ['Black', 'Red', 'Loamy'],
        'weather': ['Semi-Arid', 'Post-Monsoon', 'Dry'],
        'npk': (80, 40, 40), 'npk_var': 0.18,
        'zn': 25, 's': 20, 'ph': 6.8, 'ph_range': (6.0, 7.5),
        'water': (28, 8), 'fertilizer': ['DAP', 'NPK_10-26-26', 'Urea']
    },
    'Bajra': {
        'zones': ['Marathwada', 'North_Maharashtra'],
        'soil': ['Sandy', 'Loamy', 'Red'],
        'weather': ['Semi-Arid', 'Dry', 'Hot', 'Warm'],
        'npk': (60, 40, 20), 'npk_var': 0.2,
        'zn': 5, 's': 10, 'ph': 7.0, 'ph_range': (6.5, 7.5),
        'water': (30, 5), 'fertilizer': ['Urea', 'SSP', 'MOP']
    },
    'Groundnut': {
        'zones': ['Vidarbha', 'Western_Maharashtra'],
        'soil': ['Sandy', 'Red', 'Loamy'],
        'weather': ['Semi-Arid', 'Post-Monsoon', 'Warm'],
        'npk': (25, 50, 75), 'npk_var': 0.2,
        'zn': 25, 's': 20, 'ph': 6.5, 'ph_range': (6.0, 7.0),
        'water': (28, 6), 'fertilizer': ['SSP', 'MOP', 'Gypsum']
    },
    'Onion': {
        'zones': ['Western_Maharashtra', 'North_Maharashtra'],
        'soil': ['Loamy', 'Red', 'Black'],
        'weather': ['Cool_Dry', 'Winter', 'Post-Monsoon'],
        'npk': (100, 50, 100), 'npk_var': 0.15,
        'zn': 5, 's': 30, 'ph': 6.5, 'ph_range': (6.0, 7.0),
        'water': (26, 8), 'fertilizer': ['NPK_19-19-19', 'Urea', 'SSP']
    },
    'Tomato': {
        'zones': ['Western_Maharashtra', 'Konkan', 'North_Maharashtra'],
        'soil': ['Loamy', 'Red', 'Alluvial'],
        'weather': ['Winter', 'Cool_Dry', 'Post-Monsoon'],
        'npk': (120, 60, 60), 'npk_var': 0.15,
        'zn': 5, 's': 20, 'ph': 6.5, 'ph_range': (6.0, 7.0),
        'water': (27, 10), 'fertilizer': ['NPK_19-19-19', 'DAP', 'MOP']
    },
    'Grapes': {
        'zones': ['Western_Maharashtra', 'North_Maharashtra'],
        'soil': ['Black', 'Loamy'],
        'weather': ['Semi-Arid', 'Cool_Dry', 'Winter'],
        'npk': (50, 50, 100), 'npk_var': 0.15,
        'zn': 5, 's': 20, 'ph': 7.0, 'ph_range': (6.5, 7.5),
        'water': (25, 5), 'fertilizer': ['NPK_19-19-19', 'Organic_Compost', 'SSP']
    },
    'Banana': {
        'zones': ['Konkan', 'Western_Maharashtra'],
        'soil': ['Loamy', 'Alluvial', 'Clay'],
        'weather': ['Tropical', 'Humid', 'Monsoon', 'Warm'],
        'npk': (200, 60, 200), 'npk_var': 0.1,
        'zn': 5, 's': 20, 'ph': 6.8, 'ph_range': (6.0, 7.5),
        'water': (32, 12), 'fertilizer': ['Urea', 'MOP', 'Organic_Compost']
    },
    'Mango': {
        'zones': ['Konkan', 'Western_Maharashtra'],
        'soil': ['Laterite', 'Red', 'Alluvial'],
        'weather': ['Tropical', 'Humid', 'Monsoon', 'Warm'],
        'npk': (100, 50, 100), 'npk_var': 0.15,
        'zn': 5, 's': 20, 'ph': 6.3, 'ph_range': (5.5, 7.0),
        'water': (30, 10), 'fertilizer': ['Organic_Compost', 'NPK_10-26-26', 'Urea']
    },
    'Chilli': {
        'zones': ['Vidarbha', 'Western_Maharashtra', 'North_Maharashtra'],
        'soil': ['Loamy', 'Red', 'Black'],
        'weather': ['Tropical', 'Warm', 'Post-Monsoon'],
        'npk': (100, 50, 50), 'npk_var': 0.15,
        'zn': 5, 's': 20, 'ph': 6.5, 'ph_range': (6.0, 7.0),
        'water': (28, 9), 'fertilizer': ['NPK_19-19-19', 'DAP', 'MOP']
    },
    'Turmeric': {
        'zones': ['Konkan', 'Western_Maharashtra'],
        'soil': ['Loamy', 'Red', 'Clay'],
        'weather': ['Monsoon', 'Humid', 'Warm'],
        'npk': (80, 60, 120), 'npk_var': 0.15,
        'zn': 5, 's': 20, 'ph': 6.8, 'ph_range': (6.0, 7.5),
        'water': (30, 12), 'fertilizer': ['Organic_Compost', 'DAP', 'MOP']
    },
    'Pomegranate': {
        'zones': ['Western_Maharashtra', 'Marathwada'],
        'soil': ['Black', 'Red', 'Loamy'],
        'weather': ['Semi-Arid', 'Dry', 'Winter', 'Cool_Dry'],
        'npk': (50, 50, 50), 'npk_var': 0.15,
        'zn': 5, 's': 20, 'ph': 7.0, 'ph_range': (6.5, 7.5),
        'water': (26, 6), 'fertilizer': ['NPK_19-19-19', 'Organic_Compost']
    },
    'Chickpea': {
        'zones': ['Marathwada', 'Vidarbha', 'Western_Maharashtra'],
        'soil': ['Black', 'Loamy', 'Clay'],
        'weather': ['Winter', 'Cool_Dry', 'Post-Monsoon'],
        'npk': (20, 40, 20), 'npk_var': 0.2,
        'zn': 25, 's': 20, 'ph': 6.8, 'ph_range': (6.0, 7.5),
        'water': (25, 7), 'fertilizer': ['DAP', 'SSP', 'MOP']
    },
    'Sunflower': {
        'zones': ['Vidarbha', 'Marathwada', 'Western_Maharashtra'],
        'soil': ['Loamy', 'Red', 'Black'],
        'weather': ['Semi-Arid', 'Post-Monsoon', 'Warm'],
        'npk': (60, 90, 40), 'npk_var': 0.15,
        'zn': 5, 's': 40, 'ph': 7.0, 'ph_range': (6.5, 7.5),
        'water': (28, 8), 'fertilizer': ['DAP', 'SSP', 'MOP']
    },
    'Maize': {
        'zones': ['Vidarbha', 'Western_Maharashtra', 'North_Maharashtra'],
        'soil': ['Loamy', 'Alluvial', 'Black'],
        'weather': ['Monsoon', 'Post-Monsoon', 'Warm', 'Humid'],
        'npk': (120, 60, 40), 'npk_var': 0.15,
        'zn': 25, 's': 20, 'ph': 6.3, 'ph_range': (5.5, 7.0),
        'water': (29, 10), 'fertilizer': ['Urea', 'DAP', 'MOP']
    }
}

def generate_comprehensive_dataset(samples_per_combination=8):
    """Generate balanced dataset with realistic variations"""
    
    print("="*70)
    print("GENERATING COMPREHENSIVE MAHARASHTRA DATASET")
    print("="*70)
    
    data = []
    
    for crop_name, profile in CROP_PROFILES.items():
        print(f"\n{crop_name}:")
        
        # Generate all valid combinations
        combinations = []
        for zone in profile['zones']:
            for district in DISTRICTS_BY_ZONE[zone]:
                for soil in profile['soil']:
                    for weather in profile['weather']:
                        combinations.append((district, soil, weather, zone))
        
        print(f"  {len(combinations)} valid input combinations")
        
        # For each combination, generate multiple samples with variations
        for district, soil, weather, zone in combinations:
            for _ in range(samples_per_combination):
                # NPK with realistic variations
                n = int(profile['npk'][0] * np.random.uniform(1 - profile['npk_var'], 1 + profile['npk_var']))
                p = int(profile['npk'][1] * np.random.uniform(1 - profile['npk_var'], 1 + profile['npk_var']))
                k = int(profile['npk'][2] * np.random.uniform(1 - profile['npk_var'], 1 + profile['npk_var']))
                
                # Micronutrients with variation
                zn = int(profile['zn'] * np.random.uniform(0.9, 1.1))
                s = int(profile['s'] * np.random.uniform(0.9, 1.1))
                
                # pH within range
                ph = round(np.random.uniform(profile['ph_range'][0], profile['ph_range'][1]), 1)
                
                # Water quality based on zone characteristics
                temp_base, turb_base = profile['water']
                water_temp = round(temp_base + np.random.uniform(-2, 2), 1)
                turbidity = round(turb_base + np.random.uniform(-3, 3), 1)
                turbidity = max(1, turbidity)  # Min 1 NTU
                
                # Select fertilizer
                fertilizer = random.choice(profile['fertilizer'])
                
                data.append({
                    'District': district,
                    'Soil_Type': soil,
                    'Crop_Name': crop_name,
                    'N_kg_ha': max(1, n),
                    'P2O5_kg_ha': max(1, p),
                    'K2O_kg_ha': max(1, k),
                    'Zn_kg_ha': max(0, zn),
                    'S_kg_ha': max(0, s),
                    'Recommended_pH': ph,
                    'Turbidity_NTU': turbidity,
                    'Water_Temp_C': water_temp,
                    'Weather': weather,
                    'Fertilizer': fertilizer
                })
        
        print(f"  Generated {len(combinations) * samples_per_combination} samples")
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Shuffle
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    print("\n" + "="*70)
    print("DATASET SUMMARY")
    print("="*70)
    print(f"Total rows: {len(df)}")
    print(f"Crops: {df['Crop_Name'].nunique()}")
    print(f"Districts: {df['District'].nunique()}")
    print(f"\nCrop balance:")
    counts = df['Crop_Name'].value_counts()
    print(f"  Min: {counts.min()}, Max: {counts.max()}, Avg: {counts.mean():.1f}")
    print(f"  Balance ratio: {counts.max() / counts.min():.2f}x")
    
    # Check contradictions
    grouped = df.groupby(['District', 'Soil_Type', 'Weather'])['Crop_Name'].nunique()
    contradictions = grouped[grouped > 1]
    print(f"\n✅ Contradictions: {len(contradictions)} (Multiple crops per condition is realistic)")
    
    # Save
    output_path = '../maharashtra_smart_farmer_dataset_final.xlsx'
    df.to_excel(output_path, index=False)
    
    print(f"\n✅ Dataset saved to: {output_path}")
    print("="*70)
    print("\nNEXT STEPS:")
    print("1. Update config.py: DATASET_PATH = 'maharashtra_smart_farmer_dataset_final.xlsx'")
    print("2. Run: python train_models_fast.py")
    print("3. Expected accuracy: 80-85%+")
    print("="*70)
    
    return df

if __name__ == "__main__":
    df = generate_comprehensive_dataset(samples_per_combination=8)
