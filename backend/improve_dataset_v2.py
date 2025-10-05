"""
Advanced dataset improvement with augmentation and balancing
"""

import pandas as pd
import numpy as np
from config import DATASET_PATH

def improve_dataset_advanced():
    """Remove contradictions AND augment data for better balance"""
    print("="*70)
    print("ADVANCED DATASET IMPROVEMENT")
    print("="*70)
    
    # Load dataset
    df = pd.read_excel(DATASET_PATH)
    print(f"\nOriginal: {len(df)} rows, {df['Crop_Name'].nunique()} crops")
    
    # ==================================================================
    # STEP 1: Remove contradictions - keep ALL instances of best crop
    # ==================================================================
    print("\n" + "="*70)
    print("STEP 1: Removing Contradictions (Keeping Multiple Samples)")
    print("="*70)
    
    input_cols = ['District', 'Soil_Type', 'Weather']
    
    # High-value crops get priority
    crop_priority = {
        'Sugarcane': 10, 'Grapes': 9, 'Pomegranate': 9, 'Banana': 8,
        'Mango': 8, 'Cotton': 7, 'Soybean': 7, 'Onion': 7,
        'Tomato': 6, 'Chilli': 6, 'Turmeric': 6, 'Sunflower': 5,
        'Wheat': 5, 'Rice': 5, 'Maize': 4, 'Groundnut': 4,
        'Chickpea': 3, 'Jowar': 3, 'Bajra': 2
    }
    
    improved_rows = []
    
    for name, group in df.groupby(input_cols):
        # Find most common crop
        crop_counts = group['Crop_Name'].value_counts()
        
        # If tied, use priority
        top_crops = crop_counts[crop_counts == crop_counts.max()].index.tolist()
        if len(top_crops) > 1:
            # Choose based on priority
            best_crop = max(top_crops, key=lambda x: crop_priority.get(x, 0))
        else:
            best_crop = top_crops[0]
        
        # Keep ALL rows with the best crop (not just one)
        best_samples = group[group['Crop_Name'] == best_crop]
        improved_rows.extend(best_samples.to_dict('records'))
    
    df_clean = pd.DataFrame(improved_rows)
    print(f"After cleaning: {len(df_clean)} rows")
    
    # Verify no contradictions
    grouped = df_clean.groupby(input_cols)['Crop_Name'].nunique()
    contradictions = grouped[grouped > 1]
    print(f"✅ Contradictions: {len(contradictions)} (should be 0)")
    
    # ==================================================================
    # STEP 2: Balance by augmentation
    # ==================================================================
    print("\n" + "="*70)
    print("STEP 2: Augmenting Minority Classes")
    print("="*70)
    
    crop_counts = df_clean['Crop_Name'].value_counts()
    target_count = int(crop_counts.quantile(0.75))  # 75th percentile as target
    
    print(f"Current range: {crop_counts.min()} - {crop_counts.max()}")
    print(f"Target samples per crop: {target_count}")
    
    augmented_rows = []
    
    for crop in df_clean['Crop_Name'].unique():
        crop_data = df_clean[df_clean['Crop_Name'] == crop]
        current = len(crop_data)
        
        # Add all existing
        augmented_rows.extend(crop_data.to_dict('records'))
        
        # Augment if below target
        if current < target_count:
            shortage = target_count - current
            print(f"  {crop}: {current} → {target_count} (+{shortage})")
            
            for _ in range(shortage):
                # Pick random sample
                base = crop_data.sample(n=1).iloc[0].to_dict()
                
                # Create augmented version with small variations
                aug = base.copy()
                
                # ±8% variation to NPK
                aug['N_kg_ha'] = max(1, int(base['N_kg_ha'] * np.random.uniform(0.92, 1.08)))
                aug['P2O5_kg_ha'] = max(1, int(base['P2O5_kg_ha'] * np.random.uniform(0.92, 1.08)))
                aug['K2O_kg_ha'] = max(1, int(base['K2O_kg_ha'] * np.random.uniform(0.92, 1.08)))
                aug['Zn_kg_ha'] = max(0, int(base['Zn_kg_ha'] * np.random.uniform(0.92, 1.08)))
                aug['S_kg_ha'] = max(0, int(base['S_kg_ha'] * np.random.uniform(0.92, 1.08)))
                
                # ±0.15 to pH
                aug['Recommended_pH'] = round(np.clip(base['Recommended_pH'] + np.random.uniform(-0.15, 0.15), 5.0, 8.5), 1)
                
                # Small variations to water quality
                aug['Turbidity_NTU'] = round(max(0, base['Turbidity_NTU'] + np.random.uniform(-1.5, 1.5)), 1)
                aug['Water_Temp_C'] = round(base['Water_Temp_C'] + np.random.uniform(-0.8, 0.8), 1)
                
                augmented_rows.append(aug)
    
    df_final = pd.DataFrame(augmented_rows)
    df_final = df_final.sample(frac=1, random_state=42).reset_index(drop=True)
    
    print(f"\n✅ Final dataset: {len(df_final)} rows")
    
    # ==================================================================
    # STEP 3: Verification
    # ==================================================================
    print("\n" + "="*70)
    print("STEP 3: Quality Check")
    print("="*70)
    
    final_counts = df_final['Crop_Name'].value_counts()
    print(f"Crop balance: {final_counts.min()} - {final_counts.max()}")
    print(f"Balance ratio: {final_counts.max() / final_counts.min():.2f}x")
    
    # Final contradiction check
    grouped = df_final.groupby(input_cols)['Crop_Name'].nunique()
    contradictions = grouped[grouped > 1]
    print(f"✅ Contradictions: {len(contradictions)}")
    
    print(f"✅ Missing values: {df_final.isnull().sum().sum()}")
    
    # ==================================================================
    # STEP 4: Save
    # ==================================================================
    output = DATASET_PATH.replace('.xlsx', '_v2_improved.xlsx')
    df_final.to_excel(output, index=False)
    
    print(f"\n✅ Saved to: {output}")
    print("\n" + "="*70)
    print("NEXT: Update config.py DATASET_PATH to use this file")
    print("Then run: python train_models_fast.py")
    print("Expected: 75-85% accuracy")
    print("="*70)
    
    return df_final

if __name__ == "__main__":
    improve_dataset_advanced()
