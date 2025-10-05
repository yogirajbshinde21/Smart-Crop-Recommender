"""
Quick test to verify confidence scores are realistic (not 100%/0%)
"""

import requests
import json

API_URL = "http://localhost:5000"

print("="*80)
print("TESTING REALISTIC CONFIDENCE SCORES")
print("="*80)

test_cases = [
    {
        "name": "Yavatmal (Vidarbha) - Should show multiple crops with realistic confidence",
        "data": {
            "District": "Yavatmal",
            "Soil_Type": "Black",
            "Weather": "Monsoon"
        },
        "expected": "Cotton 60-70%, Soybean 25-35%, Others 5-15%"
    },
    {
        "name": "Raigad (Konkan) - Coastal crops only",
        "data": {
            "District": "Raigad",
            "Soil_Type": "Laterite",
            "Weather": "Monsoon"
        },
        "expected": "Rice 65-75%, Coconut 20-30%, Mango 5-15%"
    },
    {
        "name": "Latur (Marathwada) - Drought resistant crops",
        "data": {
            "District": "Latur",
            "Soil_Type": "Black",
            "Weather": "Semi-Arid"
        },
        "expected": "Sorghum 60-70%, Cotton 20-30%, Chickpea 5-15%"
    },
    {
        "name": "Nashik (North Maharashtra) - Grape belt",
        "data": {
            "District": "Nashik",
            "Soil_Type": "Black",
            "Weather": "Moderate Rainfall"
        },
        "expected": "Grapes 50-65%, Onion 25-35%, Others 5-15%"
    }
]

print("\nStarting tests...\n")

for i, test in enumerate(test_cases, 1):
    print(f"{'='*80}")
    print(f"TEST {i}: {test['name']}")
    print(f"{'='*80}")
    print(f"Input: {test['data']['District']} + {test['data']['Soil_Type']} + {test['data']['Weather']}")
    print(f"Expected: {test['expected']}")
    
    try:
        response = requests.post(f"{API_URL}/recommend-crop", json=test['data'], timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                crops = result['data']['recommendations']
                
                print(f"\n✅ SUCCESS - Got {len(crops)} crop recommendations:")
                
                # Check for extremes
                has_extreme = False
                for crop in crops:
                    confidence = crop['confidence']
                    status = ""
                    
                    if confidence >= 99:
                        status = " ⚠️ TOO HIGH (99%+)"
                        has_extreme = True
                    elif confidence <= 1:
                        status = " ⚠️ TOO LOW (0-1%)"
                        has_extreme = True
                    elif 40 <= confidence <= 80:
                        status = " ✓ REALISTIC"
                    else:
                        status = " → OK"
                    
                    print(f"  {crop['crop_name']:20s}: {confidence:5.2f}%{status}")
                
                if has_extreme:
                    print(f"\n❌ EXTREME CONFIDENCE DETECTED!")
                    print(f"   Issue still exists - review dataset/model")
                else:
                    print(f"\n✓ All confidence scores are realistic (not 100% or 0%)")
                
            else:
                print(f"✗ API Error: {result.get('error')}")
        
        else:
            print(f"✗ HTTP Error: {response.status_code}")
            print(f"  Response: {response.text[:200]}")
    
    except requests.exceptions.ConnectionError:
        print(f"✗ CONNECTION ERROR: API server not running")
        print(f"  Start server with: python app.py")
        break
    
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    print()

print("="*80)
print("TEST COMPLETE")
print("="*80)
print("\nIf you see 99%+ or 0-1% confidence:")
print("  1. Check config.py uses: maharashtra_agricultural_dataset_realistic.csv")
print("  2. Retrain: python train_models_research.py")
print("  3. Restart API: python app.py")
print("\nExpected confidence ranges:")
print("  Primary crop:   50-75%")
print("  Secondary crop: 20-40%")
print("  Tertiary crop:  5-15%")
print("="*80)
