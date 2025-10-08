"""
Utility modules for Smart Farmer Recommender System
"""

from .crop_prediction_calibrator import (
    calibrate_crop_predictions,
    calibrate_comparison_results,
    get_crop_config,
    is_crop_suitable_for_zone,
    get_realistic_nutrient_range,
    CROP_CALIBRATION_CONFIG
)

from .crop_suitability_validator import (
    validate_crop_suitability,
    validate_crop_comparison,
    get_zone_from_district,
    get_traditional_crops_for_district
)

__all__ = [
    # Calibration functions
    'calibrate_crop_predictions',
    'calibrate_comparison_results',
    'get_crop_config',
    'is_crop_suitable_for_zone',
    'get_realistic_nutrient_range',
    'CROP_CALIBRATION_CONFIG',
    # Suitability validation functions
    'validate_crop_suitability',
    'validate_crop_comparison',
    'get_zone_from_district',
    'get_traditional_crops_for_district'
]
