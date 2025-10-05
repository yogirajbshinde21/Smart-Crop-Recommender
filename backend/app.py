"""
Flask API for Smart Farmer Recommender System
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pandas as pd
import numpy as np
import joblib
import traceback

from config import (
    MODEL_DIR, CROP_MODEL_FILE, NUTRIENT_MODEL_FILE, WATER_MODEL_FILE,
    FERTILIZER_MODEL_FILE, ENCODER_FILE, SCALER_FILE, DEBUG, PORT, HOST,
    AGRICULTURAL_ZONES, ZONE_CHARACTERISTICS, MARKET_RATES, INPUT_COSTS,
    EXPECTED_YIELDS, DATASET_PATH
)
from validation import (
    validate_prediction, get_region, filter_invalid_crops,
    get_alternative_crops, validate_nutrients, get_region_characteristics
)

app = Flask(__name__)

# Production-ready CORS - Allow multiple origins
cors_origins = os.environ.get('CORS_ORIGINS', 'http://localhost:3000,https://smart-farmer-frontend.onrender.com').split(',')
CORS(app, resources={
    r"/*": {
        "origins": cors_origins,
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Global variables for models and processors
models = {}
encoders = {}
scalers = {}
dataset = None


def load_models():
    """Load all trained models"""
    global models, encoders, scalers, dataset
    
    try:
        print("Loading models...")
        
        # Load models
        models['crop'] = joblib.load(os.path.join(MODEL_DIR, CROP_MODEL_FILE))
        models['nutrient'] = joblib.load(os.path.join(MODEL_DIR, NUTRIENT_MODEL_FILE))
        models['water'] = joblib.load(os.path.join(MODEL_DIR, WATER_MODEL_FILE))
        models['fertilizer'] = joblib.load(os.path.join(MODEL_DIR, FERTILIZER_MODEL_FILE))
        
        # Load encoders and scalers
        encoders = joblib.load(os.path.join(MODEL_DIR, ENCODER_FILE))
        scalers = joblib.load(os.path.join(MODEL_DIR, SCALER_FILE))
        
        # Load dataset for insights (CSV instead of Excel)
        if DATASET_PATH.endswith('.csv'):
            dataset = pd.read_csv(DATASET_PATH)
        else:
            dataset = pd.read_excel(DATASET_PATH)
        
        print("[SUCCESS] All models loaded successfully!")
        return True
        
    except Exception as e:
        print(f"Error loading models: {str(e)}")
        print(traceback.format_exc())
        return False


def get_zone(district):
    """Get agricultural zone for a district"""
    for zone, districts in AGRICULTURAL_ZONES.items():
        if district in districts:
            return zone
    return 'Other'


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Smart Farmer API is running',
        'models_loaded': len(models) == 4
    })


@app.route('/dropdown-data', methods=['GET'])
def get_dropdown_data():
    """Get all dropdown options for the frontend"""
    try:
        districts = sorted(dataset['District'].unique().tolist())
        soil_types = sorted(dataset['Soil_Type'].unique().tolist())
        crops = sorted(dataset['Crop_Name'].unique().tolist())
        weather_conditions = sorted(dataset['Weather'].unique().tolist())
        fertilizers = sorted(dataset['Fertilizer'].unique().tolist())
        
        return jsonify({
            'success': True,
            'data': {
                'districts': districts,
                'soil_types': soil_types,
                'crops': crops,
                'weather_conditions': weather_conditions,
                'fertilizers': fertilizers,
                'zones': list(AGRICULTURAL_ZONES.keys())
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/recommend-crop', methods=['POST'])
def recommend_crop():
    """Recommend top 3 crops based on inputs"""
    try:
        data = request.json
        district = data.get('District')
        soil_type = data.get('Soil_Type')
        weather = data.get('Weather')
        
        if not all([district, soil_type, weather]):
            return jsonify({
                'success': False,
                'error': 'Missing required fields: District, Soil_Type, Weather'
            }), 400
        
        # Get zone
        zone = get_zone(district)
        
        # Validate inputs against encoder classes
        if 'District' in encoders:
            valid_districts = encoders['District'].classes_.tolist()
            if district not in valid_districts:
                return jsonify({
                    'success': False,
                    'error': f'District "{district}" not found in training data. Please select from available districts.'
                }), 400
        
        if 'Soil_Type' in encoders:
            valid_soil_types = encoders['Soil_Type'].classes_.tolist()
            if soil_type not in valid_soil_types:
                return jsonify({
                    'success': False,
                    'error': f'Soil Type "{soil_type}" not found in training data. Please select from available soil types.'
                }), 400
        
        if 'Weather' in encoders:
            valid_weather = encoders['Weather'].classes_.tolist()
            if weather not in valid_weather:
                return jsonify({
                    'success': False,
                    'error': f'Weather condition "{weather}" not found in training data. Please select from available weather conditions.'
                }), 400
        
        # Prepare input
        input_df = pd.DataFrame([{
            'District': district,
            'Soil_Type': soil_type,
            'Weather': weather,
            'Zone': zone
        }])
        
        # Encode features
        feature_columns = ['District', 'Soil_Type', 'Weather', 'Zone']
        for col in feature_columns:
            if col in encoders:
                input_df[col] = encoders[col].transform(input_df[col])
        
        # Get predictions with probabilities (use .values to avoid sklearn warning)
        input_array = input_df[feature_columns].values
        probabilities = models['crop'].predict_proba(input_array)[0]
        
        # Get all predictions sorted by probability
        all_indices = np.argsort(probabilities)[::-1]
        crop_encoder = encoders['Crop_Name']
        
        # Create list of (crop_name, probability) tuples
        all_predictions = []
        for idx in all_indices[:15]:  # Check top 15
            crop_name = crop_encoder.inverse_transform([idx])[0]
            prob = float(probabilities[idx])
            all_predictions.append((crop_name, prob))
        
        # Apply validation filter
        valid_predictions = filter_invalid_crops(all_predictions, district, soil_type, weather)
        
        # Build top 3 valid crops
        top_3_crops = []
        for pred in valid_predictions[:3]:
            crop_name = pred['crop']
            confidence = pred['probability'] * 100
            validation_info = pred['validation']
            
            # Get additional info
            crop_data_rows = dataset[dataset['Crop_Name'] == crop_name]
            if len(crop_data_rows) > 0:
                crop_data = crop_data_rows.iloc[0]
            
            top_3_crops.append({
                'crop_name': crop_name,
                'confidence': round(confidence, 2),
                'avg_yield': EXPECTED_YIELDS.get(crop_name, 'N/A'),
                'market_rate': MARKET_RATES.get(crop_name, 'N/A'),
                'suitable_for_zone': zone,
                'validation': {
                    'is_valid': validation_info['is_valid'],
                    'region': validation_info['region'],
                    'reasoning': validation_info['reasoning']
                }
            })
        
        # Get region characteristics
        region = get_region(district)
        region_info = get_region_characteristics(region)
        
        # Get alternative crops
        alternatives = get_alternative_crops(district, soil_type, weather)
        
        # Zone characteristics
        zone_info = ZONE_CHARACTERISTICS.get(zone, {})
        
        # Check if no crops were found and provide helpful info
        no_data_message = None
        suitable_combinations = []
        
        if len(top_3_crops) == 0:
            # Check what combinations exist for this district
            district_data = dataset[dataset['District'] == district]
            
            if len(district_data) > 0:
                # Get available soil types and weather combinations
                available_soils = sorted(district_data['Soil_Type'].unique().tolist())
                available_weather = sorted(district_data['Weather'].unique().tolist())
                
                # Find suitable combinations
                combinations = district_data.groupby(['Soil_Type', 'Weather'])['Crop_Name'].apply(
                    lambda x: sorted(x.unique().tolist())
                ).reset_index()
                
                for _, row in combinations.iterrows():
                    suitable_combinations.append({
                        'soil_type': row['Soil_Type'],
                        'weather': row['Weather'],
                        'crops': row['Crop_Name'][:5]  # Top 5 crops for this combo
                    })
                
                no_data_message = {
                    'title': 'No Crops Found for This Combination',
                    'reason': f'The combination of {soil_type} soil with {weather} weather is not typical for {district} district.',
                    'district_info': f'{district} is located in the {zone} zone.',
                    'available_soils': available_soils,
                    'available_weather': available_weather,
                    'suggestion': f'In {district}, the common soil types are {", ".join(available_soils)}. Please try selecting one of these soil types for better recommendations.'
                }
            else:
                no_data_message = {
                    'title': 'No Data Available',
                    'reason': f'No agricultural data available for {district} district in our database.',
                    'suggestion': 'Please select a different district or contact support for assistance.'
                }
        
        return jsonify({
            'success': True,
            'data': {
                'recommendations': top_3_crops,
                'zone': zone,
                'region': region,
                'region_info': region_info,
                'zone_info': zone_info,
                'alternative_crops': alternatives[:5] if len(top_3_crops) < 3 else [],
                'no_data_message': no_data_message,
                'suitable_combinations': suitable_combinations[:6] if suitable_combinations else [],
                'input': {
                    'district': district,
                    'soil_type': soil_type,
                    'weather': weather
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/predict-nutrients', methods=['POST'])
def predict_nutrients():
    """Predict nutrient requirements"""
    try:
        data = request.json
        district = data.get('District')
        soil_type = data.get('Soil_Type')
        crop_name = data.get('Crop_Name')
        weather = data.get('Weather')
        
        if not all([district, soil_type, crop_name, weather]):
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400
        
        # Get zone
        zone = get_zone(district)
        
        # Prepare input with computed features
        # Use default values for NPK_Ratio and Total_Nutrients since we're predicting them
        input_df = pd.DataFrame([{
            'District': district,
            'Soil_Type': soil_type,
            'Crop_Name': crop_name,
            'Weather': weather,
            'Zone': zone,
            'NPK_Ratio': 1.0,  # Default ratio
            'Total_Nutrients': 200.0  # Default total
        }])
        
        # Encode features
        feature_columns = ['District', 'Soil_Type', 'Crop_Name', 'Weather', 'Zone']
        all_columns = ['District', 'Soil_Type', 'Crop_Name', 'Weather', 'Zone', 'NPK_Ratio', 'Total_Nutrients']
        for col in feature_columns:
            if col in encoders:
                input_df[col] = encoders[col].transform(input_df[col])
        
        # Predict (use .values with correct column order to avoid sklearn warning)
        input_array = input_df[all_columns].values
        prediction = models['nutrient'].predict(input_array)[0]
        
        nutrients = {
            'N_kg_ha': round(float(prediction[0]), 2),
            'P2O5_kg_ha': round(float(prediction[1]), 2),
            'K2O_kg_ha': round(float(prediction[2]), 2),
            'Zn_kg_ha': round(float(prediction[3]), 2),
            'S_kg_ha': round(float(prediction[4]), 2)
        }
        
        # Calculate NPK ratio
        total = nutrients['N_kg_ha'] + nutrients['P2O5_kg_ha'] + nutrients['K2O_kg_ha']
        npk_ratio = {
            'N': round((nutrients['N_kg_ha'] / total) * 100, 1) if total > 0 else 0,
            'P': round((nutrients['P2O5_kg_ha'] / total) * 100, 1) if total > 0 else 0,
            'K': round((nutrients['K2O_kg_ha'] / total) * 100, 1) if total > 0 else 0
        }
        
        # Validate crop-district-soil compatibility
        crop_validation = validate_prediction(district, soil_type, crop_name, weather)
        
        # Validate nutrient predictions against research ranges
        nutrient_validation_status, nutrient_warnings = validate_nutrients(crop_name, nutrients)
        
        # Deficiency alerts
        alerts = []
        
        # Add validation warnings
        for warning in nutrient_warnings:
            alerts.append({
                'type': warning['type'],
                'nutrient': warning['nutrient'],
                'message': warning['message'],
                'expected_range': warning['expected_range']
            })
        
        # Add standard alerts
        if nutrients['Zn_kg_ha'] < 5:
            alerts.append({
                'type': 'warning',
                'nutrient': 'Zinc',
                'message': 'Zinc deficiency common in Maharashtra. Consider zinc sulfate application.'
            })
        
        if nutrients['S_kg_ha'] < 10:
            alerts.append({
                'type': 'info',
                'nutrient': 'Sulfur',
                'message': 'Low sulfur requirement. Monitor crop development.'
            })
        
        return jsonify({
            'success': True,
            'data': {
                'nutrients': nutrients,
                'npk_ratio': npk_ratio,
                'alerts': alerts,
                'validation': {
                    'crop_compatibility': crop_validation,
                    'nutrient_accuracy': nutrient_validation_status
                },
                'input': {
                    'district': district,
                    'soil_type': soil_type,
                    'crop_name': crop_name,
                    'weather': weather,
                    'zone': zone
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/water-quality-analysis', methods=['POST'])
def water_quality_analysis():
    """Predict water quality parameters"""
    try:
        data = request.json
        district = data.get('District')
        weather = data.get('Weather')
        soil_type = data.get('Soil_Type')
        
        if not all([district, weather, soil_type]):
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400
        
        # Get zone
        zone = get_zone(district)
        
        # Prepare input
        input_df = pd.DataFrame([{
            'District': district,
            'Weather': weather,
            'Soil_Type': soil_type,
            'Zone': zone
        }])
        
        # Encode features
        feature_columns = ['District', 'Weather', 'Soil_Type', 'Zone']
        for col in feature_columns:
            if col in encoders:
                input_df[col] = encoders[col].transform(input_df[col])
        
        # Predict (use .values to avoid sklearn warning)
        prediction = models['water'].predict(input_df.values)[0]
        
        water_params = {
            'recommended_pH': round(float(prediction[0]), 2),
            'turbidity_NTU': round(float(prediction[1]), 2),
            'water_temp_C': round(float(prediction[2]), 2)
        }
        
        # pH recommendations
        ph_status = 'Neutral'
        ph_advice = 'pH level is optimal for most crops.'
        
        if water_params['recommended_pH'] < 6.0:
            ph_status = 'Acidic'
            ph_advice = 'Consider adding lime to increase pH for better nutrient availability.'
        elif water_params['recommended_pH'] > 8.0:
            ph_status = 'Alkaline'
            ph_advice = 'Consider adding organic matter or sulfur to lower pH.'
        
        # Turbidity analysis
        turbidity_status = 'Clear'
        turbidity_advice = 'Water turbidity is acceptable for irrigation.'
        
        if water_params['turbidity_NTU'] > 10:
            turbidity_status = 'Moderate'
            turbidity_advice = 'Consider filtration or sedimentation for sensitive crops.'
        elif water_params['turbidity_NTU'] > 15:
            turbidity_status = 'High'
            turbidity_advice = 'Pre-treatment recommended before irrigation.'
        
        # Temperature considerations
        temp_status = 'Optimal'
        temp_advice = 'Water temperature suitable for irrigation.'
        
        if water_params['water_temp_C'] > 35:
            temp_status = 'High'
            temp_advice = 'Consider early morning or evening irrigation to avoid thermal stress.'
        
        return jsonify({
            'success': True,
            'data': {
                'water_parameters': water_params,
                'analysis': {
                    'pH': {
                        'status': ph_status,
                        'advice': ph_advice
                    },
                    'turbidity': {
                        'status': turbidity_status,
                        'advice': turbidity_advice
                    },
                    'temperature': {
                        'status': temp_status,
                        'advice': temp_advice
                    }
                },
                'input': {
                    'district': district,
                    'weather': weather,
                    'soil_type': soil_type,
                    'zone': zone
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/fertilizer-recommendation', methods=['POST'])
def fertilizer_recommendation():
    """Recommend optimal fertilizer"""
    try:
        data = request.json
        crop_name = data.get('Crop_Name')
        soil_type = data.get('Soil_Type')
        n_kg_ha = data.get('N_kg_ha', 0)
        p2o5_kg_ha = data.get('P2O5_kg_ha', 0)
        k2o_kg_ha = data.get('K2O_kg_ha', 0)
        
        if not all([crop_name, soil_type]):
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400
        
        # Prepare input
        input_df = pd.DataFrame([{
            'Crop_Name': crop_name,
            'Soil_Type': soil_type,
            'N_kg_ha': n_kg_ha,
            'P2O5_kg_ha': p2o5_kg_ha,
            'K2O_kg_ha': k2o_kg_ha
        }])
        
        # Encode features
        for col in ['Crop_Name', 'Soil_Type']:
            if col in encoders:
                input_df[col] = encoders[col].transform(input_df[col])
        
        # Get predictions with probabilities (use .values to avoid sklearn warning)
        probabilities = models['fertilizer'].predict_proba(input_df.values)[0]
        predicted_class = models['fertilizer'].predict(input_df.values)[0]
        
        # Apply temperature scaling to smooth confidence
        temperature = 1.5
        probabilities = np.exp(np.log(probabilities + 1e-10) / temperature)
        probabilities = probabilities / probabilities.sum()
        
        # Get top 3 fertilizers
        top_3_indices = np.argsort(probabilities)[-3:][::-1]
        recommendations = []
        
        fertilizer_encoder = encoders['Fertilizer']
        
        for idx in top_3_indices:
            fertilizer = fertilizer_encoder.inverse_transform([idx])[0]
            confidence = float(probabilities[idx] * 100)
            
            recommendations.append({
                'fertilizer': fertilizer,
                'confidence': round(confidence, 2),
                'cost_per_hectare': INPUT_COSTS['Fertilizer'].get(fertilizer, 'N/A'),
                'is_primary': idx == predicted_class
            })
        
        return jsonify({
            'success': True,
            'data': {
                'recommendations': recommendations,
                'input': {
                    'crop_name': crop_name,
                    'soil_type': soil_type,
                    'nutrients': {
                        'N': n_kg_ha,
                        'P': p2o5_kg_ha,
                        'K': k2o_kg_ha
                    }
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/compare-crops', methods=['POST'])
def compare_crops():
    """Compare multiple crops side by side"""
    try:
        data = request.json
        crops = data.get('crops', [])  # List of crop names
        district = data.get('District')
        soil_type = data.get('Soil_Type')
        weather = data.get('Weather')
        
        if not crops or not all([district, soil_type, weather]):
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400
        
        # Validate inputs against encoder classes
        if 'District' in encoders:
            valid_districts = encoders['District'].classes_.tolist()
            if district not in valid_districts:
                return jsonify({
                    'success': False,
                    'error': f'District "{district}" not found in training data. Please select from available districts.'
                }), 400
        
        if 'Soil_Type' in encoders:
            valid_soil_types = encoders['Soil_Type'].classes_.tolist()
            if soil_type not in valid_soil_types:
                return jsonify({
                    'success': False,
                    'error': f'Soil Type "{soil_type}" not found in training data. Please select from available soil types.'
                }), 400
        
        if 'Weather' in encoders:
            valid_weather = encoders['Weather'].classes_.tolist()
            if weather not in valid_weather:
                return jsonify({
                    'success': False,
                    'error': f'Weather condition "{weather}" not found in training data. Please select from available weather conditions.'
                }), 400
        
        if 'Crop_Name' in encoders:
            valid_crops = encoders['Crop_Name'].classes_.tolist()
            for crop in crops:
                if crop not in valid_crops:
                    return jsonify({
                        'success': False,
                        'error': f'Crop "{crop}" not found in training data. Please select from available crops.'
                    }), 400
        
        zone = get_zone(district)
        comparison_data = []
        
        for crop_name in crops:
            # Get nutrient requirements
            input_df = pd.DataFrame([{
                'District': district,
                'Soil_Type': soil_type,
                'Crop_Name': crop_name,
                'Weather': weather,
                'Zone': zone,
                'NPK_Ratio': 1.0,  # Default ratio
                'Total_Nutrients': 200.0  # Default total
            }])
            
            # Encode
            for col in ['District', 'Soil_Type', 'Crop_Name', 'Weather', 'Zone']:
                if col in encoders:
                    input_df[col] = encoders[col].transform(input_df[col])
            
            # Predict nutrients (use .values to avoid sklearn warning)
            nutrients = models['nutrient'].predict(input_df.values)[0]
            
            # Calculate costs and returns
            seed_cost = INPUT_COSTS['Seeds'].get(crop_name, 5000)
            fertilizer_cost = INPUT_COSTS['Fertilizer'].get('DAP', 1400)
            total_cost = seed_cost + fertilizer_cost + INPUT_COSTS['Labor'] + INPUT_COSTS['Irrigation'] + INPUT_COSTS['Pesticides']
            
            expected_yield = EXPECTED_YIELDS.get(crop_name, 20)
            market_rate = MARKET_RATES.get(crop_name, 3000)
            gross_income = expected_yield * market_rate
            net_income = gross_income - total_cost
            roi = (net_income / total_cost * 100) if total_cost > 0 else 0
            
            # Risk assessment
            risk_score = 'Medium'
            if zone in ['Marathwada'] and crop_name in ['Sugarcane', 'Rice']:
                risk_score = 'High'
            elif zone in ['Western Maharashtra'] and crop_name in ['Sugarcane', 'Grapes']:
                risk_score = 'Low'
            
            comparison_data.append({
                'crop_name': crop_name,
                'nutrients': {
                    'N': round(float(nutrients[0]), 2),
                    'P': round(float(nutrients[1]), 2),
                    'K': round(float(nutrients[2]), 2),
                    'Zn': round(float(nutrients[3]), 2),
                    'S': round(float(nutrients[4]), 2)
                },
                'economics': {
                    'total_cost': round(total_cost, 2),
                    'expected_yield': expected_yield,
                    'market_rate': market_rate,
                    'gross_income': round(gross_income, 2),
                    'net_income': round(net_income, 2),
                    'roi_percentage': round(roi, 2)
                },
                'risk_assessment': {
                    'risk_level': risk_score,
                    'water_requirement': 'High' if crop_name in ['Sugarcane', 'Rice'] else 'Medium',
                    'zone_suitability': zone
                }
            })
        
        # Determine best crop
        best_crop = max(comparison_data, key=lambda x: x['economics']['roi_percentage'])
        
        return jsonify({
            'success': True,
            'data': {
                'comparison': comparison_data,
                'recommendation': {
                    'best_crop': best_crop['crop_name'],
                    'reason': f"Highest ROI of {best_crop['economics']['roi_percentage']:.2f}%",
                    'roi': best_crop['economics']['roi_percentage']
                },
                'input': {
                    'district': district,
                    'soil_type': soil_type,
                    'weather': weather,
                    'zone': zone
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/district-insights/<district_name>', methods=['GET'])
def district_insights(district_name):
    """Get detailed insights for a specific district"""
    try:
        district_data = dataset[dataset['District'] == district_name]
        
        if district_data.empty:
            return jsonify({
                'success': False,
                'error': f'No data found for district: {district_name}'
            }), 404
        
        zone = get_zone(district_name)
        zone_info = ZONE_CHARACTERISTICS.get(zone, {})
        
        # Soil type distribution
        soil_distribution = district_data['Soil_Type'].value_counts().to_dict()
        
        # Popular crops
        crop_distribution = district_data['Crop_Name'].value_counts().head(10).to_dict()
        
        # Weather patterns
        weather_distribution = district_data['Weather'].value_counts().to_dict()
        
        # Average nutrient requirements
        avg_nutrients = {
            'N_kg_ha': round(district_data['N_kg_ha'].mean(), 2),
            'P2O5_kg_ha': round(district_data['P2O5_kg_ha'].mean(), 2),
            'K2O_kg_ha': round(district_data['K2O_kg_ha'].mean(), 2),
            'Zn_kg_ha': round(district_data['Zn_kg_ha'].mean(), 2),
            'S_kg_ha': round(district_data['S_kg_ha'].mean(), 2)
        }
        
        # Water quality stats
        water_stats = {
            'avg_pH': round(district_data['Recommended_pH'].mean(), 2),
            'avg_turbidity': round(district_data['Turbidity_NTU'].mean(), 2),
            'avg_temp': round(district_data['Water_Temp_C'].mean(), 2)
        }
        
        return jsonify({
            'success': True,
            'data': {
                'district': district_name,
                'zone': zone,
                'zone_characteristics': zone_info,
                'soil_distribution': soil_distribution,
                'popular_crops': crop_distribution,
                'weather_patterns': weather_distribution,
                'average_nutrients': avg_nutrients,
                'water_quality': water_stats,
                'total_records': len(district_data)
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/statistics', methods=['GET'])
def get_statistics():
    """Get overall system statistics"""
    try:
        stats = {
            'total_records': len(dataset),
            'total_districts': dataset['District'].nunique(),
            'total_crops': dataset['Crop_Name'].nunique(),
            'total_soil_types': dataset['Soil_Type'].nunique(),
            'total_weather_conditions': dataset['Weather'].nunique(),
            'zones': len(AGRICULTURAL_ZONES),
            'districts_by_zone': {zone: len(districts) for zone, districts in AGRICULTURAL_ZONES.items()}
        }
        
        return jsonify({
            'success': True,
            'data': stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Load models when app starts
load_models()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
