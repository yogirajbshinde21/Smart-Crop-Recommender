"""Test API endpoints to see detailed errors"""
import requests
import json

# Test recommend-crop endpoint
print("Testing /recommend-crop endpoint...")
response = requests.post('http://localhost:5000/recommend-crop', json={
    'District': 'Mumbai City',
    'Soil_Type': 'Black',
    'Weather': 'Warm'
})

print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

print("\n" + "="*70 + "\n")

# Test compare-crops endpoint
print("Testing /compare-crops endpoint...")
response = requests.post('http://localhost:5000/compare-crops', json={
    'crops': ['Chickpea', 'Chili', 'Mango'],
    'District': 'Raigad',
    'Soil_Type': 'Black',
    'Weather': 'Warm'
})

print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
