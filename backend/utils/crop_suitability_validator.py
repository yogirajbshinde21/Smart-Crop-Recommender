"""
Crop Suitability Validator - Post-Processing Validation Layer
==============================================================

This module validates crop suitability for specific districts/zones and provides
intelligent warnings and recommendations WITHOUT modifying ML model predictions.

Features:
- District-wise traditional crop validation
- Irrigation requirement compatibility checking
- Zone-specific risk assessment
- Contextual warning messages
- Alternative crop recommendations

Author: Smart Farmer System
Date: October 2025
"""

import logging
from typing import Dict, Any, List, Optional
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import configuration data
from config import (
    DISTRICT_TRADITIONAL_CROPS,
    CROP_IRRIGATION_NEEDS,
    ZONE_CONSTRAINTS,
    AGRICULTURAL_ZONES
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# WARNING MESSAGE TEMPLATES
# ============================================================================

WARNING_TEMPLATES = {
    'high_risk': {
        'Grapes_Marathwada': """⚠️ HIGH RISK: Grapes are non-traditional for {district} (Marathwada zone)

Challenges:
• Requires 800-1000mm supplemental irrigation; Marathwada has only 15-20% irrigation coverage
• High initial investment (₹10-12 lakhs/ha) in drought-prone region
• Market distance: Major grape mandis are in Nashik/Sangli (300+ km away)
• Water scarcity during critical growth stages (flowering, fruit development)

Consider instead: Sorghum, Cotton, Pomegranate (drought-tolerant), Pigeon Pea

Success conditions if you proceed:
• Assured drip irrigation system with backup water source
• Minimum 5-acre plot for commercial viability
• Cold storage facility within 50km
• Reliable groundwater or canal irrigation access""",
        
        'Sugarcane_Marathwada': """⚠️ HIGH RISK: Sugarcane requires very high water in water-scarce Marathwada

Critical Issues:
• Water requirement: 2000-2500mm vs. Marathwada rainfall: 600-900mm
• This crop has contributed to severe groundwater depletion in the region
• Unsustainable in drought-prone areas without perennial water source

Strongly Recommended: Drought-resilient crops like Sorghum, Pearl Millet, Chickpea, Cotton

Note: Several districts in Marathwada have banned/restricted sugarcane due to water crisis""",
        
        'Banana_Marathwada': """⚠️ HIGH RISK: Banana requires high water and continuous irrigation

Water Requirement: 1800-2000mm per year
Region Reality: 600-900mm rainfall, limited irrigation

Recommended Alternatives: Pomegranate (adapted to region), Cotton, Sorghum""",
        
        'Rice_Western_Maharashtra': """⚠️ ADVISORY: Rice requires very high water; region is better suited for other crops

Western Maharashtra specializes in:
• Sugarcane (with canal irrigation)
• Grapes (high-value, drip irrigation)
• Pomegranate (drought-adapted)
• Wheat (Rabi season)

Rice cultivation here may face water competition from sugarcane""",
        
        'default': """⚠️ HIGH RISK: {crop} is challenging for {zone} region

This crop requires: {irrigation} irrigation
Region water availability: {water_availability}

Risk Factors: {risk_factors}

Consider traditional crops: {suitable_crops}"""
    },
    
    'caution': {
        'default': """⚠️ CAUTION: {crop} is not commonly grown in {district}

While possible, this crop may face challenges:
• {risk_factors}

Success requires:
• {success_conditions}

Alternative options: {recommendations}"""
    },
    
    'advisory': {
        'default': """ℹ️ ADVISORY: {crop} is not traditionally grown in {district}

This region typically grows: {traditional_crops}

If pursuing {crop}:
• Ensure irrigation availability matches crop needs ({irrigation} requirement)
• Consult local agricultural extension officers
• Consider market access and transportation

Suitability score: {suitability_score}/100"""
    }
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_zone_from_district(district: str) -> Optional[str]:
    """
    Returns the agricultural zone for a given district.
    
    Args:
        district: District name (e.g., 'Nanded', 'Pune')
        
    Returns:
        Zone name or None if district not found
    """
    for zone, districts in AGRICULTURAL_ZONES.items():
        if district in districts:
            return zone
    return None


def get_traditional_crops_for_district(district: str) -> List[str]:
    """
    Get list of traditional crops for a district.
    
    Args:
        district: District name
        
    Returns:
        List of traditional crop names
    """
    return DISTRICT_TRADITIONAL_CROPS.get(district, [])


def get_zone_constraints(zone: str) -> Dict[str, Any]:
    """
    Get constraints and characteristics for a zone.
    
    Args:
        zone: Zone name
        
    Returns:
        Dictionary of zone constraints
    """
    return ZONE_CONSTRAINTS.get(zone, {})


# ============================================================================
# MAIN VALIDATION FUNCTION
# ============================================================================

def validate_crop_suitability(
    crop_name: str,
    district: str,
    zone: Optional[str] = None,
    debug: bool = False
) -> Dict[str, Any]:
    """
    Validates if a crop is suitable for the given district/zone.
    
    This is a post-processing validation layer that does NOT affect
    ML model predictions. It provides contextual warnings and recommendations
    based on Maharashtra agricultural data.
    
    Args:
        crop_name: Name of the crop (e.g., 'Grapes', 'Rice')
        district: District name (e.g., 'Nanded', 'Pune')
        zone: Agricultural zone (optional, will be determined from district)
        debug: Enable debug logging
        
    Returns:
        Dictionary with validation results:
        {
            'is_traditional': bool,
            'suitability_score': int (0-100),
            'warning_level': 'none' | 'advisory' | 'caution' | 'high_risk',
            'warning_message': str,
            'recommendations': list[str],
            'risk_factors': list[str],
            'success_conditions': list[str],
            'zone': str,
            'irrigation_compatibility': str
        }
    """
    
    try:
        # Determine zone if not provided
        if zone is None:
            zone = get_zone_from_district(district)
            if zone is None:
                logger.warning(f"District '{district}' not found in zone mapping")
                return _get_default_validation(crop_name, district)
        
        if debug:
            logger.info(f"\n{'='*70}")
            logger.info(f"VALIDATING: {crop_name} in {district} ({zone})")
            logger.info(f"{'='*70}")
        
        # Get traditional crops for district
        traditional_crops = get_traditional_crops_for_district(district)
        is_traditional = crop_name in traditional_crops
        
        # Get zone constraints
        zone_constraints = get_zone_constraints(zone)
        suitable_crops = zone_constraints.get('suitable_crops', [])
        challenging_crops = zone_constraints.get('challenging_crops', [])
        risk_factors = zone_constraints.get('risk_factors', [])
        
        # Get irrigation requirements
        crop_irrigation = CROP_IRRIGATION_NEEDS.get(crop_name, 'Medium')
        water_availability = zone_constraints.get('water_availability', 'Medium')
        
        # Initialize result
        result = {
            'is_traditional': is_traditional,
            'zone': zone,
            'irrigation_requirement': crop_irrigation,
            'water_availability': water_availability,
            'recommendations': [],
            'risk_factors': [],
            'success_conditions': []
        }
        
        # =====================================================================
        # DETERMINE WARNING LEVEL AND SUITABILITY SCORE
        # =====================================================================
        
        if is_traditional:
            # Traditional crop - no warnings
            result['warning_level'] = 'none'
            result['suitability_score'] = 95
            result['warning_message'] = f"✅ {crop_name} is traditionally grown in {district}"
            result['irrigation_compatibility'] = 'Compatible'
            
            if debug:
                logger.info(f"✅ Traditional crop - High suitability")
        
        elif crop_name in challenging_crops:
            # High risk - crop is specifically challenging for this zone
            result['warning_level'] = 'high_risk'
            result['suitability_score'] = 30
            result['risk_factors'] = risk_factors.copy()
            result['irrigation_compatibility'] = 'Incompatible'
            
            # Get specific warning message template
            template_key = f"{crop_name}_{zone}"
            if template_key in WARNING_TEMPLATES['high_risk']:
                result['warning_message'] = WARNING_TEMPLATES['high_risk'][template_key].format(
                    crop=crop_name,
                    district=district,
                    zone=zone
                )
            else:
                result['warning_message'] = WARNING_TEMPLATES['high_risk']['default'].format(
                    crop=crop_name,
                    zone=zone,
                    irrigation=crop_irrigation,
                    water_availability=water_availability,
                    risk_factors=', '.join(risk_factors),
                    suitable_crops=', '.join(suitable_crops[:4])
                )
            
            # Add recommendations from suitable crops
            result['recommendations'] = [
                f"{crop} (traditional, {CROP_IRRIGATION_NEEDS.get(crop, 'Medium')} water)"
                for crop in suitable_crops[:4]
            ]
            
            # Add success conditions
            result['success_conditions'] = [
                "Assured irrigation system with backup",
                "Minimum viable plot size (3-5 acres)",
                "Market access and transportation",
                "Technical knowledge or extension support"
            ]
            
            if debug:
                logger.info(f"⚠️  HIGH RISK - Challenging crop for zone")
        
        elif crop_irrigation in ['Very High', 'High'] and water_availability == 'Low':
            # Caution - high water crop in low water zone
            result['warning_level'] = 'caution'
            result['suitability_score'] = 50
            result['risk_factors'] = [
                f"Crop requires {crop_irrigation} irrigation",
                f"Zone has {water_availability} water availability",
                "Potential water stress during critical growth stages"
            ]
            result['irrigation_compatibility'] = 'Marginal'
            
            result['warning_message'] = f"""⚠️ CAUTION: {crop_name} requires {crop_irrigation} irrigation

Region: {district} ({zone})
Water Availability: {water_availability}
Irrigation Coverage: {zone_constraints.get('irrigation_coverage', 'Limited')}

Risk Factors:
{chr(10).join('• ' + rf for rf in result['risk_factors'])}

Success requires:
• Assured irrigation source (drip/sprinkler recommended)
• Water availability during critical crop stages
• Backup water arrangement for dry spells

Traditional alternatives: {', '.join(traditional_crops[:4])}"""
            
            result['recommendations'] = traditional_crops[:4]
            result['success_conditions'] = [
                "Reliable irrigation system",
                "Adequate water storage",
                "Regular monitoring and maintenance"
            ]
            
            if debug:
                logger.info(f"⚠️  CAUTION - Irrigation mismatch")
        
        else:
            # Advisory - not traditional but potentially viable
            result['warning_level'] = 'advisory'
            result['suitability_score'] = 70
            result['irrigation_compatibility'] = 'Moderate'
            
            result['warning_message'] = WARNING_TEMPLATES['advisory']['default'].format(
                crop=crop_name,
                district=district,
                traditional_crops=', '.join(traditional_crops[:4]),
                irrigation=crop_irrigation,
                suitability_score=result['suitability_score']
            )
            
            result['recommendations'] = traditional_crops[:3]
            result['success_conditions'] = [
                "Consult local agricultural extension officers",
                "Ensure irrigation matches crop requirements",
                "Verify market access and pricing"
            ]
            
            if debug:
                logger.info(f"ℹ️  ADVISORY - Non-traditional but potentially viable")
        
        # =====================================================================
        # ADD ADDITIONAL CONTEXT
        # =====================================================================
        
        # Add irrigation requirement details
        irrigation_details = {
            'Very High': '2000-2500mm per year',
            'High': '1000-1500mm per year',
            'Medium': '600-1000mm per year',
            'Low': '400-600mm per year (rain-fed possible)'
        }
        result['irrigation_details'] = irrigation_details.get(crop_irrigation, 'Variable')
        
        # Add zone characteristics
        result['zone_characteristics'] = {
            'rainfall': zone_constraints.get('rainfall', 'N/A'),
            'irrigation_coverage': zone_constraints.get('irrigation_coverage', 'N/A'),
            'water_availability': water_availability
        }
        
        if debug:
            logger.info(f"\nSuitability Score: {result['suitability_score']}/100")
            logger.info(f"Warning Level: {result['warning_level']}")
            logger.info(f"Irrigation: {crop_irrigation} (crop) vs {water_availability} (zone)")
            logger.info(f"{'='*70}\n")
        
        return result
        
    except Exception as e:
        logger.error(f"Error validating crop suitability: {str(e)}")
        return _get_default_validation(crop_name, district, error=str(e))


def _get_default_validation(
    crop_name: str,
    district: str,
    error: Optional[str] = None
) -> Dict[str, Any]:
    """
    Returns default validation result when error occurs or data is missing.
    
    Args:
        crop_name: Crop name
        district: District name
        error: Error message if applicable
        
    Returns:
        Default validation dictionary
    """
    return {
        'is_traditional': False,
        'suitability_score': 50,
        'warning_level': 'advisory',
        'warning_message': f"ℹ️ Limited suitability data available for {crop_name} in {district}. Consult local agricultural experts.",
        'recommendations': [],
        'risk_factors': ['Limited validation data available'],
        'success_conditions': ['Consult local agricultural extension officers'],
        'zone': 'Unknown',
        'irrigation_requirement': 'Medium',
        'water_availability': 'Unknown',
        'irrigation_compatibility': 'Unknown',
        'validation_error': error
    }


# ============================================================================
# BATCH VALIDATION FOR COMPARISON
# ============================================================================

def validate_crop_comparison(
    crops: List[str],
    district: str,
    zone: Optional[str] = None,
    debug: bool = False
) -> Dict[str, Dict[str, Any]]:
    """
    Validates multiple crops for comparison.
    
    Args:
        crops: List of crop names
        district: District name
        zone: Agricultural zone (optional)
        debug: Enable debug logging
        
    Returns:
        Dictionary mapping crop names to validation results
    """
    
    if zone is None:
        zone = get_zone_from_district(district)
    
    results = {}
    for crop in crops:
        results[crop] = validate_crop_suitability(crop, district, zone, debug)
    
    return results


# ============================================================================
# TESTING
# ============================================================================

if __name__ == '__main__':
    """Test crop suitability validation"""
    
    print("\n" + "="*80)
    print("CROP SUITABILITY VALIDATOR - TEST SUITE")
    print("="*80)
    
    # Test Case 1: Grapes in Nanded (Marathwada) - Should show HIGH RISK
    print("\nTEST 1: Grapes in Nanded (Marathwada)")
    print("-" * 80)
    result1 = validate_crop_suitability('Grapes', 'Nanded', debug=True)
    print(f"Warning Level: {result1['warning_level']}")
    print(f"Suitability Score: {result1['suitability_score']}/100")
    print(f"\n{result1['warning_message']}")
    
    # Test Case 2: Sorghum in Nanded - Should show NO WARNING
    print("\n" + "="*80)
    print("\nTEST 2: Sorghum in Nanded (Traditional Crop)")
    print("-" * 80)
    result2 = validate_crop_suitability('Sorghum', 'Nanded', debug=True)
    print(f"Warning Level: {result2['warning_level']}")
    print(f"Suitability Score: {result2['suitability_score']}/100")
    print(f"\n{result2['warning_message']}")
    
    # Test Case 3: Grapes in Sangli (Western Maharashtra) - Should show NO WARNING
    print("\n" + "="*80)
    print("\nTEST 3: Grapes in Sangli (Western Maharashtra - Traditional)")
    print("-" * 80)
    result3 = validate_crop_suitability('Grapes', 'Sangli', debug=True)
    print(f"Warning Level: {result3['warning_level']}")
    print(f"Suitability Score: {result3['suitability_score']}/100")
    print(f"\n{result3['warning_message']}")
    
    # Test Case 4: Batch validation
    print("\n" + "="*80)
    print("\nTEST 4: Batch Validation - Multiple Crops in Nanded")
    print("-" * 80)
    batch_results = validate_crop_comparison(
        crops=['Grapes', 'Rice', 'Wheat', 'Cotton', 'Sorghum'],
        district='Nanded',
        debug=False
    )
    
    for crop, result in batch_results.items():
        status_icon = {
            'none': '✅',
            'advisory': 'ℹ️',
            'caution': '⚠️',
            'high_risk': '🚫'
        }.get(result['warning_level'], '❓')
        
        print(f"\n{status_icon} {crop}:")
        print(f"   Level: {result['warning_level']}")
        print(f"   Score: {result['suitability_score']}/100")
        print(f"   Traditional: {result['is_traditional']}")
    
    print("\n" + "="*80)
    print("TEST SUITE COMPLETED")
    print("="*80 + "\n")
