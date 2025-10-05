"""
Data preprocessing and model training module
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, r2_score, mean_absolute_error
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
        print(f"\nColumns: {list(self.data.columns)}")
        print(f"\nSample data:\n{self.data.head()}")
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
    
    def load_encoders_scalers(self):
        """Load encoders and scalers"""
        encoder_path = os.path.join(MODEL_DIR, ENCODER_FILE)
        scaler_path = os.path.join(MODEL_DIR, SCALER_FILE)
        
        if os.path.exists(encoder_path) and os.path.exists(scaler_path):
            self.encoders = joblib.load(encoder_path)
            self.scalers = joblib.load(scaler_path)
            print("Encoders and scalers loaded!")
            return True
        return False


class CropRecommenderModel:
    """Crop Recommendation using Random Forest"""
    
    def __init__(self):
        self.model = None
        self.feature_columns = ['District', 'Soil_Type', 'Weather', 'Zone']
        
    def train(self, df, processor):
        """Train crop recommendation model"""
        print("\n" + "="*60)
        print("Training Crop Recommendation Model (Random Forest)")
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
            X_encoded, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )
        
        # Train Random Forest with hyperparameter tuning
        print("\nPerforming hyperparameter tuning...")
        param_grid = {
            'n_estimators': [100, 200],
            'max_depth': [15, 20, None],
            'min_samples_split': [2, 5],
            'min_samples_leaf': [1, 2]
        }
        
        rf = RandomForestClassifier(random_state=42)
        grid_search = GridSearchCV(rf, param_grid, cv=3, scoring='accuracy', n_jobs=-1)
        grid_search.fit(X_train, y_train)
        
        self.model = grid_search.best_estimator_
        print(f"Best parameters: {grid_search.best_params_}")
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\n✓ Crop Recommendation Model Accuracy: {accuracy*100:.2f}%")
        
        # Cross-validation score
        cv_scores = cross_val_score(self.model, X_encoded, y_encoded, cv=5)
        print(f"✓ Cross-validation accuracy: {cv_scores.mean()*100:.2f}% (+/- {cv_scores.std()*100:.2f}%)")
        
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
    
    def load_model(self):
        """Load the model"""
        model_path = os.path.join(MODEL_DIR, CROP_MODEL_FILE)
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
            return True
        return False


class NutrientPredictorModel:
    """Nutrient Prediction using MLP Neural Network"""
    
    def __init__(self):
        self.model = None
        self.feature_columns = ['District', 'Soil_Type', 'Crop_Name', 'Weather', 'Zone']
        self.target_columns = ['N_kg_ha', 'P2O5_kg_ha', 'K2O_kg_ha', 'Zn_kg_ha', 'S_kg_ha']
        
    def train(self, df, processor):
        """Train nutrient prediction model"""
        print("\n" + "="*60)
        print("Training Nutrient Prediction Model (MLP Neural Network)")
        print("="*60)
        
        # Add zone feature
        df = processor.add_zone_feature(df)
        
        # Prepare features and targets
        X = df[self.feature_columns].copy()
        y = df[self.target_columns].copy()
        
        # Encode features
        X_encoded = processor.encode_features(X, self.feature_columns, fit=False)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_encoded, y, test_size=0.2, random_state=42
        )
        
        # Scale features and targets
        scaler_X = StandardScaler()
        X_train_scaled = scaler_X.fit_transform(X_train)
        X_test_scaled = scaler_X.transform(X_test)
        
        scaler_y = StandardScaler()
        y_train_scaled = scaler_y.fit_transform(y_train)
        y_test_scaled = scaler_y.transform(y_test)
        
        # Store scalers
        processor.scalers['nutrient_X'] = scaler_X
        processor.scalers['nutrient_y'] = scaler_y
        
        # Train MLP Regressor
        print("\nTraining MLP Neural Network...")
        self.model = MLPRegressor(
            hidden_layer_sizes=(128, 64, 32),
            activation='relu',
            solver='adam',
            alpha=0.001,
            batch_size=32,
            learning_rate='adaptive',
            max_iter=1000,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.1
        )
        
        self.model.fit(X_train_scaled, y_train_scaled)
        
        # Evaluate
        y_pred_scaled = self.model.predict(X_test_scaled)
        y_pred = scaler_y.inverse_transform(y_pred_scaled)
        
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        
        print(f"\n✓ Nutrient Prediction Model R² Score: {r2:.4f}")
        print(f"✓ Mean Absolute Error: {mae:.2f}")
        
        # Individual nutrient R² scores
        print("\nIndividual Nutrient R² Scores:")
        for i, col in enumerate(self.target_columns):
            r2_individual = r2_score(y_test[col], y_pred[:, i])
            print(f"  {col}: {r2_individual:.4f}")
        
        return r2
    
    def save_model(self):
        """Save the model"""
        if not os.path.exists(MODEL_DIR):
            os.makedirs(MODEL_DIR)
        joblib.dump(self.model, os.path.join(MODEL_DIR, NUTRIENT_MODEL_FILE))
        print(f"Model saved to {NUTRIENT_MODEL_FILE}")
    
    def load_model(self):
        """Load the model"""
        model_path = os.path.join(MODEL_DIR, NUTRIENT_MODEL_FILE)
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
            return True
        return False


class WaterQualityPredictorModel:
    """Water Quality Prediction using Random Forest"""
    
    def __init__(self):
        self.model = None
        self.feature_columns = ['District', 'Weather', 'Soil_Type', 'Zone']
        self.target_columns = ['Recommended_pH', 'Turbidity_NTU', 'Water_Temp_C']
        
    def train(self, df, processor):
        """Train water quality prediction model"""
        print("\n" + "="*60)
        print("Training Water Quality Prediction Model (Random Forest)")
        print("="*60)
        
        # Add zone feature
        df = processor.add_zone_feature(df)
        
        # Prepare features and targets
        X = df[self.feature_columns].copy()
        y = df[self.target_columns].copy()
        
        # Encode features
        X_encoded = processor.encode_features(X, self.feature_columns, fit=False)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_encoded, y, test_size=0.2, random_state=42
        )
        
        # Train Random Forest Regressor
        print("\nTraining Random Forest Regressor...")
        self.model = RandomForestRegressor(
            n_estimators=200,
            max_depth=20,
            min_samples_split=2,
            min_samples_leaf=1,
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        
        print(f"\n✓ Water Quality Prediction Model R² Score: {r2:.4f}")
        print(f"✓ Mean Absolute Error: {mae:.2f}")
        
        # Individual parameter R² scores
        print("\nIndividual Parameter R² Scores:")
        for i, col in enumerate(self.target_columns):
            r2_individual = r2_score(y_test[col], y_pred[:, i])
            print(f"  {col}: {r2_individual:.4f}")
        
        return r2
    
    def save_model(self):
        """Save the model"""
        if not os.path.exists(MODEL_DIR):
            os.makedirs(MODEL_DIR)
        joblib.dump(self.model, os.path.join(MODEL_DIR, WATER_MODEL_FILE))
        print(f"Model saved to {WATER_MODEL_FILE}")
    
    def load_model(self):
        """Load the model"""
        model_path = os.path.join(MODEL_DIR, WATER_MODEL_FILE)
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
            return True
        return False


class FertilizerRecommenderModel:
    """Fertilizer Recommendation using Random Forest"""
    
    def __init__(self):
        self.model = None
        self.feature_columns = ['Crop_Name', 'Soil_Type', 'N_kg_ha', 'P2O5_kg_ha', 'K2O_kg_ha']
        
    def train(self, df, processor):
        """Train fertilizer recommendation model"""
        print("\n" + "="*60)
        print("Training Fertilizer Recommendation Model (Random Forest)")
        print("="*60)
        
        # Prepare features and target
        X = df[self.feature_columns].copy()
        y = df['Fertilizer'].copy()
        
        # Encode features
        X_encoded = processor.encode_features(X, ['Crop_Name', 'Soil_Type'], fit=False)
        
        # Encode target
        fertilizer_encoder = LabelEncoder()
        y_encoded = fertilizer_encoder.fit_transform(y)
        processor.encoders['Fertilizer'] = fertilizer_encoder
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_encoded, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )
        
        # Train Random Forest Classifier
        print("\nTraining Random Forest Classifier...")
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=20,
            min_samples_split=2,
            min_samples_leaf=1,
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\n✓ Fertilizer Recommendation Model Accuracy: {accuracy*100:.2f}%")
        
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
    
    def load_model(self):
        """Load the model"""
        model_path = os.path.join(MODEL_DIR, FERTILIZER_MODEL_FILE)
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
            return True
        return False


def train_all_models():
    """Train all models"""
    print("\n" + "="*70)
    print("SMART FARMER RECOMMENDER SYSTEM - MODEL TRAINING")
    print("Maharashtra Agricultural AI System")
    print("="*70)
    
    # Initialize processor
    processor = DataProcessor()
    
    # Load data
    df = processor.load_data()
    
    # Train Crop Recommender
    crop_model = CropRecommenderModel()
    crop_accuracy = crop_model.train(df, processor)
    crop_model.save_model()
    
    # Train Nutrient Predictor
    nutrient_model = NutrientPredictorModel()
    nutrient_r2 = nutrient_model.train(df, processor)
    nutrient_model.save_model()
    
    # Train Water Quality Predictor
    water_model = WaterQualityPredictorModel()
    water_r2 = water_model.train(df, processor)
    water_model.save_model()
    
    # Train Fertilizer Recommender
    fertilizer_model = FertilizerRecommenderModel()
    fertilizer_accuracy = fertilizer_model.train(df, processor)
    fertilizer_model.save_model()
    
    # Save encoders and scalers
    processor.save_encoders_scalers()
    
    # Summary
    print("\n" + "="*70)
    print("MODEL TRAINING COMPLETE - SUMMARY")
    print("="*70)
    print(f"✓ Crop Recommendation Accuracy: {crop_accuracy*100:.2f}%")
    print(f"✓ Nutrient Prediction R² Score: {nutrient_r2:.4f}")
    print(f"✓ Water Quality R² Score: {water_r2:.4f}")
    print(f"✓ Fertilizer Recommendation Accuracy: {fertilizer_accuracy*100:.2f}%")
    print(f"\nAll models saved in: {MODEL_DIR}")
    print("="*70)


if __name__ == "__main__":
    train_all_models()
