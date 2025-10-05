"""
Agricultural Validation Layer for Maharashtra Smart Farmer System
Ensures scientific accuracy by enforcing district-crop-soil compatibility rules
"""

# ==================================================================
# REGIONAL MAPPING - BASED ON RESEARCH DATA
# ==================================================================

DISTRICTS_BY_REGION = {
    'Konkan': [
        'Thane', 'Palghar', 'Raigad', 'Ratnagiri', 'Sindhudurg', 
        'Mumbai City', 'Mumbai Suburban'
    ],
    'Vidarbha': [
        'Nagpur', 'Amravati', 'Akola', 'Yavatmal', 'Buldhana', 'Washim',
        'Wardha', 'Chandrapur', 'Bhandara', 'Gadchiroli', 'Gondia'
    ],
    'Marathwada': [
        'Aurangabad', 'Jalna', 'Beed', 'Latur', 'Osmanabad', 
        'Nanded', 'Parbhani', 'Hingoli'
    ],
    'Western_Maharashtra': [
        'Pune', 'Satara', 'Sangli', 'Kolhapur', 'Solapur'
    ],
    'North_Maharashtra': [
        'Nashik', 'Dhule', 'Jalgaon', 'Nandurbar', 'Ahmednagar'
    ]
}

# Inverse mapping: District -> Region
DISTRICT_TO_REGION = {}
for region, districts in DISTRICTS_BY_REGION.items():
    for district in districts:
        DISTRICT_TO_REGION[district] = region

# ==================================================================
# CROP COMPATIBILITY RULES
# ==================================================================

# Crops allowed by region (based on research data)
REGION_ALLOWED_CROPS = {
    'Konkan': [
        'Rice', 'Coconut', 'Mango', 'Cashew', 'Vegetables', 
        'Finger Millet', 'Groundnut', 'Pulses'
    ],
    'Vidarbha': [
        'Cotton', 'Soybean', 'Wheat', 'Sorghum', 'Pigeon Pea', 
        'Rice', 'Chickpea', 'Sunflower', 'Maize', 'Safflower'
    ],
    'Marathwada': [
        'Sorghum', 'Cotton', 'Bajra', 'Chickpea', 'Pigeon Pea', 
        'Soybean', 'Sunflower', 'Pulses', 'Safflower'
    ],
    'Western_Maharashtra': [
        'Sugarcane', 'Wheat', 'Sorghum', 'Grapes', 'Pomegranate', 
        'Maize', 'Cotton', 'Soybean', 'Vegetables', 'Onion'
    ],
    'North_Maharashtra': [
        'Grapes', 'Onion', 'Cotton', 'Banana', 'Wheat', 'Sugarcane',
        'Sorghum', 'Maize', 'Chickpea', 'Vegetables'
    ]
}

# Crops forbidden by region
REGION_FORBIDDEN_CROPS = {
    'Konkan': ['Cotton', 'Wheat', 'Grapes', 'Pomegranate', 'Bajra', 'Safflower'],
    'Vidarbha': ['Coconut', 'Cashew', 'Grapes', 'Pomegranate', 'Banana'],
    'Marathwada': ['Coconut', 'Cashew', 'Rice', 'Grapes', 'Banana', 'Mango'],
    'Western_Maharashtra': ['Coconut', 'Cashew', 'Bajra'],
    'North_Maharashtra': ['Coconut', 'Cashew', 'Mango']
}

# Soil-crop strict compatibility
SOIL_COMPATIBLE_CROPS = {
    'Laterite': ['Rice', 'Coconut', 'Cashew', 'Mango', 'Groundnut', 'Vegetables', 'Finger Millet'],
    'Black': ['Cotton', 'Wheat', 'Sorghum', 'Chickpea', 'Sugarcane', 'Soybean', 'Safflower', 
              'Pigeon Pea', 'Sunflower', 'Onion', 'Grapes', 'Pomegranate'],
    'Red': ['Rice', 'Cotton', 'Groundnut', 'Soybean', 'Mango', 'Maize', 
            'Finger Millet', 'Vegetables', 'Pulses'],
    'Alluvial': ['Sugarcane', 'Rice', 'Wheat', 'Maize', 'Vegetables', 'Banana', 
                 'Soybean', 'Cotton'],
    'Sandy': ['Bajra', 'Groundnut', 'Pulses', 'Coconut', 'Vegetables', 'Finger Millet'],
    'Clay': ['Rice', 'Cotton', 'Wheat', 'Sugarcane', 'Soybean', 'Chickpea']
}

# Weather-crop compatibility
WEATHER_COMPATIBLE_CROPS = {
    'Monsoon': ['Rice', 'Cotton', 'Soybean', 'Maize', 'Sorghum', 'Coconut', 'Mango'],
    'Heavy Rainfall': ['Rice', 'Coconut', 'Cashew', 'Mango', 'Vegetables'],
    'Humid': ['Rice', 'Coconut', 'Banana', 'Sugarcane', 'Vegetables'],
    'Post-Monsoon': ['Cotton', 'Soybean', 'Wheat', 'Sorghum', 'Chickpea', 'Vegetables', 'Onion'],
    'Winter': ['Wheat', 'Chickpea', 'Onion', 'Vegetables', 'Grapes', 'Pomegranate'],
    'Cool Dry': ['Wheat', 'Chickpea', 'Grapes', 'Pomegranate', 'Onion'],
    'Semi-Arid': ['Sorghum', 'Bajra', 'Cotton', 'Chickpea', 'Grapes', 'Pomegranate', 'Safflower'],
    'Dry': ['Sorghum', 'Bajra', 'Safflower', 'Sunflower', 'Pomegranate'],
    'Moderate Rainfall': ['Cotton', 'Soybean', 'Wheat', 'Grapes', 'Sugarcane', 'Onion'],
    'Summer': ['Sorghum', 'Sunflower', 'Groundnut', 'Vegetables']
}

# ==================================================================
# CROP-SPECIFIC NUTRIENT RANGES (Research-Based)
# ==================================================================

CROP_NUTRIENT_RANGES = {
    'Cotton': {
        'N_kg_ha': (100, 150), 'P2O5_kg_ha': (40, 60), 'K2O_kg_ha': (40, 60),
        'Zn_kg_ha': (2.5, 5.0), 'S_kg_ha': (15, 25)
    },
    'Sugarcane': {
        'N_kg_ha': (200, 300), 'P2O5_kg_ha': (80, 120), 'K2O_kg_ha': (150, 200),
        'Zn_kg_ha': (5.0, 10.0), 'S_kg_ha': (25, 40)
    },
    'Rice': {
        'N_kg_ha': (100, 120), 'P2O5_kg_ha': (50, 60), 'K2O_kg_ha': (50, 60),
        'Zn_kg_ha': (2.5, 5.0), 'S_kg_ha': (10, 20)
    },
    'Wheat': {
        'N_kg_ha': (100, 120), 'P2O5_kg_ha': (50, 60), 'K2O_kg_ha': (50, 60),
        'Zn_kg_ha': (2.5, 5.0), 'S_kg_ha': (15, 25)
    },
    'Soybean': {
        'N_kg_ha': (30, 40), 'P2O5_kg_ha': (60, 80), 'K2O_kg_ha': (40, 50),
        'Zn_kg_ha': (2.5, 5.0), 'S_kg_ha': (15, 25)
    },
    'Grapes': {
        'N_kg_ha': (100, 150), 'P2O5_kg_ha': (50, 75), 'K2O_kg_ha': (100, 150),
        'Zn_kg_ha': (5.0, 10.0), 'S_kg_ha': (20, 30)
    },
    'Coconut': {
        'N_kg_ha': (500, 600), 'P2O5_kg_ha': (320, 390), 'K2O_kg_ha': (1200, 1400),
        'Zn_kg_ha': (5.0, 15.0), 'S_kg_ha': (25, 40)
    },
    'Sorghum': {
        'N_kg_ha': (80, 100), 'P2O5_kg_ha': (40, 50), 'K2O_kg_ha': (40, 50),
        'Zn_kg_ha': (2.5, 5.0), 'S_kg_ha': (15, 25)
    },
    'Bajra': {
        'N_kg_ha': (60, 80), 'P2O5_kg_ha': (40, 50), 'K2O_kg_ha': (20, 30),
        'Zn_kg_ha': (2.5, 5.0), 'S_kg_ha': (10, 20)
    },
    'Chickpea': {
        'N_kg_ha': (20, 30), 'P2O5_kg_ha': (40, 50), 'K2O_kg_ha': (20, 30),
        'Zn_kg_ha': (2.5, 5.0), 'S_kg_ha': (15, 25)
    },
    'Maize': {
        'N_kg_ha': (120, 150), 'P2O5_kg_ha': (50, 70), 'K2O_kg_ha': (40, 60),
        'Zn_kg_ha': (2.5, 5.0), 'S_kg_ha': (15, 25)
    },
    'Onion': {
        'N_kg_ha': (100, 120), 'P2O5_kg_ha': (50, 70), 'K2O_kg_ha': (100, 120),
        'Zn_kg_ha': (2.5, 5.0), 'S_kg_ha': (25, 35)
    },
    'Pomegranate': {
        'N_kg_ha': (100, 150), 'P2O5_kg_ha': (50, 75), 'K2O_kg_ha': (100, 150),
        'Zn_kg_ha': (5.0, 10.0), 'S_kg_ha': (20, 30)
    },
    'Banana': {
        'N_kg_ha': (200, 250), 'P2O5_kg_ha': (70, 100), 'K2O_kg_ha': (300, 400),
        'Zn_kg_ha': (5.0, 10.0), 'S_kg_ha': (25, 35)
    }
}

# ==================================================================
# VALIDATION FUNCTIONS
# ==================================================================

def get_region(district):
    """Get region for a district"""
    return DISTRICT_TO_REGION.get(district, 'Unknown')


def validate_crop_for_district(crop, district):
    """Check if crop is valid for district"""
    region = get_region(district)
    
    if region == 'Unknown':
        return False, f"District '{district}' not found in database"
    
    allowed_crops = REGION_ALLOWED_CROPS.get(region, [])
    forbidden_crops = REGION_FORBIDDEN_CROPS.get(region, [])
    
    if crop in forbidden_crops:
        return False, f"{crop} is not suitable for {region} region (District: {district})"
    
    if crop not in allowed_crops:
        return False, f"{crop} is not commonly grown in {region} region"
    
    return True, f"{crop} is suitable for {region} region"


def validate_crop_for_soil(crop, soil_type):
    """Check if crop is compatible with soil type"""
    compatible_crops = SOIL_COMPATIBLE_CROPS.get(soil_type, [])
    
    if crop not in compatible_crops:
        return False, f"{crop} is not compatible with {soil_type} soil"
    
    return True, f"{crop} grows well in {soil_type} soil"


def validate_crop_for_weather(crop, weather):
    """Check if crop is suitable for weather condition"""
    compatible_crops = WEATHER_COMPATIBLE_CROPS.get(weather, [])
    
    if crop not in compatible_crops:
        return False, f"{crop} is not suitable for {weather} weather conditions"
    
    return True, f"{crop} thrives in {weather} conditions"


def validate_prediction(district, soil_type, crop, weather):
    """
    Comprehensive validation of crop prediction
    Returns: (is_valid, validation_details)
    """
    validation_results = {
        'is_valid': True,
        'region': get_region(district),
        'checks': [],
        'warnings': [],
        'errors': []
    }
    
    # Check 1: District compatibility
    is_valid_district, msg_district = validate_crop_for_district(crop, district)
    validation_results['checks'].append({
        'check': 'District Compatibility',
        'passed': is_valid_district,
        'message': msg_district
    })
    if not is_valid_district:
        validation_results['is_valid'] = False
        validation_results['errors'].append(msg_district)
    
    # Check 2: Soil compatibility
    is_valid_soil, msg_soil = validate_crop_for_soil(crop, soil_type)
    validation_results['checks'].append({
        'check': 'Soil Compatibility',
        'passed': is_valid_soil,
        'message': msg_soil
    })
    if not is_valid_soil:
        validation_results['is_valid'] = False
        validation_results['errors'].append(msg_soil)
    
    # Check 3: Weather compatibility
    is_valid_weather, msg_weather = validate_crop_for_weather(crop, weather)
    validation_results['checks'].append({
        'check': 'Weather Compatibility',
        'passed': is_valid_weather,
        'message': msg_weather
    })
    if not is_valid_weather:
        validation_results['warnings'].append(msg_weather)
    
    # Generate reasoning
    if validation_results['is_valid']:
        validation_results['reasoning'] = (
            f"{crop} is scientifically suitable for {district} district "
            f"({validation_results['region']} region) with {soil_type} soil "
            f"and {weather} weather conditions."
        )
    else:
        validation_results['reasoning'] = (
            f"{crop} is NOT recommended for {district} district. "
            f"Validation failed: {', '.join(validation_results['errors'])}"
        )
    
    return validation_results


def get_alternative_crops(district, soil_type, weather):
    """Get valid alternative crops for given conditions"""
    region = get_region(district)
    
    # Get intersection of all compatible crops
    allowed_by_region = set(REGION_ALLOWED_CROPS.get(region, []))
    allowed_by_soil = set(SOIL_COMPATIBLE_CROPS.get(soil_type, []))
    allowed_by_weather = set(WEATHER_COMPATIBLE_CROPS.get(weather, []))
    
    # Intersection
    valid_crops = allowed_by_region & allowed_by_soil & allowed_by_weather
    
    # Remove forbidden crops
    forbidden = set(REGION_FORBIDDEN_CROPS.get(region, []))
    valid_crops = valid_crops - forbidden
    
    return sorted(list(valid_crops))


def filter_invalid_crops(predictions, district, soil_type, weather):
    """
    Filter crop predictions to return only valid ones
    predictions: list of (crop_name, probability) tuples
    Returns: filtered list of valid predictions
    """
    valid_crops = get_alternative_crops(district, soil_type, weather)
    
    filtered = []
    for crop, prob in predictions:
        if crop in valid_crops:
            validation = validate_prediction(district, soil_type, crop, weather)
            filtered.append({
                'crop': crop,
                'probability': prob,
                'validation': validation
            })
    
    return filtered


def validate_nutrients(crop, nutrients):
    """Validate if predicted nutrients are within research-based ranges"""
    if crop not in CROP_NUTRIENT_RANGES:
        return True, []  # No validation data available
    
    ranges = CROP_NUTRIENT_RANGES[crop]
    warnings = []
    
    for nutrient, (min_val, max_val) in ranges.items():
        if nutrient in nutrients:
            value = nutrients[nutrient]
            if value < min_val:
                warnings.append({
                    'nutrient': nutrient,
                    'type': 'low',
                    'value': value,
                    'expected_range': f"{min_val}-{max_val}",
                    'message': f"{nutrient} is below recommended range for {crop}"
                })
            elif value > max_val:
                warnings.append({
                    'nutrient': nutrient,
                    'type': 'high',
                    'value': value,
                    'expected_range': f"{min_val}-{max_val}",
                    'message': f"{nutrient} exceeds recommended range for {crop}"
                })
    
    is_valid = len(warnings) == 0
    return is_valid, warnings


def get_region_characteristics(region):
    """Get detailed characteristics of a region"""
    characteristics = {
        'Konkan': {
            'climate': 'Coastal, High rainfall (2000-4000mm)',
            'soil_types': 'Laterite (70%), Red (20%), Sandy (10%)',
            'major_crops': 'Rice, Coconut, Mango, Cashew',
            'characteristics': 'High humidity, good water availability, laterite soil dominant'
        },
        'Vidarbha': {
            'climate': 'Moderate rainfall (800-1200mm), Cotton belt',
            'soil_types': 'Black (80%), Clay (15%), Red (5%)',
            'major_crops': 'Cotton, Soybean, Wheat, Sorghum',
            'characteristics': 'Black soil region, suitable for cotton and pulses'
        },
        'Marathwada': {
            'climate': 'Semi-arid, Drought-prone (600-900mm)',
            'soil_types': 'Black (70%), Red (20%), Sandy (10%)',
            'major_crops': 'Sorghum, Cotton, Bajra, Chickpea',
            'characteristics': 'Low rainfall, drought-resistant crops preferred'
        },
        'Western_Maharashtra': {
            'climate': 'Moderate rainfall (1000-2000mm), Sugarcane belt',
            'soil_types': 'Black (60%), Red (25%), Alluvial (15%)',
            'major_crops': 'Sugarcane, Grapes, Wheat, Pomegranate',
            'characteristics': 'Fertile region, high-value crops, good irrigation'
        },
        'North_Maharashtra': {
            'climate': 'Moderate rainfall (700-1200mm)',
            'soil_types': 'Black (70%), Alluvial (20%), Red (10%)',
            'major_crops': 'Grapes, Onion, Cotton, Banana',
            'characteristics': 'Famous for grapes (Nashik) and onions'
        }
    }
    
    return characteristics.get(region, {})


# ==================================================================
# TEST VALIDATION EXAMPLES
# ==================================================================

def run_validation_tests():
    """Run validation tests on known examples"""
    test_cases = [
        # Should PASS
        ('Raigad', 'Laterite', 'Rice', 'Monsoon', True),
        ('Raigad', 'Laterite', 'Coconut', 'Humid', True),
        ('Latur', 'Black', 'Sorghum', 'Semi-Arid', True),
        ('Nashik', 'Black', 'Grapes', 'Moderate Rainfall', True),
        ('Nagpur', 'Black', 'Cotton', 'Post-Monsoon', True),
        
        # Should FAIL
        ('Raigad', 'Laterite', 'Grapes', 'Monsoon', False),
        ('Latur', 'Black', 'Coconut', 'Semi-Arid', False),
        ('Nagpur', 'Black', 'Grapes', 'Post-Monsoon', False),
    ]
    
    print("="*70)
    print("VALIDATION LAYER TESTS")
    print("="*70)
    
    passed = 0
    failed = 0
    
    for district, soil, crop, weather, expected_valid in test_cases:
        result = validate_prediction(district, soil, crop, weather)
        actual_valid = result['is_valid']
        
        status = "✓ PASS" if actual_valid == expected_valid else "✗ FAIL"
        print(f"\n{status}: {district} + {soil} + {crop} + {weather}")
        print(f"  Expected: {expected_valid}, Got: {actual_valid}")
        print(f"  Reasoning: {result['reasoning']}")
        
        if actual_valid == expected_valid:
            passed += 1
        else:
            failed += 1
    
    print("\n" + "="*70)
    print(f"Test Results: {passed}/{len(test_cases)} passed")
    print("="*70)


if __name__ == "__main__":
    run_validation_tests()
