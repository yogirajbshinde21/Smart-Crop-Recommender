"""
Test Script for Crop Comparison with Calibration
=================================================

This script tests the /compare-crops endpoint with the new calibration system.

Usage:
    python test_calibration_api.py
"""

import requests
import json
from typing import Dict, Any

# API Configuration
BASE_URL = "http://localhost:5000"
COMPARE_CROPS_ENDPOINT = f"{BASE_URL}/compare-crops"

def print_header(text: str, char: str = "=", width: int = 80):
    """Print formatted header"""
    print(f"\n{char * width}")
    print(f"{text.center(width)}")
    print(f"{char * width}\n")

def print_crop_details(crop: Dict[str, Any], is_best: bool = False):
    """Print formatted crop details"""
    marker = "🏆 " if is_best else "   "
    print(f"{marker}{crop['crop_name']}")
    print(f"{'─' * 70}")
    
    # Economics
    econ = crop['economics']
    print(f"  💰 Economics:")
    print(f"     Total Cost:  ₹{econ['total_cost']:,.2f}/ha")
    print(f"     Net Income:  ₹{econ['net_income']:,.2f}/ha")
    print(f"     ROI:         {econ['roi_percentage']:.2f}%")
    print(f"     Yield:       {econ['expected_yield']} quintal/ha")
    print(f"     Market Rate: ₹{econ['market_rate']}/quintal")
    
    # Nutrients
    nutrients = crop['nutrients']
    print(f"  🌱 Nutrient Requirements:")
    print(f"     N:  {nutrients['N']:>7.2f} kg/ha")
    print(f"     P:  {nutrients['P']:>7.2f} kg/ha")
    print(f"     K:  {nutrients['K']:>7.2f} kg/ha")
    print(f"     Zn: {nutrients['Zn']:>7.2f} kg/ha")
    print(f"     S:  {nutrients['S']:>7.2f} kg/ha")
    
    # Risk Assessment
    risk = crop['risk_assessment']
    print(f"  ⚠️  Risk Assessment:")
    print(f"     Risk Level:  {risk['risk_level']}")
    print(f"     Water Need:  {risk['water_requirement']}")
    print(f"     Zone:        {risk['zone_suitability']}")
    
    # Zone Validation
    if 'zone_validation' in crop:
        zone_val = crop['zone_validation']
        print(f"  📍 Zone Validation:")
        print(f"     Traditional: {'Yes' if zone_val['is_traditional'] else 'No'}")
        if zone_val.get('warning'):
            print(f"     ⚠️  Warning: {zone_val['warning']}")
    
    print()

def test_compare_crops(
    crops: list,
    district: str,
    soil_type: str,
    weather: str
):
    """Test the compare-crops endpoint with calibration"""
    
    print_header("CROP COMPARISON TEST WITH CALIBRATION", "=")
    
    # Prepare request
    payload = {
        "crops": crops,
        "District": district,
        "Soil_Type": soil_type,
        "Weather": weather
    }
    
    print("📤 Request Payload:")
    print(f"   Crops:     {', '.join(crops)}")
    print(f"   District:  {district}")
    print(f"   Soil Type: {soil_type}")
    print(f"   Weather:   {weather}")
    
    try:
        # Make request
        print(f"\n🌐 Sending POST request to {COMPARE_CROPS_ENDPOINT}...")
        response = requests.post(
            COMPARE_CROPS_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        # Check response
        print(f"📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                result_data = data['data']
                
                # Print calibration info
                if result_data.get('calibration_applied'):
                    print_header("CALIBRATION APPLIED", "✓")
                    print(f"ℹ️  {result_data.get('calibration_note', 'N/A')}")
                
                # Print recommendation
                recommendation = result_data['recommendation']
                print_header("BEST CROP RECOMMENDATION", "🌟")
                print(f"  🏆 Best Crop:  {recommendation['best_crop']}")
                print(f"  📊 ROI:        {recommendation['roi']:.2f}%")
                print(f"  💵 Total Cost: ₹{recommendation['total_cost']:,.2f}")
                print(f"  💰 Net Income: ₹{recommendation['net_income']:,.2f}")
                print(f"  📝 Reason:     {recommendation['reason']}")
                
                # Print zone warnings if any
                if 'zone_warnings' in result_data and result_data['zone_warnings']:
                    print_header("ZONE WARNINGS", "⚠️")
                    for warning in result_data['zone_warnings']:
                        print(f"  ⚠️  {warning['crop']}: {warning['warning']}")
                
                # Print detailed comparison
                print_header("DETAILED CROP COMPARISON", "📊")
                best_crop_name = recommendation['best_crop']
                
                for crop in result_data['comparison']:
                    is_best = crop['crop_name'] == best_crop_name
                    print_crop_details(crop, is_best)
                
                # Print summary statistics
                print_header("SUMMARY STATISTICS", "📈")
                all_rois = [c['economics']['roi_percentage'] for c in result_data['comparison']]
                all_costs = [c['economics']['total_cost'] for c in result_data['comparison']]
                
                print(f"  Number of Crops Compared: {len(result_data['comparison'])}")
                print(f"  Average ROI:              {sum(all_rois)/len(all_rois):.2f}%")
                print(f"  ROI Range:                {min(all_rois):.2f}% - {max(all_rois):.2f}%")
                print(f"  Average Cost:             ₹{sum(all_costs)/len(all_costs):,.2f}")
                print(f"  Cost Range:               ₹{min(all_costs):,.2f} - ₹{max(all_costs):,.2f}")
                
                print_header("TEST PASSED ✅", "=")
                return True
            else:
                print(f"\n❌ API returned success=false")
                print(f"Error: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"\n❌ HTTP Error {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection Error: Could not connect to the API server")
        print("   Make sure the backend server is running on http://localhost:5000")
        return False
    except requests.exceptions.Timeout:
        print("\n❌ Timeout Error: Request took too long")
        return False
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def run_test_suite():
    """Run a suite of tests"""
    
    print_header("CROP CALIBRATION API TEST SUITE", "═")
    print("Testing the /compare-crops endpoint with calibration system")
    print("Ensure backend server is running before proceeding")
    
    input("\nPress Enter to start tests...")
    
    # Test Case 1: Original user scenario (Grapes, Rice, Wheat in Nanded)
    print_header("TEST CASE 1: Nanded District - Grapes, Rice, Wheat", "═")
    test1_passed = test_compare_crops(
        crops=["Grapes", "Rice", "Wheat"],
        district="Nanded",
        soil_type="Black",
        weather="Moderate Rainfall"
    )
    
    # Test Case 2: Western Maharashtra - High value crops
    print_header("TEST CASE 2: Sangli District - Grapes, Sugarcane, Pomegranate", "═")
    test2_passed = test_compare_crops(
        crops=["Grapes", "Sugarcane", "Pomegranate"],
        district="Sangli",
        soil_type="Black",
        weather="Moderate Rainfall"
    )
    
    # Test Case 3: Vidarbha - Cotton belt
    print_header("TEST CASE 3: Amravati District - Cotton, Soybean, Pigeon Pea", "═")
    test3_passed = test_compare_crops(
        crops=["Cotton", "Soybean", "Pigeon Pea"],
        district="Amravati",
        soil_type="Black",
        weather="Low Rainfall"
    )
    
    # Final Summary
    print_header("TEST SUITE SUMMARY", "═")
    results = [
        ("Test 1 - Nanded (Grapes, Rice, Wheat)", test1_passed),
        ("Test 2 - Sangli (Grapes, Sugarcane, Pomegranate)", test2_passed),
        ("Test 3 - Amravati (Cotton, Soybean, Pigeon Pea)", test3_passed)
    ]
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {status}: {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print_header("ALL TESTS PASSED! 🎉", "═")
    else:
        print_header("SOME TESTS FAILED ⚠️", "═")
    
    return all_passed

if __name__ == '__main__':
    """Run the test suite"""
    run_test_suite()
