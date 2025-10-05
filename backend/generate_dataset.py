"""
Generate high-quality Maharashtra agricultural dataset with realistic patterns
"""

import pandas as pd
import numpy as np
from itertools import product
import random

# Maharashtra districts with zones
DISTRICTS_BY_ZONE = {
    'Western_Maharashtra': ['Pune', 'Satara', 'Sangli', 'Kolhapur', 'Solapur', 'Ahmednagar'],
    'Vidarbha': ['Nagpur', 'Amravati', 'Akola', 'Yavatmal', 'Wardha', 'Chandrapur', 'Gadchiroli', 'Gondia', 'Bhandara', 'Buldhana', 'Washim'],
    'Marathwada': ['Aurangabad', 'Jalna', 'Beed', 'Latur', 'Osmanabad', 'Nanded', 'Parbhani', 'Hingoli'],
    'Konkan': ['Mumbai City', 'Mumbai Suburban', 'Thane', 'Raigad', 'Ratnagiri', 'Sindhudurg'],
    'North_Maharashtra': ['Nashik', 'Dhule', 'Jalgaon', 'Nandurbar']
}

# Realistic crop-soil-weather mappings for Maharashtra
CROP_PROFILES = {
    'Cotton': {
        'soil': ['Black', 'Clay', 'Loamy'],
        'weather': ['Semi-Arid', 'Post-Monsoon', 'Dry'],
        'zones': ['Vidarbha', 'Marathwada', 'Western_Maharashtra'],
        'npk': (120, 60, 40), 'zn': 25, 's': 20, 'ph': (6.0, 7.5),
        'fertilizer': ['Urea', 'DAP', 'NPK_12-32-16']
    },
    'Soybean': {
        'soil': ['Black', 'Red', 'Loamy'],
        'weather': ['Monsoon', 'Humid', 'Post-Monsoon'],
        'zones': ['Vidarbha', 'Marathwada'],
        'npk': (30, 60, 40), 'zn': 5, 's': 20, 'ph': (6.5, 7.5),
        'fertilizer': ['DAP', 'NPK_10-26-26', 'SSP']
    },
    'Rice': {
        'soil': ['Clay', 'Alluvial', 'Loamy'],
        'weather': ['Monsoon', 'Humid', 'Tropical'],
        'zones': ['Konkan', 'Vidarbha'],
        'npk': (100, 50, 50), 'zn': 25, 's': 12, 'ph': (5.5, 6.5),
        'fertilizer': ['Urea', 'DAP', 'MOP']
    },
    'Wheat': {
        'soil': ['Loamy', 'Clay', 'Alluvial'],
        'weather': ['Winter', 'Cool_Dry', 'Post-Monsoon'],
        'zones': ['Western_Maharashtra', 'North_Maharashtra', 'Marathwada'],
        'npk': (120, 60, 40), 'zn': 25, 's': 20, 'ph': (6.5, 7.5),
        'fertilizer': ['Urea', 'DAP', 'NPK_12-32-16']
    },
    'Sugarcane': {
        'soil': ['Black', 'Loamy', 'Clay'],
        'weather': ['Tropical', 'Humid', 'Monsoon'],
        'zones': ['Western_Maharashtra', 'North_Maharashtra'],
        'npk': (150, 60, 60), 'zn': 10, 's': 25, 'ph': (6.5, 7.5),
        'fertilizer': ['Urea', 'DAP', 'Organic_Compost']
    },
    'Jowar': {
        'soil': ['Black', 'Red', 'Loamy'],
        'weather': ['Semi-Arid', 'Post-Monsoon', 'Dry'],
        'zones': ['Marathwada', 'Vidarbha', 'Western_Maharashtra'],
        'npk': (80, 40, 40), 'zn': 25, 's': 20, 'ph': (6.0, 7.5),
        'fertilizer': ['DAP', 'NPK_10-26-26', 'Urea']
    },
    'Bajra': {
        'soil': ['Sandy', 'Loamy', 'Red'],
        'weather': ['Semi-Arid', 'Dry', 'Hot'],
        'zones': ['Marathwada', 'North_Maharashtra'],
        'npk': (60, 40, 20), 'zn': 5, 's': 10, 'ph': (6.5, 7.5),
        'fertilizer': ['Urea', 'SSP', 'MOP']
    },
    'Groundnut': {
        'soil': ['Sandy', 'Red', 'Loamy'],
        'weather': ['Semi-Arid', 'Post-Monsoon', 'Warm'],
        'zones': ['Vidarbha', 'Western_Maharashtra'],
        'npk': (25, 50, 75), 'zn': 25, 's': 20, 'ph': (6.0, 7.0),
        'fertilizer': ['SSP', 'MOP', 'Gypsum']
    },
    'Onion': {
        'soil': ['Loamy', 'Red', 'Black'],
        'weather': ['Cool_Dry', 'Winter', 'Post-Monsoon'],
        'zones': ['Western_Maharashtra', 'North_Maharashtra'],
        'npk': (100, 50, 100), 'zn': 5, 's': 30, 'ph': (6.0, 7.0),
        'fertilizer': ['NPK_19-19-19', 'Urea', 'SSP']
    },
    'Tomato': {
        'soil': ['Loamy', 'Red', 'Alluvial'],
        'weather': ['Winter', 'Cool_Dry', 'Post-Monsoon'],
        'zones': ['Western_Maharashtra', 'Konkan', 'North_Maharashtra'],
        'npk': (120, 60, 60), 'zn': 5, 's': 20, 'ph': (6.0, 7.0),
        'fertilizer': ['NPK_19-19-19', 'DAP', 'MOP']
    },
    'Grapes': {
        'soil': ['Black', 'Loamy'],
        'weather': ['Semi-Arid', 'Cool_Dry', 'Winter'],
        'zones': ['Western_Maharashtra', 'North_Maharashtra'],
        'npk': (50, 50, 100), 'zn': 5, 's': 20, 'ph': (6.5, 7.5),
        'fertilizer': ['NPK_19-19-19', 'Organic_Compost', 'SSP']
    },
    'Banana': {
        'soil': ['Loamy', 'Alluvial', 'Clay'],
        'weather': ['Tropical', 'Humid', 'Monsoon'],
        'zones': ['Konkan', 'Western_Maharashtra'],
        'npk': (200, 60, 200), 'zn': 5, 's': 20, 'ph': (6.0, 7.5),
        'fertilizer': ['Urea', 'MOP', 'Organic_Compost']
    },
    'Mango': {
        'soil': ['Laterite', 'Red', 'Alluvial'],
        'weather': ['Tropical', 'Humid', 'Monsoon'],
        'zones': ['Konkan', 'Western_Maharashtra'],
        'npk': (100, 50, 100), 'zn': 5, 's': 20, 'ph': (5.5, 7.0),
        'fertilizer': ['Organic_Compost', 'NPK_10-26-26', 'Urea']
    },
    'Chilli': {
        'soil': ['Loamy', 'Red', 'Black'],
        'weather': ['Tropical', 'Warm', 'Post-Monsoon'],
        'zones': ['Vidarbha', 'Western_Maharashtra', 'North_Maharashtra'],
        'npk': (100, 50, 50), 'zn': 5, 's': 20, 'ph': (6.0, 7.0),
        'fertilizer': ['NPK_19-19-19', 'DAP', 'MOP']
    },
    'Turmeric': {
        'soil': ['Loamy', 'Red', 'Clay'],
        'weather': ['Monsoon', 'Humid', 'Warm'],
        'zones': ['Konkan', 'Western_Maharashtra'],
        'npk': (80, 60, 120), 'zn': 5, 's': 20, 'ph': (6.0, 7.5),
        'fertilizer': ['Organic_Compost', 'DAP', 'MOP']
    },
    'Pomegranate': {
        'soil': ['Black', 'Red', 'Loamy'],
        'weather': ['Semi-Arid', 'Dry', 'Winter'],
        'zones': ['Western_Maharashtra', 'Marathwada'],
        'npk': (50, 50, 50), 'zn': 5, 's': 20, 'ph': (6.5, 7.5),
        'fertilizer': ['NPK_19-19-19', 'Organic_Compost']
    },
    'Chickpea': {
        'soil': ['Black', 'Loamy', 'Clay'],
        'weather': ['Winter', 'Cool_Dry', 'Post-Monsoon'],
        'zones': ['Marathwada', 'Vidarbha', 'Western_Maharashtra'],
        'npk': (20, 40, 20), 'zn': 25, 's': 20, 'ph': (6.0, 7.5),
        'fertilizer': ['DAP', 'SSP', 'MOP']
    },
    'Sunflower': {
        'soil': ['Loamy', 'Red', 'Black'],
        'weather': ['Semi-Arid', 'Post-Monsoon', 'Warm'],
        'zones': ['Vidarbha', 'Marathwada', 'Western_Maharashtra'],
        'npk': (60, 90, 40), 'zn': 5, 's': 40, 'ph': (6.5, 7.5),
        'fertilizer': ['DAP', 'SSP', 'MOP']
    },
    'Maize': {
        'soil': ['Loamy', 'Alluvial', 'Black'],
        'weather': ['Monsoon', 'Post-Monsoon', 'Warm'],
        'zones': ['Vidarbha', 'Western_Maharashtra', 'North_Maharashtra'],
        'npk': (120, 60, 40), 'zn': 25, 's': 20, 'ph': (5.5, 7.0),
        'fertilizer': ['Urea', 'DAP', 'MOP']
    }
}

def generate_realistic_dataset(samples_per_crop=100):
    """Generate scientifically accurate dataset"""
    
    data = []
    
    for crop, profile in CROP_PROFILES.items():
        print(f"Generating {samples_per_crop} samples for {crop}...")
        
        for _ in range(samples_per_crop):
            # Select zone
            zone = random.choice(profile['zones'])
            
            # Select district from zone
            district = random.choice(DISTRICTS_BY_ZONE[zone])
            
            # Select compatible soil and weather
            soil = random.choice(profile['soil'])
            weather = random.choice(profile['weather'])
            
            # Add realistic variations to NPK (±15%)
            n = int(profile['npk'][0] * random.uniform(0.85, 1.15))
            p = int(profile['npk'][1] * random.uniform(0.85, 1.15))
            k = int(profile['npk'][2] * random.uniform(0.85, 1.15))
            zn = int(profile['zn'] * random.uniform(0.9, 1.1))
            s = int(profile['s'] * random.uniform(0.9, 1.1))
            
            # pH with variation
            ph = round(random.uniform(profile['ph'][0], profile['ph'][1]), 1)
            
            # Water quality parameters based on zone
            if zone == 'Konkan':
                turbidity = round(random.uniform(5, 15), 1)
                water_temp = round(random.uniform(28, 35), 1)
            elif zone in ['Vidarbha', 'Marathwada']:
                turbidity = round(random.uniform(8, 19), 1)
                water_temp = round(random.uniform(30, 38), 1)
            else:
                turbidity = round(random.uniform(2, 12), 1)
                water_temp = round(random.uniform(25, 33), 1)
            
            # Select fertilizer
            fertilizer = random.choice(profile['fertilizer'])
            
            data.append({
                'District': district,
                'Soil_Type': soil,
                'Crop_Name': crop,
                'N_kg_ha': n,
                'P2O5_kg_ha': p,
                'K2O_kg_ha': k,
                'Zn_kg_ha': zn,
                'S_kg_ha': s,
                'Recommended_pH': ph,
                'Turbidity_NTU': turbidity,
                'Water_Temp_C': water_temp,
                'Weather': weather,
                'Fertilizer': fertilizer
            })
    
    df = pd.DataFrame(data)
    
    # Shuffle
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    print(f"\n✅ Generated {len(df)} rows with {df['Crop_Name'].nunique()} crops")
    print(f"✅ Covering {df['District'].nunique()} districts")
    
    return df

def validate_dataset(df):
    """Validate dataset quality"""
    print("\n" + "="*70)
    print("VALIDATION REPORT")
    print("="*70)
    
    # Check balance
    crop_counts = df['Crop_Name'].value_counts()
    print(f"\n✅ Crop balance:")
    print(f"   Min: {crop_counts.min()}, Max: {crop_counts.max()}")
    print(f"   Ratio: {crop_counts.max() / crop_counts.min():.2f}x (should be <2x)")
    
    # Check contradictions
    grouping_cols = ['District', 'Soil_Type', 'Weather']
    grouped = df.groupby(grouping_cols)['Crop_Name'].nunique()
    multi_crops = grouped[grouped > 1]
    
    if len(multi_crops) > 0:
        print(f"\n⚠️  {len(multi_crops)} input combinations produce multiple crops")
        print("   This is REALISTIC - same conditions can grow different crops")
    else:
        print("\n✅ One-to-one input-output mapping")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    print("="*70)
    print("GENERATING HIGH-QUALITY MAHARASHTRA AGRICULTURAL DATASET")
    print("="*70)
    
    # Generate dataset (100 samples per crop = 1900 total)
    df = generate_realistic_dataset(samples_per_crop=100)
    
    # Validate
    validate_dataset(df)
    
    # Save
    output_path = '../maharashtra_smart_farmer_dataset_v2.xlsx'
    df.to_excel(output_path, index=False)
    
    print(f"\n✅ Dataset saved to: {output_path}")
    print("="*70)