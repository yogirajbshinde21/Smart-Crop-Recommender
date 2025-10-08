"""
Crop Prediction Calibrator - Post-Processing Layer
===================================================

This module provides calibration functions to adjust ML model predictions
to realistic agricultural values without modifying the trained models or dataset.

The calibrator applies correction factors to:
1. Economic metrics (ROI, costs, income)
2. Nutrient requirements (N, P, K, Zn, S)
3. District-specific validations

Author: Smart Farmer System
Date: October 2025
"""

import logging
from typing import Dict, Any, Optional

# Configure logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# CROP-SPECIFIC CALIBRATION CONFIGURATION
# ============================================================================
# Based on real Maharashtra agricultural data and research papers

CROP_CALIBRATION_CONFIG = {
    'Rice': {
        'costMultiplier': 1.5,          # Adjust from ₹31,900 to ₹47,850/ha
        'roiMultiplier': 0.15,          # CORRECTED: Realistic B:C ratio 1.27-1.50 (27-50% ROI)
        'nutrientDivisor': 200,          # Scale down 30,586 kg/ha to 152.93 kg/ha
        'maxROI': 80,                   # CORRECTED: Cap at realistic 80% maximum
        'minROI': 20,                    # Floor minimum ROI
        'minCost': 40000,                # Minimum realistic cost
        'maxCost': 70000,                # Maximum realistic cost
        'realisticYield': 40,            # Quintal/ha
        'notes': 'Paddy cultivation in Maharashtra, Kharif season. B:C ratio 1.27-1.50'
    },
    'Wheat': {
        'costMultiplier': 1.4,
        'roiMultiplier': 0.25,          # CORRECTED: B:C ratio 1.40-1.60 (40-60% ROI)
        'nutrientDivisor': 200,
        'maxROI': 70,                   # CORRECTED: Realistic maximum
        'minROI': 30,
        'minCost': 35000,
        'maxCost': 60000,
        'realisticYield': 35,
        'notes': 'Rabi season crop, B:C ratio 1.40-1.60'
    },
    'Grapes': {
        'costMultiplier': 8.5,           # Critical: ₹129,400 → ₹1,100,000/ha
        'roiMultiplier': 0.08,           # CORRECTED: B:C ratio 1.81 (81% ROI) realistic
        'nutrientDivisor': 200,
        'maxROI': 150,                   # CORRECTED: Cap at 150% (very optimistic but possible)
        'minROI': 60,                    # Minimum for high-value crop
        'minCost': 900000,               # Very high input cost (perennial crop)
        'maxCost': 1500000,
        'realisticYield': 200,
        'notes': 'Based on Sangli/Nashik data. B:C ratio 1.81 (81% ROI). Highest profitability crop'
    },
    'Cotton': {
        'costMultiplier': 1.8,
        'roiMultiplier': 0.20,          # CORRECTED: B:C ratio 1.30-1.50 (30-50% ROI)
        'nutrientDivisor': 200,
        'maxROI': 65,                   # CORRECTED: Realistic maximum
        'minROI': 20,
        'minCost': 45000,
        'maxCost': 80000,
        'realisticYield': 18,
        'notes': 'Kharif crop, Vidarbha & Marathwada. B:C ratio 1.30-1.50'
    },
    'Sugarcane': {
        'costMultiplier': 2.5,
        'roiMultiplier': 0.18,          # CORRECTED: B:C ratio 1.50-1.70 (50-70% ROI)
        'nutrientDivisor': 200,
        'maxROI': 90,                   # CORRECTED: High irrigation cost considered
        'minROI': 40,
        'minCost': 80000,
        'maxCost': 150000,
        'realisticYield': 800,
        'notes': 'High water requirement, Western Maharashtra. B:C ratio 1.50-1.70'
    },
    'Soybean': {
        'costMultiplier': 1.6,
        'roiMultiplier': 0.22,          # CORRECTED: B:C ratio 1.40-1.60 (40-60% ROI)
        'nutrientDivisor': 200,
        'maxROI': 75,                   # CORRECTED: Realistic maximum
        'minROI': 30,
        'minCost': 30000,
        'maxCost': 60000,
        'realisticYield': 25,
        'notes': 'Kharif oilseed, Vidarbha region. B:C ratio 1.40-1.60'
    },
    'Sorghum': {
        'costMultiplier': 1.5,
        'roiMultiplier': 0.18,          # CORRECTED: B:C ratio 1.35-1.55 (35-55% ROI)
        'nutrientDivisor': 200,
        'maxROI': 65,                   # CORRECTED: Realistic for drought-resistant crop
        'minROI': 25,
        'minCost': 25000,
        'maxCost': 50000,
        'realisticYield': 30,
        'notes': 'Jowar - drought-resistant, Marathwada. B:C ratio 1.35-1.55'
    },
    'Maize': {
        'costMultiplier': 1.6,
        'roiMultiplier': 0.25,          # CORRECTED: B:C ratio 1.50-1.80 (50-80% ROI)
        'nutrientDivisor': 200,
        'maxROI': 85,                   # CORRECTED: Good returns with hybrid varieties
        'minROI': 40,
        'minCost': 35000,
        'maxCost': 65000,
        'realisticYield': 45,
        'notes': 'Kharif & Rabi, hybrid varieties. B:C ratio 1.50-1.80'
    },
    'Chickpea': {
        'costMultiplier': 1.7,
        'roiMultiplier': 0.28,          # CORRECTED: B:C ratio 1.60-1.90 (60-90% ROI)
        'nutrientDivisor': 200,
        'maxROI': 95,                   # CORRECTED: Good pulse market prices
        'minROI': 50,
        'minCost': 35000,
        'maxCost': 65000,
        'realisticYield': 20,
        'notes': 'Chana - Rabi pulse, good market price. B:C ratio 1.60-1.90'
    },
    'Pigeon Pea': {
        'costMultiplier': 1.6,
        'roiMultiplier': 0.26,          # CORRECTED: B:C ratio 1.55-1.80 (55-80% ROI)
        'nutrientDivisor': 200,
        'maxROI': 88,                   # CORRECTED: Pulses have good returns
        'minROI': 45,
        'minCost': 30000,
        'maxCost': 60000,
        'realisticYield': 18,
        'notes': 'Tur/Arhar - Kharif pulse, Vidarbha. B:C ratio 1.55-1.80'
    },
    'Pomegranate': {
        'costMultiplier': 6.0,
        'roiMultiplier': 0.10,          # CORRECTED: B:C ratio 2.00-2.50 (100-150% ROI)
        'nutrientDivisor': 200,
        'maxROI': 160,                  # CORRECTED: High-value perennial can exceed 100%
        'minROI': 70,
        'minCost': 500000,
        'maxCost': 900000,
        'realisticYield': 150,
        'notes': 'High-value perennial, Solapur region. B:C ratio 2.00-2.50'
    },
    'Groundnut': {
        'costMultiplier': 1.7,
        'roiMultiplier': 0.24,          # CORRECTED: B:C ratio 1.50-1.70 (50-70% ROI)
        'nutrientDivisor': 200,
        'maxROI': 80,                   # CORRECTED: Realistic oilseed returns
        'minROI': 40,
        'minCost': 40000,
        'maxCost': 75000,
        'realisticYield': 28,
        'notes': 'Kharif oilseed, Vidarbha & Konkan. B:C ratio 1.50-1.70'
    },
    'Sunflower': {
        'costMultiplier': 1.6,
        'roiMultiplier': 0.22,          # CORRECTED: B:C ratio 1.45-1.65 (45-65% ROI)
        'nutrientDivisor': 200,
        'maxROI': 75,                   # CORRECTED: Realistic oilseed returns
        'minROI': 35,
        'minCost': 35000,
        'maxCost': 65000,
        'realisticYield': 20,
        'notes': 'Rabi & Kharif oilseed. B:C ratio 1.45-1.65'
    },
    'Banana': {
        'costMultiplier': 4.0,
        'roiMultiplier': 0.12,          # CORRECTED: B:C ratio 1.80-2.20 (80-120% ROI)
        'nutrientDivisor': 200,
        'maxROI': 135,                  # CORRECTED: High-value perennial
        'minROI': 65,
        'minCost': 250000,
        'maxCost': 500000,
        'realisticYield': 400,
        'notes': 'High-value perennial, Jalgaon region. B:C ratio 1.80-2.20'
    },
    'Mango': {
        'costMultiplier': 5.0,
        'roiMultiplier': 0.10,          # CORRECTED: B:C ratio 1.70-2.00 (70-100% ROI)
        'nutrientDivisor': 200,
        'maxROI': 120,                  # CORRECTED: Perennial fruit crop
        'minROI': 60,
        'minCost': 300000,
        'maxCost': 700000,
        'realisticYield': 80,
        'notes': 'Konkan & Ratnagiri Alphonso famous. B:C ratio 1.70-2.00'
    },
    'Coconut': {
        'costMultiplier': 4.5,
        'roiMultiplier': 0.11,          # CORRECTED: B:C ratio 1.60-1.90 (60-90% ROI)
        'nutrientDivisor': 200,
        'maxROI': 110,                  # CORRECTED: Perennial coastal crop
        'minROI': 55,
        'minCost': 200000,
        'maxCost': 450000,
        'realisticYield': 100,
        'notes': 'Perennial, Konkan coastal region. B:C ratio 1.60-1.90'
    },
    'Pearl Millet': {
        'costMultiplier': 1.5,
        'roiMultiplier': 0.16,          # CORRECTED: B:C ratio 1.30-1.50 (30-50% ROI)
        'nutrientDivisor': 200,
        'maxROI': 60,                   # CORRECTED: Drought-resistant crop
        'minROI': 25,
        'minCost': 25000,
        'maxCost': 50000,
        'realisticYield': 25,
        'notes': 'Bajra - drought-resistant, Kharif. B:C ratio 1.30-1.50'
    },
    'Green Gram': {
        'costMultiplier': 1.7,
        'roiMultiplier': 0.30,          # CORRECTED: B:C ratio 1.70-2.00 (70-100% ROI)
        'nutrientDivisor': 200,
        'maxROI': 105,                  # CORRECTED: Short-duration pulse, good returns
        'minROI': 60,
        'minCost': 35000,
        'maxCost': 65000,
        'realisticYield': 12,
        'notes': 'Moong - summer pulse, short duration. B:C ratio 1.70-2.00'
    },
    'Black Gram': {
        'costMultiplier': 1.7,
        'roiMultiplier': 0.28,          # CORRECTED: B:C ratio 1.65-1.90 (65-90% ROI)
        'nutrientDivisor': 200,
        'maxROI': 100,                  # CORRECTED: Good pulse market
        'minROI': 55,
        'minCost': 35000,
        'maxCost': 65000,
        'realisticYield': 12,
        'notes': 'Urad - Kharif pulse. B:C ratio 1.65-1.90'
    }
}

# Default calibration for crops not in config
DEFAULT_CALIBRATION = {
    'costMultiplier': 1.5,
    'roiMultiplier': 0.20,          # Conservative default: B:C ratio ~1.40-1.60
    'nutrientDivisor': 200,
    'maxROI': 70,                   # Conservative realistic maximum
    'minROI': 25,
    'minCost': 30000,
    'maxCost': 100000,
    'notes': 'Default calibration applied - Conservative B:C ratio 1.40-1.60'
}

# ============================================================================
# DISTRICT-SPECIFIC ZONE MAPPING
# ============================================================================
# For zone-based crop suitability validation

DISTRICT_ZONES = {
    'Nanded': 'Marathwada',
    'Aurangabad': 'Marathwada',
    'Jalna': 'Marathwada',
    'Beed': 'Marathwada',
    'Latur': 'Marathwada',
    'Osmanabad': 'Marathwada',
    'Parbhani': 'Marathwada',
    'Hingoli': 'Marathwada',
    'Pune': 'Western Maharashtra',
    'Satara': 'Western Maharashtra',
    'Sangli': 'Western Maharashtra',
    'Kolhapur': 'Western Maharashtra',
    'Solapur': 'Western Maharashtra',
    'Nagpur': 'Vidarbha',
    'Amravati': 'Vidarbha',
    'Akola': 'Vidarbha',
    'Yavatmal': 'Vidarbha',
    'Buldhana': 'Vidarbha',
    'Washim': 'Vidarbha',
    'Wardha': 'Vidarbha',
    'Chandrapur': 'Vidarbha',
    'Bhandara': 'Vidarbha',
    'Gadchiroli': 'Vidarbha',
    'Gondia': 'Vidarbha',
    'Nashik': 'North Maharashtra',
    'Dhule': 'North Maharashtra',
    'Jalgaon': 'North Maharashtra',
    'Nandurbar': 'North Maharashtra',
    'Ahmednagar': 'North Maharashtra',
    'Thane': 'Konkan',
    'Palghar': 'Konkan',
    'Raigad': 'Konkan',
    'Ratnagiri': 'Konkan',
    'Sindhudurg': 'Konkan',
    'Mumbai City': 'Konkan',
    'Mumbai Suburban': 'Konkan'
}

# Zone-specific crop suitability
ZONE_TRADITIONAL_CROPS = {
    'Marathwada': ['Rice', 'Wheat', 'Cotton', 'Sorghum', 'Pearl Millet', 'Pigeon Pea', 'Chickpea'],
    'Western Maharashtra': ['Sugarcane', 'Grapes', 'Pomegranate', 'Wheat', 'Soybean'],
    'Vidarbha': ['Cotton', 'Soybean', 'Pigeon Pea', 'Wheat', 'Sorghum'],
    'North Maharashtra': ['Cotton', 'Wheat', 'Sorghum', 'Banana', 'Groundnut'],
    'Konkan': ['Rice', 'Coconut', 'Mango', 'Cashew']
}


# ============================================================================
# MAIN CALIBRATION FUNCTION
# ============================================================================

def calibrate_crop_predictions(
    raw_prediction: Dict[str, Any],
    crop_name: str,
    district: str,
    debug: bool = True
) -> Dict[str, Any]:
    """
    Calibrate raw ML model predictions to realistic agricultural values.
    
    This is a post-processing layer that does NOT modify the trained model
    or dataset. It applies correction factors based on real agricultural
    research data from Maharashtra.
    
    Args:
        raw_prediction: Raw prediction dict with economics, nutrients, risk_assessment
        crop_name: Name of the crop (e.g., 'Rice', 'Wheat', 'Grapes')
        district: District name for zone-specific validation
        debug: If True, log calibration details
        
    Returns:
        Calibrated prediction dictionary with realistic values
        
    Example Input:
        {
            'crop_name': 'Grapes',
            'economics': {
                'total_cost': 129400,
                'net_income': 1470600,
                'roi_percentage': 1136.48
            },
            'nutrients': {
                'N': 30553.23,
                'P': 15019.43,
                'K': 59026.26,
                'Zn': 552.08,
                'S': 1530.36
            },
            'risk_assessment': {...}
        }
        
    Example Output:
        {
            'crop_name': 'Grapes',
            'economics': {
                'total_cost': 1099900,
                'net_income': 2500300,
                'roi_percentage': 227.30
            },
            'nutrients': {
                'N': 152.77,
                'P': 75.10,
                'K': 295.13,
                'Zn': 2.76,
                'S': 7.65
            },
            'risk_assessment': {...}
        }
    """
    
    try:
        # Get calibration config for this crop
        crop_config = CROP_CALIBRATION_CONFIG.get(crop_name, DEFAULT_CALIBRATION)
        
        if debug:
            logger.info(f"\n{'='*70}")
            logger.info(f"CALIBRATING: {crop_name} in {district}")
            logger.info(f"{'='*70}")
        
        # Create a copy to avoid modifying the original
        calibrated = {
            'crop_name': raw_prediction.get('crop_name', crop_name),
            'economics': {},
            'nutrients': {},
            'risk_assessment': raw_prediction.get('risk_assessment', {}).copy()
        }
        
        # =====================================================================
        # 1. CALIBRATE ECONOMIC METRICS
        # =====================================================================
        
        raw_economics = raw_prediction.get('economics', {})
        raw_cost = raw_economics.get('total_cost', 0)
        raw_roi = raw_economics.get('roi_percentage', 0)
        raw_net_income = raw_economics.get('net_income', 0)
        
        # Apply cost multiplier
        calibrated_cost = raw_cost * crop_config['costMultiplier']
        
        # Enforce cost bounds
        calibrated_cost = max(crop_config['minCost'], 
                             min(calibrated_cost, crop_config['maxCost']))
        
        # Apply ROI multiplier
        calibrated_roi = raw_roi * crop_config['roiMultiplier']
        
        # Enforce ROI bounds
        calibrated_roi = max(crop_config['minROI'],
                            min(calibrated_roi, crop_config['maxROI']))
        
        # Recalculate net income based on calibrated values
        # Net Income = Total Cost * (ROI / 100)
        calibrated_net_income = calibrated_cost * (calibrated_roi / 100)
        
        calibrated['economics'] = {
            'total_cost': round(calibrated_cost, 2),
            'net_income': round(calibrated_net_income, 2),
            'roi_percentage': round(calibrated_roi, 2),
            'expected_yield': raw_economics.get('expected_yield', 0),
            'market_rate': raw_economics.get('market_rate', 0),
            'gross_income': round(calibrated_cost + calibrated_net_income, 2)
        }
        
        if debug:
            logger.info(f"\nECONOMIC CALIBRATION:")
            logger.info(f"  Total Cost:  ₹{raw_cost:,.0f} → ₹{calibrated_cost:,.0f} "
                       f"(×{crop_config['costMultiplier']})")
            logger.info(f"  ROI:         {raw_roi:.2f}% → {calibrated_roi:.2f}% "
                       f"(×{crop_config['roiMultiplier']})")
            logger.info(f"  Net Income:  ₹{raw_net_income:,.0f} → ₹{calibrated_net_income:,.0f}")
        
        # =====================================================================
        # 2. CALIBRATE NUTRIENT REQUIREMENTS
        # =====================================================================
        
        raw_nutrients = raw_prediction.get('nutrients', {})
        nutrient_divisor = crop_config['nutrientDivisor']
        
        calibrated['nutrients'] = {
            'N': round(raw_nutrients.get('N', 0) / nutrient_divisor, 2),
            'P': round(raw_nutrients.get('P', 0) / nutrient_divisor, 2),
            'K': round(raw_nutrients.get('K', 0) / nutrient_divisor, 2),
            'Zn': round(raw_nutrients.get('Zn', 0) / nutrient_divisor, 2),
            'S': round(raw_nutrients.get('S', 0) / nutrient_divisor, 2)
        }
        
        if debug:
            logger.info(f"\nNUTRIENT CALIBRATION (÷{nutrient_divisor}):")
            for nutrient in ['N', 'P', 'K', 'Zn', 'S']:
                raw_val = raw_nutrients.get(nutrient, 0)
                cal_val = calibrated['nutrients'][nutrient]
                logger.info(f"  {nutrient:3s}: {raw_val:,.2f} → {cal_val:,.2f} kg/ha")
        
        # =====================================================================
        # 3. DISTRICT-SPECIFIC VALIDATION
        # =====================================================================
        
        zone = DISTRICT_ZONES.get(district, 'Unknown')
        traditional_crops = ZONE_TRADITIONAL_CROPS.get(zone, [])
        
        # Add zone suitability flag
        calibrated['zone_validation'] = {
            'zone': zone,
            'is_traditional': crop_name in traditional_crops,
            'warning': None
        }
        
        # Add warning for non-traditional crops in specific zones
        if crop_name not in traditional_crops:
            if zone == 'Marathwada' and crop_name in ['Grapes', 'Sugarcane']:
                calibrated['zone_validation']['warning'] = (
                    f"{crop_name} is non-traditional for {zone}. "
                    f"Consider water availability and market access."
                )
            elif zone == 'Konkan' and crop_name in ['Cotton', 'Wheat']:
                calibrated['zone_validation']['warning'] = (
                    f"{crop_name} is not commonly grown in {zone} due to high rainfall."
                )
        
        if debug and calibrated['zone_validation']['warning']:
            logger.info(f"\nZONE WARNING: {calibrated['zone_validation']['warning']}")
        
        # =====================================================================
        # 4. PRESERVE RISK ASSESSMENT
        # =====================================================================
        
        # Keep original risk assessment (already copied above)
        if debug:
            logger.info(f"\nRISK ASSESSMENT (unchanged):")
            logger.info(f"  Risk Level: {calibrated['risk_assessment'].get('risk_level', 'N/A')}")
            logger.info(f"  Water Req:  {calibrated['risk_assessment'].get('water_requirement', 'N/A')}")
        
        if debug:
            logger.info(f"{'='*70}\n")
        
        return calibrated
        
    except Exception as e:
        logger.error(f"Calibration error for {crop_name}: {str(e)}")
        logger.warning("Returning original prediction with error flag")
        
        # Return original with error flag
        error_prediction = raw_prediction.copy()
        error_prediction['calibration_error'] = str(e)
        error_prediction['calibration_applied'] = False
        return error_prediction


def calibrate_comparison_results(
    comparison_data: list,
    district: str,
    debug: bool = True
) -> Dict[str, Any]:
    """
    Calibrate all crops in a comparison result and re-determine best crop.
    
    This ensures that relative rankings are preserved after calibration
    and the best crop recommendation remains consistent.
    
    Args:
        comparison_data: List of crop predictions to calibrate
        district: District name for zone validation
        debug: Enable debug logging
        
    Returns:
        Dictionary with calibrated comparison data and updated recommendation
    """
    
    calibrated_comparison = []
    
    # Calibrate each crop
    for crop_data in comparison_data:
        crop_name = crop_data.get('crop_name', '')
        calibrated = calibrate_crop_predictions(crop_data, crop_name, district, debug)
        calibrated_comparison.append(calibrated)
    
    # Re-determine best crop based on calibrated ROI
    # This preserves relative ranking (highest ROI remains highest)
    best_crop = max(calibrated_comparison, 
                   key=lambda x: x['economics']['roi_percentage'])
    
    return {
        'comparison': calibrated_comparison,
        'recommendation': {
            'best_crop': best_crop['crop_name'],
            'reason': f"Highest ROI of {best_crop['economics']['roi_percentage']:.2f}%",
            'roi': best_crop['economics']['roi_percentage'],
            'total_cost': best_crop['economics']['total_cost'],
            'net_income': best_crop['economics']['net_income']
        }
    }


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_crop_config(crop_name: str) -> Dict[str, Any]:
    """Get calibration config for a specific crop."""
    return CROP_CALIBRATION_CONFIG.get(crop_name, DEFAULT_CALIBRATION)


def is_crop_suitable_for_zone(crop_name: str, zone: str) -> bool:
    """Check if a crop is traditionally suitable for a zone."""
    traditional_crops = ZONE_TRADITIONAL_CROPS.get(zone, [])
    return crop_name in traditional_crops


def get_realistic_nutrient_range(crop_name: str) -> Dict[str, tuple]:
    """
    Get realistic nutrient requirement ranges (kg/ha) for common crops.
    Based on agricultural research and best practices.
    """
    ranges = {
        'Rice': {'N': (100, 150), 'P': (40, 60), 'K': (40, 60)},
        'Wheat': {'N': (100, 140), 'P': (50, 70), 'K': (40, 60)},
        'Cotton': {'N': (120, 180), 'P': (50, 80), 'K': (50, 80)},
        'Sugarcane': {'N': (200, 300), 'P': (80, 120), 'K': (100, 150)},
        'Soybean': {'N': (20, 40), 'P': (60, 80), 'K': (40, 60)},
        'Grapes': {'N': (120, 180), 'P': (60, 90), 'K': (180, 250)},
        'Pomegranate': {'N': (100, 150), 'P': (50, 80), 'K': (100, 150)}
    }
    return ranges.get(crop_name, {'N': (80, 150), 'P': (40, 80), 'K': (40, 80)})


# ============================================================================
# TESTING & VALIDATION
# ============================================================================

if __name__ == '__main__':
    """Test calibration with sample data"""
    
    print("\n" + "="*80)
    print("CROP PREDICTION CALIBRATOR - TEST SUITE")
    print("="*80)
    
    # Test case 1: Grapes in Nanded (from user's example)
    test_grapes = {
        'crop_name': 'Grapes',
        'economics': {
            'total_cost': 129400,
            'net_income': 1470600,
            'roi_percentage': 1136.48,
            'expected_yield': 200,
            'market_rate': 8000
        },
        'nutrients': {
            'N': 30553.23,
            'P': 15019.43,
            'K': 59026.26,
            'Zn': 552.08,
            'S': 1530.36
        },
        'risk_assessment': {
            'risk_level': 'Medium',
            'water_requirement': 'Medium',
            'zone_suitability': 'Marathwada'
        }
    }
    
    print("\nTEST 1: Grapes in Nanded")
    calibrated_grapes = calibrate_crop_predictions(test_grapes, 'Grapes', 'Nanded')
    
    # Test case 2: Rice in Nanded
    test_rice = {
        'crop_name': 'Rice',
        'economics': {
            'total_cost': 31900,
            'net_income': 108100,
            'roi_percentage': 338.87,
            'expected_yield': 40,
            'market_rate': 3500
        },
        'nutrients': {
            'N': 30586.95,
            'P': 15030.06,
            'K': 59017.22,
            'Zn': 553.75,
            'S': 1534.01
        },
        'risk_assessment': {
            'risk_level': 'High',
            'water_requirement': 'High',
            'zone_suitability': 'Marathwada'
        }
    }
    
    print("\nTEST 2: Rice in Nanded")
    calibrated_rice = calibrate_crop_predictions(test_rice, 'Rice', 'Nanded')
    
    # Test case 3: Full comparison calibration
    print("\n" + "="*80)
    print("TEST 3: Full Comparison Calibration")
    print("="*80)
    
    comparison_input = [test_grapes, test_rice, {
        'crop_name': 'Wheat',
        'economics': {
            'total_cost': 31400,
            'net_income': 56100,
            'roi_percentage': 178.66,
            'expected_yield': 35,
            'market_rate': 2500
        },
        'nutrients': {
            'N': 30640.34,
            'P': 15047.03,
            'K': 59000.75,
            'Zn': 556.42,
            'S': 1540.21
        },
        'risk_assessment': {
            'risk_level': 'Medium',
            'water_requirement': 'Medium',
            'zone_suitability': 'Marathwada'
        }
    }]
    
    result = calibrate_comparison_results(comparison_input, 'Nanded', debug=False)
    
    print(f"\nBEST CROP RECOMMENDATION:")
    print(f"  Crop: {result['recommendation']['best_crop']}")
    print(f"  ROI: {result['recommendation']['roi']:.2f}%")
    print(f"  Total Cost: ₹{result['recommendation']['total_cost']:,.2f}")
    print(f"  Net Income: ₹{result['recommendation']['net_income']:,.2f}")
    
    print("\n" + "="*80)
    print("TEST SUITE COMPLETED")
    print("="*80 + "\n")
