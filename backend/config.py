"""
Configuration file for Smart Farmer Recommender System
"""

import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data paths
DATA_DIR = os.path.join(BASE_DIR, 'data')
# Updated to use realistic dataset (multi-crop, proper confidence distribution)
DATASET_PATH = os.path.join(BASE_DIR, '..', 'maharashtra_agricultural_dataset_realistic.csv')
MODEL_DIR = os.path.join(BASE_DIR, 'models')

# Model filenames
CROP_MODEL_FILE = 'crop_recommender.pkl'
NUTRIENT_MODEL_FILE = 'nutrient_predictor.pkl'
WATER_MODEL_FILE = 'water_quality_predictor.pkl'
FERTILIZER_MODEL_FILE = 'fertilizer_recommender.pkl'
ENCODER_FILE = 'encoders.pkl'
SCALER_FILE = 'scalers.pkl'

# Maharashtra Agricultural Zones (All 36 districts)
AGRICULTURAL_ZONES = {
    'Konkan': ['Thane', 'Palghar', 'Raigad', 'Ratnagiri', 'Sindhudurg', 'Mumbai City', 'Mumbai Suburban'],
    'Vidarbha': ['Nagpur', 'Amravati', 'Akola', 'Yavatmal', 'Buldhana', 'Washim', 'Wardha', 'Chandrapur', 'Bhandara', 'Gadchiroli', 'Gondia'],
    'Marathwada': ['Aurangabad', 'Jalna', 'Beed', 'Latur', 'Osmanabad', 'Nanded', 'Parbhani', 'Hingoli'],
    'Western_Maharashtra': ['Pune', 'Satara', 'Sangli', 'Kolhapur', 'Solapur'],
    'North_Maharashtra': ['Nashik', 'Dhule', 'Jalgaon', 'Nandurbar', 'Ahmednagar']
}

# Zone characteristics
ZONE_CHARACTERISTICS = {
    'Konkan': {
        'climate': 'Coastal, High rainfall',
        'major_crops': ['Rice', 'Coconut', 'Mango', 'Cashew'],
        'soil_types': ['Laterite', 'Clay', 'Red'],
        'rainfall': 'Heavy (2000-4000mm)',
        'irrigation': 'Good natural water availability'
    },
    'Vidarbha': {
        'climate': 'Semi-arid to moderate',
        'major_crops': ['Cotton', 'Soybean', 'Pigeon Pea', 'Wheat'],
        'soil_types': ['Black', 'Clay'],
        'rainfall': 'Moderate (800-1200mm)',
        'irrigation': 'Canal and well irrigation'
    },
    'Marathwada': {
        'climate': 'Semi-arid, drought-prone',
        'major_crops': ['Sorghum', 'Pearl Millet', 'Cotton', 'Pulses'],
        'soil_types': ['Black', 'Red', 'Sandy'],
        'rainfall': 'Low to moderate (600-900mm)',
        'irrigation': 'Limited, drought-prone'
    },
    'Western Maharashtra': {
        'climate': 'Moderate to semi-arid',
        'major_crops': ['Sugarcane', 'Grapes', 'Pomegranate', 'Wheat'],
        'soil_types': ['Black', 'Red', 'Alluvial'],
        'rainfall': 'Moderate (600-1200mm)',
        'irrigation': 'Canal irrigation available'
    },
    'North Maharashtra': {
        'climate': 'Moderate',
        'major_crops': ['Cotton', 'Wheat', 'Sorghum', 'Banana'],
        'soil_types': ['Black', 'Alluvial'],
        'rainfall': 'Moderate (700-1000mm)',
        'irrigation': 'Canal and well irrigation'
    }
}

# Maharashtra Market Rates (Rs/Quintal - Approximate)
MARKET_RATES = {
    'Cotton': 6500,
    'Soybean': 4200,
    'Rice': 3500,
    'Wheat': 2500,
    'Sugarcane': 300,
    'Sorghum': 3000,
    'Pearl Millet': 2800,
    'Maize': 2200,
    'Chickpea': 5500,
    'Pigeon Pea': 6000,
    'Green Gram': 7500,
    'Black Gram': 7000,
    'Groundnut': 6000,
    'Sunflower': 6500,
    'Grapes': 8000,
    'Pomegranate': 9000,
    'Banana': 1500,
    'Mango': 4000,
    'Coconut': 2500
}

# Input cost estimates (Rs/hectare)
INPUT_COSTS = {
    'Seeds': {
        'Cotton': 4000,
        'Soybean': 3000,
        'Rice': 2500,
        'Wheat': 2000,
        'Sugarcane': 25000,
        'Sorghum': 1500,
        'Pearl Millet': 1500,
        'Maize': 2000,
        'Chickpea': 3000,
        'Pigeon Pea': 2500,
        'Green Gram': 3500,
        'Black Gram': 3500,
        'Groundnut': 4000,
        'Sunflower': 3000,
        'Grapes': 100000,
        'Pomegranate': 80000,
        'Banana': 50000,
        'Mango': 60000,
        'Coconut': 40000
    },
    'Fertilizer': {
        'DAP': 1400,
        'Urea': 800,
        'NPK 10-26-26': 1200,
        'NPK 12-32-16': 1300,
        'NPK 20-20-20': 1100,
        'NPK 19-19-19': 1100,
        'Organic Compost': 600,
        'Vermicompost': 800,
        'Bio-Fertilizer': 500,
        'Liquid Fertilizer': 1500
    },
    'Labor': 15000,
    'Irrigation': 8000,
    'Pesticides': 5000
}

# Expected yields (Quintal/hectare)
EXPECTED_YIELDS = {
    'Cotton': 18,
    'Soybean': 25,
    'Rice': 40,
    'Wheat': 35,
    'Sugarcane': 800,
    'Sorghum': 30,
    'Pearl Millet': 25,
    'Maize': 45,
    'Chickpea': 20,
    'Pigeon Pea': 18,
    'Green Gram': 12,
    'Black Gram': 12,
    'Groundnut': 28,
    'Sunflower': 20,
    'Grapes': 200,
    'Pomegranate': 150,
    'Banana': 400,
    'Mango': 80,
    'Coconut': 100
}

# ============================================================================
# CROP SUITABILITY AND DISTRICT-WISE TRADITIONAL CROPS
# ============================================================================
# Based on Maharashtra Krishi Vibhag (Agricultural Department) data
# This data is used for post-prediction validation and warnings only
# Does NOT affect ML model predictions or training

# District-wise traditional crops
DISTRICT_TRADITIONAL_CROPS = {
    # Konkan Zone - High rainfall coastal region
    'Thane': ['Rice', 'Coconut', 'Mango', 'Vegetables'],
    'Palghar': ['Rice', 'Coconut', 'Mango'],
    'Raigad': ['Rice', 'Coconut', 'Mango'],
    'Ratnagiri': ['Rice', 'Coconut', 'Mango'],
    'Sindhudurg': ['Rice', 'Coconut', 'Mango'],
    'Mumbai City': ['Vegetables'],
    'Mumbai Suburban': ['Vegetables'],
    
    # Vidarbha Zone - Cotton belt
    'Nagpur': ['Cotton', 'Soybean', 'Pigeon Pea', 'Rice'],
    'Amravati': ['Cotton', 'Soybean', 'Wheat', 'Chickpea', 'Pigeon Pea'],
    'Akola': ['Cotton', 'Soybean', 'Pigeon Pea', 'Wheat'],
    'Yavatmal': ['Cotton', 'Soybean', 'Pigeon Pea', 'Sorghum'],
    'Buldhana': ['Cotton', 'Soybean', 'Pearl Millet', 'Wheat', 'Banana'],
    'Washim': ['Cotton', 'Soybean', 'Pigeon Pea', 'Pomegranate'],
    'Wardha': ['Cotton', 'Sorghum', 'Wheat', 'Pigeon Pea'],
    'Chandrapur': ['Cotton', 'Soybean', 'Rice', 'Pigeon Pea'],
    'Bhandara': ['Rice', 'Soybean', 'Pigeon Pea', 'Wheat'],
    'Gadchiroli': ['Rice', 'Pigeon Pea', 'Maize'],
    'Gondia': ['Rice', 'Soybean', 'Pigeon Pea'],
    
    # Marathwada Zone - Drought-prone, low irrigation
    'Aurangabad': ['Sorghum', 'Pearl Millet', 'Cotton', 'Pigeon Pea', 'Chickpea'],
    'Jalna': ['Sorghum', 'Cotton', 'Pigeon Pea', 'Wheat'],
    'Beed': ['Sorghum', 'Pearl Millet', 'Cotton', 'Pigeon Pea', 'Chickpea'],
    'Latur': ['Sorghum', 'Pearl Millet', 'Pigeon Pea', 'Chickpea'],
    'Osmanabad': ['Sorghum', 'Pearl Millet', 'Cotton', 'Pigeon Pea'],
    'Nanded': ['Sorghum', 'Cotton', 'Pigeon Pea', 'Rice', 'Wheat'],
    'Parbhani': ['Cotton', 'Sorghum', 'Pigeon Pea', 'Chickpea'],
    'Hingoli': ['Cotton', 'Sorghum', 'Pearl Millet', 'Pigeon Pea'],
    
    # Western Maharashtra - Irrigation available, high-value crops
    'Pune': ['Sugarcane', 'Grapes', 'Wheat', 'Vegetables', 'Pomegranate'],
    'Satara': ['Sugarcane', 'Grapes', 'Pomegranate', 'Wheat'],
    'Sangli': ['Sugarcane', 'Grapes', 'Wheat'],
    'Kolhapur': ['Sugarcane', 'Rice', 'Wheat', 'Vegetables'],
    'Solapur': ['Sugarcane', 'Cotton', 'Wheat', 'Pomegranate', 'Sorghum'],
    
    # North Maharashtra
    'Nashik': ['Grapes', 'Wheat', 'Cotton', 'Banana'],
    'Dhule': ['Cotton', 'Sorghum', 'Wheat', 'Banana'],
    'Jalgaon': ['Cotton', 'Banana', 'Wheat', 'Sorghum'],
    'Nandurbar': ['Cotton', 'Sorghum', 'Maize', 'Wheat'],
    'Ahmednagar': ['Sugarcane', 'Sorghum', 'Wheat', 'Pomegranate']
}

# Crop irrigation requirements
CROP_IRRIGATION_NEEDS = {
    'Grapes': 'High',
    'Sugarcane': 'Very High',
    'Banana': 'High',
    'Pomegranate': 'Medium',
    'Rice': 'Very High',
    'Cotton': 'Medium',
    'Soybean': 'Low',
    'Sorghum': 'Low',
    'Pearl Millet': 'Low',
    'Wheat': 'Medium',
    'Chickpea': 'Low',
    'Pigeon Pea': 'Low',
    'Maize': 'Medium',
    'Sunflower': 'Medium',
    'Groundnut': 'Medium',
    'Coconut': 'Medium',
    'Mango': 'Medium',
    'Green Gram': 'Low',
    'Black Gram': 'Low',
    'Vegetables': 'Medium'
}

# Zone-specific constraints and risk factors
ZONE_CONSTRAINTS = {
    'Marathwada': {
        'water_availability': 'Low',
        'irrigation_coverage': '15-20%',
        'rainfall': '600-900mm',
        'suitable_crops': ['Sorghum', 'Pearl Millet', 'Cotton', 'Pigeon Pea', 'Chickpea'],
        'challenging_crops': ['Grapes', 'Sugarcane', 'Banana', 'Rice'],
        'risk_factors': ['Drought-prone region', 'Limited irrigation infrastructure', 'Low rainfall', 'Groundwater depletion']
    },
    'Konkan': {
        'water_availability': 'High',
        'irrigation_coverage': 'Good',
        'rainfall': '2000-4000mm',
        'suitable_crops': ['Rice', 'Coconut', 'Mango', 'Cashew', 'Spices'],
        'challenging_crops': ['Wheat', 'Sorghum', 'Cotton'],
        'risk_factors': ['High rainfall damage to crops', 'Coastal salinity', 'Pest pressure from humidity']
    },
    'Vidarbha': {
        'water_availability': 'Medium',
        'irrigation_coverage': '30-40%',
        'rainfall': '800-1200mm',
        'suitable_crops': ['Cotton', 'Soybean', 'Pigeon Pea', 'Sorghum'],
        'challenging_crops': ['Sugarcane', 'Grapes', 'Banana'],
        'risk_factors': ['Erratic rainfall patterns', 'Cotton pest pressure', 'Market price volatility']
    },
    'Western_Maharashtra': {
        'water_availability': 'High',
        'irrigation_coverage': '50-70%',
        'rainfall': '600-1200mm',
        'suitable_crops': ['Sugarcane', 'Grapes', 'Pomegranate', 'Wheat'],
        'challenging_crops': ['Rice', 'Sorghum'],
        'risk_factors': ['Water distribution conflicts', 'High input costs', 'Market competition']
    },
    'North_Maharashtra': {
        'water_availability': 'Medium',
        'irrigation_coverage': '40-50%',
        'rainfall': '700-1000mm',
        'suitable_crops': ['Grapes', 'Cotton', 'Banana', 'Wheat'],
        'challenging_crops': ['Rice', 'Sugarcane'],
        'risk_factors': ['Seasonal water stress', 'Temperature fluctuations', 'Market distance']
    }
}

# Flask configuration
DEBUG = os.environ.get('FLASK_ENV') != 'production'
PORT = int(os.environ.get('PORT', 5000))
HOST = '0.0.0.0'

# Add CORS configuration
CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')
