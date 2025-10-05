"""
Test script for validation layer
Tests the examples from requirements:
✓ Raigad + Laterite + Monsoon → Should recommend: Rice, Coconut, Mango (NOT Grapes)
✓ Latur + Black + Semi-Arid → Should recommend: Sorghum, Bajra, Cotton (NOT Coconut)
✓ Nashik + Black + Moderate Rainfall → Should recommend: Grapes, Onion, Sugarcane
✓ Nagpur + Black + Post-Monsoon → Should recommend: Cotton, Soybean, Wheat
"""

import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from validation import validate_prediction, get_alternative_crops, filter_invalid_crops

def test_validation():
    """Run validation tests"""
    
    print("="*80)
    print("VALIDATION LAYER TESTING")
    print("Testing examples from requirements")
    print("="*80)
    
    test_cases = [
        {
            'name': 'Raigad Coastal - Should allow Rice/Coconut/Mango, NOT Grapes',
            'district': 'Raigad',
            'soil': 'Laterite',
            'weather': 'Monsoon',
            'expected_valid': ['Rice', 'Coconut', 'Mango'],
            'expected_invalid': ['Grapes', 'Cotton', 'Wheat']
        },
        {
            'name': 'Latur Drought - Should allow Sorghum/Cotton, NOT Coconut',
            'district': 'Latur',
            'soil': 'Black',
            'weather': 'Semi-Arid',
            'expected_valid': ['Sorghum', 'Cotton', 'Chickpea'],
            'expected_invalid': ['Coconut', 'Rice', 'Banana']
        },
        {
            'name': 'Nashik Grape Belt - Should allow Grapes/Onion',
            'district': 'Nashik',
            'soil': 'Black',
            'weather': 'Moderate Rainfall',
            'expected_valid': ['Grapes', 'Onion', 'Cotton'],
            'expected_invalid': ['Coconut', 'Cashew']
        },
        {
            'name': 'Nagpur Cotton Belt - Should allow Cotton/Soybean/Wheat',
            'district': 'Nagpur',
            'soil': 'Black',
            'weather': 'Post-Monsoon',
            'expected_valid': ['Cotton', 'Soybean', 'Wheat'],
            'expected_invalid': ['Grapes', 'Coconut', 'Cashew']
        }
    ]
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"TEST {i}: {test['name']}")
        print(f"{'='*80}")
        print(f"Location: {test['district']}")
        print(f"Soil: {test['soil']}")
        print(f"Weather: {test['weather']}")
        
        # Get valid crops
        valid_crops = get_alternative_crops(test['district'], test['soil'], test['weather'])
        
        print(f"\nValid crops for this location ({len(valid_crops)}):")
        print(f"  {', '.join(sorted(valid_crops))}")
        
        # Test expected valid crops
        print(f"\nExpected VALID crops:")
        all_valid = True
        for crop in test['expected_valid']:
            is_valid = crop in valid_crops
            status = "✓" if is_valid else "✗"
            print(f"  {status} {crop}: {'Allowed' if is_valid else 'BLOCKED (ERROR!)'}")
            if not is_valid:
                all_valid = False
                # Show why it's blocked
                result = validate_prediction(test['district'], test['soil'], crop, test['weather'])
                print(f"      Reason: {', '.join(result['errors'])}")
        
        # Test expected invalid crops
        print(f"\nExpected INVALID crops (should be blocked):")
        all_invalid_blocked = True
        for crop in test['expected_invalid']:
            is_blocked = crop not in valid_crops
            status = "✓" if is_blocked else "✗"
            print(f"  {status} {crop}: {'Blocked' if is_blocked else 'ALLOWED (ERROR!)'}")
            if not is_blocked:
                all_invalid_blocked = False
        
        # Test detailed validation on one valid crop
        if test['expected_valid']:
            test_crop = test['expected_valid'][0]
            print(f"\nDetailed validation for {test_crop}:")
            result = validate_prediction(test['district'], test['soil'], test_crop, test['weather'])
            print(f"  Region: {result['region']}")
            print(f"  Valid: {result['is_valid']}")
            print(f"  Reasoning: {result['reasoning']}")
            
            for check in result['checks']:
                status = "✓" if check['passed'] else "✗"
                print(f"  {status} {check['check']}: {check['message']}")
        
        # Overall test result
        test_passed = all_valid and all_invalid_blocked
        if test_passed:
            print(f"\n✓✓✓ TEST {i} PASSED ✓✓✓")
            passed += 1
        else:
            print(f"\n✗✗✗ TEST {i} FAILED ✗✗✗")
            failed += 1
    
    # Summary
    print(f"\n{'='*80}")
    print(f"VALIDATION TEST SUMMARY")
    print(f"{'='*80}")
    print(f"Total tests: {len(test_cases)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print(f"\n✓✓✓ ALL VALIDATION TESTS PASSED ✓✓✓")
        print("The validation layer is working correctly!")
    else:
        print(f"\n⚠ SOME TESTS FAILED")
        print("Please review the validation rules.")
    
    print(f"{'='*80}\n")
    
    return failed == 0


def test_filtering():
    """Test the filter function with mock predictions"""
    
    print("="*80)
    print("TESTING PREDICTION FILTERING")
    print("="*80)
    
    # Mock predictions for Raigad (should filter out Grapes)
    print("\nTest: Raigad + Laterite + Monsoon")
    print("Mock predictions from model:")
    
    mock_predictions = [
        ('Rice', 0.85),
        ('Coconut', 0.70),
        ('Grapes', 0.65),  # Should be filtered out
        ('Mango', 0.60),
        ('Cotton', 0.55),  # Should be filtered out
    ]
    
    for crop, prob in mock_predictions:
        print(f"  {crop}: {prob*100:.1f}%")
    
    # Filter
    filtered = filter_invalid_crops(mock_predictions, 'Raigad', 'Laterite', 'Monsoon')
    
    print(f"\nFiltered predictions (valid only):")
    for pred in filtered:
        print(f"  ✓ {pred['crop']}: {pred['probability']*100:.1f}%")
        print(f"    Reasoning: {pred['validation']['reasoning']}")
    
    # Check if filtering worked
    filtered_crops = [p['crop'] for p in filtered]
    if 'Grapes' not in filtered_crops and 'Cotton' not in filtered_crops:
        print(f"\n✓ Filtering worked! Grapes and Cotton were correctly filtered out.")
        return True
    else:
        print(f"\n✗ Filtering failed! Invalid crops were not removed.")
        return False


if __name__ == "__main__":
    print("\n")
    print("█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + "  MAHARASHTRA SMART FARMER - VALIDATION TESTING  ".center(78) + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)
    print("\n")
    
    # Run tests
    validation_passed = test_validation()
    print("\n")
    filtering_passed = test_filtering()
    
    # Final result
    print("\n")
    print("="*80)
    print("FINAL TEST RESULTS")
    print("="*80)
    
    if validation_passed and filtering_passed:
        print("✓✓✓ ALL TESTS PASSED ✓✓✓")
        print("\nThe system is ready for use with:")
        print("  - Scientific crop-district-soil compatibility")
        print("  - Regional constraint enforcement (0% violations)")
        print("  - Accurate recommendations based on research data")
        print("\nNext steps:")
        print("  1. Run: python train_models_research.py")
        print("  2. Run: python app.py")
        print("  3. Test with frontend")
    else:
        print("⚠ SOME TESTS FAILED")
        print("Please review the validation configuration.")
    
    print("="*80)
    print("\n")
