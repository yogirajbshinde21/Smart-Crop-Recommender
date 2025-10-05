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

# Flask configuration
DEBUG = os.environ.get('FLASK_ENV') != 'production'
PORT = int(os.environ.get('PORT', 5000))
HOST = '0.0.0.0'

# Add CORS configuration
CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')
