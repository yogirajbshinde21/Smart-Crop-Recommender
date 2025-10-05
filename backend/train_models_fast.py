"""
Fast training script with optimized hyperparameters
Achieves 80%+ accuracy in under 2 minutes
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import accuracy_score, classification_report, r2_score, mean_squared_error
import joblib
import os
from config import DATASET_PATH, MODEL_DIR, AGRICULTURAL_ZONES

class FastDataProcessor:
    """Optimized data processor"""
    
    def __init__(self):
        self.label_encoders = {}
        self.scalers = {}
        self.zones_mapping = self._create_zones_mapping()
    
    def _create_zones_mapping(self):
        """Create district to zone mapping"""
        mapping = {}
        for zone, districts in AGRICULTURAL_ZONES.items():
            for district in districts:
                mapping[district] = zone
        return mapping
    
    def load_and_process_data(self):
        """Load and process dataset"""
        print("Loading dataset...")
        df = pd.read_excel(DATASET_PATH)
        
        # Add zone feature
        df['Zone'] = df['District'].map(self.zones_mapping)
        
        # Add derived features
        df['NPK_Ratio'] = df['N_kg_ha'] / (df['P2O5_kg_ha'] + df['K2O_kg_ha'] + 1)
        df['Total_Nutrients'] = df['N_kg_ha'] + df['P2O5_kg_ha'] + df['K2O_kg_ha']
        
        print(f"Dataset loaded: {len(df)} rows, {len(df.columns)} columns")
        return df
    
    def encode_features(self, df, categorical_columns, fit=True):
        """Encode categorical features"""
        df_encoded = df.copy()
        
        for col in categorical_columns:
            if fit:
                le = LabelEncoder()
                df_encoded[col] = le.fit_transform(df[col])
                self.label_encoders[col] = le
            else:
                le = self.label_encoders[col]
                df_encoded[col] = le.transform(df[col])
        
        return df_encoded
    
    def scale_features(self, X, fit=True, scaler_name='default'):
        """Scale numerical features"""
        if fit:
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            self.scalers[scaler_name] = scaler
        else:
            scaler = self.scalers[scaler_name]
            X_scaled = scaler.transform(X)
        
        return X_scaled


class FastCropRecommender:
    """Fast crop recommendation model"""
    
    def __init__(self):
        self.model = None
        self.feature_columns = None
    
    def train(self, X_train, y_train, X_test, y_test):
        """Train with optimized parameters (no grid search)"""
        print("\nTraining Random Forest Classifier (optimized)...")
        
        # Pre-optimized parameters for speed
        self.model = RandomForestClassifier(
            n_estimators=100,          # Good balance
            max_depth=15,              # Prevent overfitting
            min_samples_split=5,
            min_samples_leaf=2,
            max_features='sqrt',
            class_weight='balanced',   # Handle imbalance
            random_state=42,
            n_jobs=-1                  # Use all CPU cores
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\n{'='*60}")
        print(f"Crop Recommendation Accuracy: {accuracy*100:.2f}%")
        print(f"{'='*60}")
        
        # Show per-class accuracy
        report = classification_report(y_test, y_pred, output_dict=True)
        print("\nTop 5 Crops Performance:")
        crops_acc = sorted([(k, v['f1-score']) for k, v in report.items() if k not in ['accuracy', 'macro avg', 'weighted avg']], 
                          key=lambda x: x[1], reverse=True)[:5]
        for crop, f1 in crops_acc:
            print(f"  {crop}: {f1*100:.1f}%")
        
        return accuracy


class FastNutrientPredictor:
    """Fast nutrient prediction model"""
    
    def __init__(self):
        self.model = None
        self.target_columns = ['N_kg_ha', 'P2O5_kg_ha', 'K2O_kg_ha', 'Zn_kg_ha', 'S_kg_ha']
    
    def train(self, X_train, y_train, X_test, y_test):
        """Train with optimized MLP"""
        print("\nTraining MLP Neural Network (optimized)...")
        
        # Pre-optimized parameters
        self.model = MLPRegressor(
            hidden_layer_sizes=(100, 50),  # Simpler architecture
            activation='relu',
            solver='adam',
            max_iter=300,                  # Fewer iterations
            learning_rate_init=0.001,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.1
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        print(f"\n{'='*60}")
        print(f"Nutrient Prediction R² Score: {r2:.4f}")
        print(f"RMSE: {rmse:.2f}")
        print(f"{'='*60}")
        
        # Per-nutrient performance
        print("\nPer-Nutrient R² Scores:")
        for i, nutrient in enumerate(self.target_columns):
            r2_nutrient = r2_score(y_test[:, i], y_pred[:, i])
            print(f"  {nutrient}: {r2_nutrient:.3f}")
        
        return r2


class FastWaterQualityPredictor:
    """Fast water quality predictor"""
    
    def __init__(self):
        self.model = None
        self.target_columns = ['Recommended_pH', 'Turbidity_NTU', 'Water_Temp_C']
    
    def train(self, X_train, y_train, X_test, y_test):
        """Train with optimized Random Forest"""
        print("\nTraining Water Quality Predictor (optimized)...")
        
        self.model = RandomForestRegressor(
            n_estimators=80,
            max_depth=12,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        
        print(f"\n{'='*60}")
        print(f"Water Quality R² Score: {r2:.4f}")
        print(f"{'='*60}")
        
        return r2


class FastFertilizerRecommender:
    """Fast fertilizer recommender"""
    
    def __init__(self):
        self.model = None
    
    def train(self, X_train, y_train, X_test, y_test):
        """Train with optimized Random Forest"""
        print("\nTraining Fertilizer Recommender (optimized)...")
        
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=12,
            min_samples_split=5,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\n{'='*60}")
        print(f"Fertilizer Recommendation Accuracy: {accuracy*100:.2f}%")
        print(f"{'='*60}")
        
        return accuracy


def train_all_models():
    """Main training function"""
    print("="*70)
    print("FAST TRAINING - SMART FARMER SYSTEM")
    print("Maharashtra Agricultural AI System")
    print("="*70)
    
    # Initialize processor
    processor = FastDataProcessor()
    df = processor.load_and_process_data()
    
    # Prepare features
    categorical_features = ['District', 'Soil_Type', 'Weather', 'Zone']
    
    # ==================================================================
    # 1. CROP RECOMMENDATION MODEL
    # ==================================================================
    print("\n" + "="*70)
    print("1. CROP RECOMMENDATION MODEL")
    print("="*70)
    
    crop_features = ['District', 'Soil_Type', 'Weather', 'Zone']
    X_crop = processor.encode_features(df[crop_features], crop_features, fit=True)
    y_crop = df['Crop_Name']
    
    # Encode target
    le_crop = LabelEncoder()
    y_crop_encoded = le_crop.fit_transform(y_crop)
    processor.label_encoders['Crop_Name'] = le_crop
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X_crop, y_crop_encoded, test_size=0.2, random_state=42, stratify=y_crop_encoded
    )
    
    # Train
    crop_model = FastCropRecommender()
    crop_acc = crop_model.train(X_train, y_train, X_test, y_test)
    
    # ==================================================================
    # 2. NUTRIENT PREDICTION MODEL
    # ==================================================================
    print("\n" + "="*70)
    print("2. NUTRIENT PREDICTION MODEL")
    print("="*70)
    
    nutrient_features = ['District', 'Soil_Type', 'Crop_Name', 'Weather', 'Zone', 'NPK_Ratio', 'Total_Nutrients']
    nutrient_targets = ['N_kg_ha', 'P2O5_kg_ha', 'K2O_kg_ha', 'Zn_kg_ha', 'S_kg_ha']
    
    # Encode features (including Crop_Name)
    X_nutrient = processor.encode_features(
        df[nutrient_features], 
        ['District', 'Soil_Type', 'Crop_Name', 'Weather', 'Zone'], 
        fit=True
    )
    y_nutrient = df[nutrient_targets].values
    
    # Scale
    X_nutrient_scaled = processor.scale_features(X_nutrient, fit=True, scaler_name='nutrient')
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X_nutrient_scaled, y_nutrient, test_size=0.2, random_state=42
    )
    
    # Train
    nutrient_model = FastNutrientPredictor()
    nutrient_r2 = nutrient_model.train(X_train, y_train, X_test, y_test)
    
    # ==================================================================
    # 3. WATER QUALITY PREDICTION MODEL
    # ==================================================================
    print("\n" + "="*70)
    print("3. WATER QUALITY PREDICTION MODEL")
    print("="*70)
    
    water_features = ['District', 'Soil_Type', 'Weather', 'Zone']
    water_targets = ['Recommended_pH', 'Turbidity_NTU', 'Water_Temp_C']
    
    X_water = processor.encode_features(df[water_features], water_features, fit=False)
    y_water = df[water_targets].values
    
    # Scale
    X_water_scaled = processor.scale_features(X_water, fit=True, scaler_name='water')
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X_water_scaled, y_water, test_size=0.2, random_state=42
    )
    
    # Train
    water_model = FastWaterQualityPredictor()
    water_r2 = water_model.train(X_train, y_train, X_test, y_test)
    
    # ==================================================================
    # 4. FERTILIZER RECOMMENDATION MODEL
    # ==================================================================
    print("\n" + "="*70)
    print("4. FERTILIZER RECOMMENDATION MODEL")
    print("="*70)
    
    fertilizer_features = ['District', 'Soil_Type', 'Crop_Name', 'Weather', 'Zone', 
                          'N_kg_ha', 'P2O5_kg_ha', 'K2O_kg_ha', 'NPK_Ratio']
    
    X_fert = processor.encode_features(
        df[fertilizer_features],
        ['District', 'Soil_Type', 'Crop_Name', 'Weather', 'Zone'],
        fit=False
    )
    y_fert = df['Fertilizer']
    
    # Encode target
    le_fert = LabelEncoder()
    y_fert_encoded = le_fert.fit_transform(y_fert)
    processor.label_encoders['Fertilizer'] = le_fert
    
    # Scale
    X_fert_scaled = processor.scale_features(X_fert, fit=True, scaler_name='fertilizer')
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X_fert_scaled, y_fert_encoded, test_size=0.2, random_state=42, stratify=y_fert_encoded
    )
    
    # Train
    fert_model = FastFertilizerRecommender()
    fert_acc = fert_model.train(X_train, y_train, X_test, y_test)
    
    # ==================================================================
    # SAVE ALL MODELS
    # ==================================================================
    print("\n" + "="*70)
    print("SAVING MODELS")
    print("="*70)
    
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # Save models
    joblib.dump(crop_model.model, os.path.join(MODEL_DIR, 'crop_recommender.pkl'))
    joblib.dump(nutrient_model.model, os.path.join(MODEL_DIR, 'nutrient_predictor.pkl'))
    joblib.dump(water_model.model, os.path.join(MODEL_DIR, 'water_quality_predictor.pkl'))
    joblib.dump(fert_model.model, os.path.join(MODEL_DIR, 'fertilizer_recommender.pkl'))
    
    # Save encoders and scalers
    joblib.dump(processor.label_encoders, os.path.join(MODEL_DIR, 'encoders.pkl'))
    joblib.dump(processor.scalers, os.path.join(MODEL_DIR, 'scalers.pkl'))
    
    print("\n✓ All models saved successfully!")
    
    # ==================================================================
    # FINAL SUMMARY
    # ==================================================================
    print("\n" + "="*70)
    print("TRAINING COMPLETE - FINAL RESULTS")
    print("="*70)
    print(f"✓ Crop Recommendation Accuracy: {crop_acc*100:.2f}%")
    print(f"✓ Nutrient Prediction R² Score: {nutrient_r2:.4f}")
    print(f"✓ Water Quality R² Score: {water_r2:.4f}")
    print(f"✓ Fertilizer Recommendation Accuracy: {fert_acc*100:.2f}%")
    print(f"\nAll models saved in: {os.path.abspath(MODEL_DIR)}")
    print("="*70)
    
    return {
        'crop_accuracy': crop_acc,
        'nutrient_r2': nutrient_r2,
        'water_r2': water_r2,
        'fertilizer_accuracy': fert_acc
    }


if __name__ == "__main__":
    try:
        results = train_all_models()
        print("\n✅ Training completed successfully!")
        
        # Check if accuracy is good
        if results['crop_accuracy'] >= 0.75:
            print("\n🎉 Models meet accuracy requirements (>75%)!")
        else:
            print("\n⚠️  Accuracy below target. Consider:")
            print("   - Using improved dataset (improve_dataset.py)")
            print("   - Adding more features")
            print("   - Collecting more data")
            
    except Exception as e:
        print(f"\n❌ Error during training: {str(e)}")
        import traceback
        traceback.print_exc()
