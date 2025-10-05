"""
New Training Script for Research-Based Dataset (10,000 rows)
Uses validation layer for scientific accuracy
Target: 85%+ accuracy with 0% regional constraint violations
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import accuracy_score, classification_report, r2_score, mean_squared_error
import joblib
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import DATASET_PATH, MODEL_DIR, AGRICULTURAL_ZONES
from validation import (
    validate_prediction, get_region, DISTRICT_TO_REGION,
    filter_invalid_crops, run_validation_tests
)

print("="*70)
print("MAHARASHTRA SMART FARMER - RESEARCH-BASED TRAINING")
print("Dataset: 10,000 rows with scientific crop-soil-district compatibility")
print("="*70)

# Run validation tests first
run_validation_tests()

class ResearchDataProcessor:
    """Process the new research-based dataset"""
    
    def __init__(self):
        self.label_encoders = {}
        self.scalers = {}
    
    def load_data(self):
        """Load CSV dataset"""
        print(f"\n{'='*70}")
        print("LOADING DATASET")
        print(f"{'='*70}")
        print(f"Path: {DATASET_PATH}")
        
        df = pd.read_csv(DATASET_PATH)
        
        print(f"✓ Loaded: {len(df)} rows, {len(df.columns)} columns")
        print(f"✓ Columns: {list(df.columns)}")
        print(f"✓ Districts: {df['District'].nunique()}")
        print(f"✓ Crops: {df['Crop_Name'].nunique()}")
        print(f"✓ Soil Types: {df['Soil_Type'].nunique()}")
        
        # Add zone
        df['Zone'] = df['District'].map(DISTRICT_TO_REGION)
        print(f"✓ Zone feature added")
        
        # Add derived features
        df['NPK_Ratio'] = df['N_kg_ha'] / (df['P2O5_kg_ha'] + df['K2O_kg_ha'] + 1)
        df['Total_Nutrients'] = df['N_kg_ha'] + df['P2O5_kg_ha'] + df['K2O_kg_ha']
        
        return df
    
    def encode_categorical(self, df, columns, fit=True):
        """Encode categorical columns"""
        df_encoded = df.copy()
        
        for col in columns:
            if col not in df.columns:
                continue
            
            if fit:
                le = LabelEncoder()
                df_encoded[col] = le.fit_transform(df[col].astype(str))
                self.label_encoders[col] = le
            else:
                le = self.label_encoders[col]
                df_encoded[col] = le.transform(df[col].astype(str))
        
        return df_encoded
    
    def scale_numerical(self, X, fit=True, scaler_name='default'):
        """Scale numerical features"""
        if fit:
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            self.scalers[scaler_name] = scaler
        else:
            scaler = self.scalers[scaler_name]
            X_scaled = scaler.transform(X)
        
        return X_scaled


def train_crop_model(processor, df):
    """Train crop recommendation model"""
    print(f"\n{'='*70}")
    print("TRAINING: CROP RECOMMENDATION MODEL")
    print(f"{'='*70}")
    
    # Features
    features = ['District', 'Soil_Type', 'Weather', 'Zone']
    target = 'Crop_Name'
    
    # Encode
    X = processor.encode_categorical(df[features], features, fit=True)
    y_encoded = processor.encode_categorical(df[[target]], [target], fit=True)
    y = y_encoded[target]
    
    # Store crop names for display
    crop_encoder = processor.label_encoders['Crop_Name']
    
    # Stratified split by district
    sss = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    for train_idx, test_idx in sss.split(X, df['District']):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
    
    # Train with more aggressive parameters for better accuracy
    model = RandomForestClassifier(
        n_estimators=300,           # More trees
        max_depth=20,               # Deeper trees
        min_samples_split=5,        # Allow more splits
        min_samples_leaf=2,         # Smaller leaf size
        max_features='sqrt',
        class_weight='balanced',
        random_state=42,
        n_jobs=-1,
        criterion='gini'
    )
    
    print(f"Training on {len(X_train)} samples...")
    # Convert to numpy arrays to avoid sklearn warning
    X_train_array = X_train.values if hasattr(X_train, 'values') else X_train
    y_train_array = y_train.values if hasattr(y_train, 'values') else y_train
    X_test_array = X_test.values if hasattr(X_test, 'values') else X_test
    y_test_array = y_test.values if hasattr(y_test, 'values') else y_test
    
    model.fit(X_train_array, y_train_array)
    
    # Evaluate
    y_pred = model.predict(X_test_array)
    accuracy = accuracy_score(y_test_array, y_pred)
    
    print(f"\n✓ ACCURACY: {accuracy*100:.2f}%")
    
    # Top crops performance with actual names
    report = classification_report(y_test_array, y_pred, output_dict=True, zero_division=0)
    crops = []
    for k, v in report.items():
        if k not in ['accuracy', 'macro avg', 'weighted avg']:
            try:
                crop_label = int(k)
                crop_name = crop_encoder.inverse_transform([crop_label])[0]
                f1 = v.get('f1-score', 0)
                support = v.get('support', 0)
                crops.append((crop_name, f1, support))
            except:
                pass
    
    crops.sort(key=lambda x: x[2], reverse=True)  # Sort by support
    
    print(f"\nTop 10 Crops by Sample Count:")
    for crop, f1, support in crops[:10]:
        print(f"  {crop:20s}: F1={f1*100:5.1f}% (samples={int(support)})")
    
    return model, accuracy


def train_nutrient_model(processor, df):
    """Train nutrient prediction model"""
    print(f"\n{'='*70}")
    print("TRAINING: NUTRIENT PREDICTION MODEL")
    print(f"{'='*70}")
    
    features = ['District', 'Soil_Type', 'Crop_Name', 'Weather', 'Zone', 'NPK_Ratio', 'Total_Nutrients']
    targets = ['N_kg_ha', 'P2O5_kg_ha', 'K2O_kg_ha', 'Zn_kg_ha', 'S_kg_ha']
    
    # Encode
    cat_cols = ['District', 'Soil_Type', 'Crop_Name', 'Weather', 'Zone']
    X = processor.encode_categorical(df[features], cat_cols, fit=False)
    y = df[targets].values
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X.values, y, test_size=0.2, random_state=42
    )
    
    # Scale
    X_train = processor.scale_numerical(X_train, fit=True, scaler_name='nutrient')
    X_test = processor.scale_numerical(X_test, fit=False, scaler_name='nutrient')
    
    # Train
    model = MLPRegressor(
        hidden_layer_sizes=(128, 64, 32),
        activation='relu',
        solver='adam',
        learning_rate='adaptive',
        max_iter=500,
        random_state=42,
        early_stopping=True,
        validation_fraction=0.15
    )
    
    print(f"Training on {len(X_train)} samples...")
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    print(f"\n✓ R² SCORE: {r2:.4f}")
    print(f"✓ RMSE: {rmse:.2f} kg/ha")
    
    # Per-nutrient
    print(f"\nPer-Nutrient Performance:")
    for i, nutrient in enumerate(targets):
        r2_n = r2_score(y_test[:, i], y_pred[:, i])
        print(f"  {nutrient:15s}: R²={r2_n:.3f}")
    
    return model, r2


def train_water_model(processor, df):
    """Train water quality model"""
    print(f"\n{'='*70}")
    print("TRAINING: WATER QUALITY MODEL")
    print(f"{'='*70}")
    
    features = ['District', 'Soil_Type', 'Crop_Name', 'Weather', 'Zone']
    targets = ['Recommended_pH', 'Turbidity_NTU', 'Water_Temp_C']
    
    # Encode
    cat_cols = ['District', 'Soil_Type', 'Crop_Name', 'Weather', 'Zone']
    X = processor.encode_categorical(df[features], cat_cols, fit=False)
    y = df[targets].values
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X.values, y, test_size=0.2, random_state=42
    )
    
    # Train
    model = RandomForestRegressor(
        n_estimators=150,
        max_depth=15,
        min_samples_split=8,
        random_state=42,
        n_jobs=-1
    )
    
    print(f"Training on {len(X_train)} samples...")
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\n✓ R² SCORE: {r2:.4f}")
    
    return model, r2


def train_fertilizer_model(processor, df):
    """Train fertilizer recommendation model"""
    print(f"\n{'='*70}")
    print("TRAINING: FERTILIZER RECOMMENDATION MODEL")
    print(f"{'='*70}")
    
    features = ['District', 'Soil_Type', 'Crop_Name', 'Weather', 'Zone', 
                'N_kg_ha', 'P2O5_kg_ha', 'K2O_kg_ha']
    target = 'Fertilizer'
    
    # Encode categorical columns (fit=True for new columns like Fertilizer)
    cat_cols = ['District', 'Soil_Type', 'Crop_Name', 'Weather', 'Zone', 'Fertilizer']
    X_and_y = processor.encode_categorical(df[features + [target]], cat_cols, fit=True)
    
    X = X_and_y[features]
    y = X_and_y[target]
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X.values, y.values, test_size=0.2, random_state=42
    )
    
    # Train
    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=12,
        min_samples_split=8,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    
    print(f"Training on {len(X_train)} samples...")
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n✓ ACCURACY: {accuracy*100:.2f}%")
    
    return model, accuracy


def main():
    """Main training pipeline"""
    
    # Initialize processor
    processor = ResearchDataProcessor()
    
    # Load data
    df = processor.load_data()
    
    # Train all models
    crop_model, crop_acc = train_crop_model(processor, df)
    nutrient_model, nutrient_r2 = train_nutrient_model(processor, df)
    water_model, water_r2 = train_water_model(processor, df)
    fert_model, fert_acc = train_fertilizer_model(processor, df)
    
    # Save models
    print(f"\n{'='*70}")
    print("SAVING MODELS")
    print(f"{'='*70}")
    
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    joblib.dump(crop_model, os.path.join(MODEL_DIR, 'crop_recommender.pkl'))
    joblib.dump(nutrient_model, os.path.join(MODEL_DIR, 'nutrient_predictor.pkl'))
    joblib.dump(water_model, os.path.join(MODEL_DIR, 'water_quality_predictor.pkl'))
    joblib.dump(fert_model, os.path.join(MODEL_DIR, 'fertilizer_recommender.pkl'))
    joblib.dump(processor.label_encoders, os.path.join(MODEL_DIR, 'encoders.pkl'))
    joblib.dump(processor.scalers, os.path.join(MODEL_DIR, 'scalers.pkl'))
    
    print("✓ All models saved!")
    
    # Final summary
    print(f"\n{'='*70}")
    print("TRAINING COMPLETE - SUMMARY")
    print(f"{'='*70}")
    print(f"Crop Recommendation:    {crop_acc*100:6.2f}%")
    print(f"Nutrient Prediction:    {nutrient_r2:6.4f} R²")
    print(f"Water Quality:          {water_r2:6.4f} R²")
    print(f"Fertilizer:             {fert_acc*100:6.2f}%")
    print(f"{'='*70}")
    print("\n✓ Ready for deployment!")
    print("  Run: python app.py")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
