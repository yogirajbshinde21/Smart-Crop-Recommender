"""
Enhanced training with advanced techniques for 85%+ accuracy
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, r2_score, mean_absolute_error
from sklearn.utils.class_weight import compute_sample_weight
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

from config import (
    DATASET_PATH, MODEL_DIR, CROP_MODEL_FILE, NUTRIENT_MODEL_FILE,
    WATER_MODEL_FILE, FERTILIZER_MODEL_FILE, ENCODER_FILE, SCALER_FILE,
    AGRICULTURAL_ZONES
)


class DataProcessor:
    """Handle data loading and preprocessing"""
    
    def __init__(self):
        self.encoders = {}
        self.scalers = {}
        self.data = None
        
    def load_data(self):
        """Load the Maharashtra farmer dataset"""
        print("Loading dataset...")
        self.data = pd.read_excel(DATASET_PATH)
        print(f"Dataset loaded: {self.data.shape[0]} rows, {self.data.shape[1]} columns")
        return self.data
    
    def add_zone_feature(self, df):
        """Add agricultural zone based on district"""
        def get_zone(district):
            for zone, districts in AGRICULTURAL_ZONES.items():
                if district in districts:
                    return zone
            return 'Other'
        
        df['Zone'] = df['District'].apply(get_zone)
        return df
    
    def encode_features(self, df, columns, fit=True):
        """Encode categorical features"""
        df_encoded = df.copy()
        
        for col in columns:
            if col in df_encoded.columns:
                if fit:
                    self.encoders[col] = LabelEncoder()
                    df_encoded[col] = self.encoders[col].fit_transform(df_encoded[col].astype(str))
                else:
                    if col in self.encoders:
                        df_encoded[col] = self.encoders[col].transform(df_encoded[col].astype(str))
        
        return df_encoded
    
    def scale_features(self, df, columns, fit=True):
        """Scale numerical features"""
        df_scaled = df.copy()
        
        for col in columns:
            if col in df_scaled.columns:
                if fit:
                    self.scalers[col] = StandardScaler()
                    df_scaled[col] = self.scalers[col].fit_transform(df_scaled[[col]])
                else:
                    if col in self.scalers:
                        df_scaled[col] = self.scalers[col].transform(df_scaled[[col]])
        
        return df_scaled
    
    def save_encoders_scalers(self):
        """Save encoders and scalers"""
        if not os.path.exists(MODEL_DIR):
            os.makedirs(MODEL_DIR)
        
        joblib.dump(self.encoders, os.path.join(MODEL_DIR, ENCODER_FILE))
        joblib.dump(self.scalers, os.path.join(MODEL_DIR, SCALER_FILE))
        print("Encoders and scalers saved!")


class EnhancedCropRecommender:
    """Enhanced Crop Recommendation with feature engineering"""
    
    def __init__(self):
        self.model = None
        # Add derived features for better predictions
        self.feature_columns = ['District', 'Soil_Type', 'Weather', 'Zone', 'pH_Category']
        
    def train(self, df, processor):
        """Train enhanced crop recommendation model"""
        print("\n" + "="*60)
        print("Training ENHANCED Crop Recommendation Model")
        print("="*60)
        
        # Add zone feature
        df = processor.add_zone_feature(df)
        
        # Prepare features and target
        X = df[self.feature_columns].copy()
        y = df['Crop_Name'].copy()
        
        # Encode features
        X_encoded = processor.encode_features(X, self.feature_columns, fit=True)
        y_encoder = LabelEncoder()
        y_encoded = y_encoder.fit_transform(y)
        
        # Store crop encoder
        processor.encoders['Crop_Name'] = y_encoder
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_encoded, y_encoded, test_size=0.2, random_state=42
        )
        
        # Compute sample weights for balanced training
        sample_weights = compute_sample_weight('balanced', y_train)
        print(f"\nUsing balanced class weights for training...")
        
        # Train with Gradient Boosting (usually better than RF)
        print("\nTraining Gradient Boosting Classifier...")
        
        param_grid = {
            'n_estimators': [150, 200, 250],
            'max_depth': [7, 10, 15],
            'learning_rate': [0.05, 0.1],
            'min_samples_split': [5, 10],
            'min_samples_leaf': [2, 4]
        }
        
        gb = GradientBoostingClassifier(random_state=42)
        grid_search = GridSearchCV(gb, param_grid, cv=3, scoring='accuracy', n_jobs=-1, verbose=1)
        grid_search.fit(X_train, y_train, sample_weight=sample_weights)
        
        self.model = grid_search.best_estimator_
        print(f"\nBest parameters: {grid_search.best_params_}")
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\n✓ ENHANCED Crop Recommendation Accuracy: {accuracy*100:.2f}%")
        
        # Cross-validation on original data
        X_encoded_orig = processor.encode_features(df[self.feature_columns], self.feature_columns, fit=False)
        y_encoded_orig = y_encoder.transform(df['Crop_Name'])
        cv_scores = cross_val_score(self.model, X_encoded_orig, y_encoded_orig, cv=5)
        print(f"✓ Cross-validation on original data: {cv_scores.mean()*100:.2f}% (+/- {cv_scores.std()*100:.2f}%)")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        print(f"\nFeature Importance:\n{feature_importance}")
        
        return accuracy
    
    def save_model(self):
        """Save the model"""
        if not os.path.exists(MODEL_DIR):
            os.makedirs(MODEL_DIR)
        joblib.dump(self.model, os.path.join(MODEL_DIR, CROP_MODEL_FILE))
        print(f"Model saved to {CROP_MODEL_FILE}")


class EnhancedNutrientPredictor:
    """Enhanced Nutrient Predictor with feature engineering"""
    
    def __init__(self):
        self.model = None
        self.feature_columns = ['District', 'Soil_Type', 'Crop_Name', 'Weather', 'Zone', 'pH_Category']
        self.target_columns = ['N_kg_ha', 'P2O5_kg_ha', 'K2O_kg_ha', 'Zn_kg_ha', 'S_kg_ha']
        
    def train(self, df, processor):
        """Train enhanced nutrient prediction model"""
        print("\n" + "="*60)
        print("Training ENHANCED Nutrient Prediction Model")
        print("="*60)
        
        # Add zone feature
        df = processor.add_zone_feature(df)
        
        # Prepare features and target
        X = df[self.feature_columns].copy()
        y = df[self.target_columns].copy()
        
        # Encode features
        X_encoded = processor.encode_features(X, self.feature_columns, fit=False)
        
        # Scale target variables for better training
        y_scaled = processor.scale_features(y, self.target_columns, fit=True)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_encoded, y_scaled, test_size=0.2, random_state=42
        )
        
        # Train Gradient Boosting Regressor (better for multi-output)
        print("\nTraining Gradient Boosting Regressor...")
        
        from sklearn.multioutput import MultiOutputRegressor
        
        gb_regressor = GradientBoostingRegressor(
            n_estimators=200,
            max_depth=7,
            learning_rate=0.1,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        
        self.model = MultiOutputRegressor(gb_regressor, n_jobs=-1)
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        
        print(f"\n✓ ENHANCED Nutrient Prediction R² Score: {r2:.4f}")
        print(f"✓ Mean Absolute Error: {mae:.2f}")
        
        # Individual R² scores
        print("\nIndividual Nutrient R² Scores:")
        for i, col in enumerate(self.target_columns):
            r2_individual = r2_score(y_test[:, i], y_pred[:, i])
            print(f"  {col}: {r2_individual:.4f}")
        
        return r2
    
    def save_model(self):
        """Save the model"""
        if not os.path.exists(MODEL_DIR):
            os.makedirs(MODEL_DIR)
        joblib.dump(self.model, os.path.join(MODEL_DIR, NUTRIENT_MODEL_FILE))
        print(f"Model saved to {NUTRIENT_MODEL_FILE}")


class EnhancedFertilizerRecommender:
    """Enhanced Fertilizer Recommender"""
    
    def __init__(self):
        self.model = None
        self.feature_columns = ['Crop_Name', 'Soil_Type', 'N_kg_ha', 'P2O5_kg_ha', 'K2O_kg_ha', 'pH_Category']
        
    def train(self, df, processor):
        """Train enhanced fertilizer recommendation model"""
        print("\n" + "="*60)
        print("Training ENHANCED Fertilizer Recommendation Model")
        print("="*60)
        
        # Prepare features and target
        X = df[self.feature_columns].copy()
        y = df['Fertilizer'].copy()
        
        # Encode categorical features
        cat_features = ['Crop_Name', 'Soil_Type', 'pH_Category']
        X_encoded = processor.encode_features(X, cat_features, fit=False)
        
        # Scale numerical features
        num_features = ['N_kg_ha', 'P2O5_kg_ha', 'K2O_kg_ha']
        X_scaled = processor.scale_features(X_encoded, num_features, fit=False)
        
        # Encode target
        y_encoder = LabelEncoder()
        y_encoded = y_encoder.fit_transform(y)
        processor.encoders['Fertilizer'] = y_encoder
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y_encoded, test_size=0.2, random_state=42
        )
        
        # Compute sample weights
        sample_weights = compute_sample_weight('balanced', y_train)
        print("\nUsing balanced class weights...")
        
        # Train Gradient Boosting
        print("\nTraining Gradient Boosting Classifier...")
        
        self.model = GradientBoostingClassifier(
            n_estimators=200,
            max_depth=10,
            learning_rate=0.1,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        
        self.model.fit(X_train, y_train, sample_weight=sample_weights)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\n✓ ENHANCED Fertilizer Recommendation Accuracy: {accuracy*100:.2f}%")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        print(f"\nFeature Importance:\n{feature_importance}")
        
        return accuracy
    
    def save_model(self):
        """Save the model"""
        if not os.path.exists(MODEL_DIR):
            os.makedirs(MODEL_DIR)
        joblib.dump(self.model, os.path.join(MODEL_DIR, FERTILIZER_MODEL_FILE))
        print(f"Model saved to {FERTILIZER_MODEL_FILE}")


def train_all_models():
    """Train all models with enhanced techniques"""
    print("="*70)
    print("ENHANCED SMART FARMER SYSTEM - MODEL TRAINING")
    print("Maharashtra Agricultural AI System v2.0")
    print("="*70)
    
    # Initialize processor
    processor = DataProcessor()
    df = processor.load_data()
    
    # Train models
    results = {}
    
    # 1. Crop Recommender
    crop_model = EnhancedCropRecommender()
    results['crop_accuracy'] = crop_model.train(df, processor)
    crop_model.save_model()
    
    # 2. Nutrient Predictor
    nutrient_model = EnhancedNutrientPredictor()
    results['nutrient_r2'] = nutrient_model.train(df, processor)
    nutrient_model.save_model()
    
    # 3. Fertilizer Recommender
    fertilizer_model = EnhancedFertilizerRecommender()
    results['fertilizer_accuracy'] = fertilizer_model.train(df, processor)
    fertilizer_model.save_model()
    
    # Save encoders and scalers
    processor.save_encoders_scalers()
    
    # Summary
    print("\n" + "="*70)
    print("ENHANCED MODEL TRAINING COMPLETE - SUMMARY")
    print("="*70)
    print(f"✓ Crop Recommendation Accuracy: {results['crop_accuracy']*100:.2f}%")
    print(f"✓ Nutrient Prediction R² Score: {results['nutrient_r2']:.4f}")
    print(f"✓ Fertilizer Recommendation Accuracy: {results['fertilizer_accuracy']*100:.2f}%")
    print(f"\nAll models saved in: {MODEL_DIR}")
    print("="*70)


if __name__ == "__main__":
    train_all_models()
