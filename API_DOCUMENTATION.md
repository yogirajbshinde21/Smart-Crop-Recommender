# 📡 Smart Farmer API Documentation

## Base URL
```
http://localhost:5000
```

## Authentication
Currently, no authentication is required. All endpoints are publicly accessible.

---

## 🔍 GET Endpoints

### 1. Health Check
Check if the API is running and models are loaded.

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "message": "Smart Farmer API is running",
  "models_loaded": true
}
```

---

### 2. Get Dropdown Data
Retrieve all available options for dropdowns (districts, soil types, crops, weather conditions).

**Endpoint**: `GET /dropdown-data`

**Response**:
```json
{
  "success": true,
  "data": {
    "districts": ["Pune", "Nagpur", "Mumbai City", ...],
    "soil_types": ["Black", "Clay", "Red", "Laterite", ...],
    "crops": ["Cotton", "Soybean", "Rice", "Wheat", ...],
    "weather_conditions": ["Monsoon", "Post-Monsoon", "Winter", ...],
    "fertilizers": ["DAP", "Urea", "NPK 10-26-26", ...],
    "zones": ["Konkan", "Vidarbha", "Marathwada", ...]
  }
}
```

---

### 3. Get System Statistics
Retrieve overall system statistics.

**Endpoint**: `GET /statistics`

**Response**:
```json
{
  "success": true,
  "data": {
    "total_records": 1800,
    "total_districts": 36,
    "total_crops": 19,
    "total_soil_types": 7,
    "total_weather_conditions": 10,
    "zones": 5,
    "districts_by_zone": {
      "Konkan": 6,
      "Vidarbha": 11,
      "Marathwada": 8,
      "Western Maharashtra": 5,
      "North Maharashtra": 5
    }
  }
}
```

---

### 4. Get District Insights
Retrieve comprehensive insights for a specific district.

**Endpoint**: `GET /district-insights/<district_name>`

**Example**: `GET /district-insights/Pune`

**Response**:
```json
{
  "success": true,
  "data": {
    "district": "Pune",
    "zone": "Western Maharashtra",
    "zone_characteristics": {
      "climate": "Moderate to semi-arid",
      "major_crops": ["Sugarcane", "Grapes", "Pomegranate", "Wheat"],
      "soil_types": ["Black", "Red", "Alluvial"],
      "rainfall": "Moderate (600-1200mm)",
      "irrigation": "Canal irrigation available"
    },
    "soil_distribution": {
      "Black": 25,
      "Red": 15,
      "Alluvial": 10
    },
    "popular_crops": {
      "Sugarcane": 12,
      "Wheat": 10,
      "Cotton": 8,
      "Soybean": 7
    },
    "weather_patterns": {
      "Monsoon": 15,
      "Post-Monsoon": 12,
      "Winter": 10
    },
    "average_nutrients": {
      "N_kg_ha": 125.5,
      "P2O5_kg_ha": 65.3,
      "K2O_kg_ha": 75.8,
      "Zn_kg_ha": 8.2,
      "S_kg_ha": 25.4
    },
    "water_quality": {
      "avg_pH": 7.2,
      "avg_turbidity": 8.5,
      "avg_temp": 28.3
    },
    "total_records": 50
  }
}
```

---

## 📮 POST Endpoints

### 1. Crop Recommendation
Get top 3 crop recommendations based on district, soil type, and weather.

**Endpoint**: `POST /recommend-crop`

**Request Body**:
```json
{
  "District": "Pune",
  "Soil_Type": "Black",
  "Weather": "Post-Monsoon"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "recommendations": [
      {
        "crop_name": "Wheat",
        "confidence": 85.23,
        "avg_yield": 35,
        "market_rate": 2500,
        "suitable_for_zone": "Western Maharashtra"
      },
      {
        "crop_name": "Chickpea",
        "confidence": 72.15,
        "avg_yield": 20,
        "market_rate": 5500,
        "suitable_for_zone": "Western Maharashtra"
      },
      {
        "crop_name": "Sorghum",
        "confidence": 65.88,
        "avg_yield": 30,
        "market_rate": 3000,
        "suitable_for_zone": "Western Maharashtra"
      }
    ],
    "zone": "Western Maharashtra",
    "zone_info": {
      "climate": "Moderate to semi-arid",
      "major_crops": ["Sugarcane", "Grapes", "Pomegranate", "Wheat"],
      "soil_types": ["Black", "Red", "Alluvial"],
      "rainfall": "Moderate (600-1200mm)",
      "irrigation": "Canal irrigation available"
    },
    "input": {
      "district": "Pune",
      "soil_type": "Black",
      "weather": "Post-Monsoon"
    }
  }
}
```

---

### 2. Nutrient Prediction
Predict precise NPK and micronutrient requirements.

**Endpoint**: `POST /predict-nutrients`

**Request Body**:
```json
{
  "District": "Nashik",
  "Soil_Type": "Red",
  "Crop_Name": "Grapes",
  "Weather": "Winter"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "nutrients": {
      "N_kg_ha": 145.25,
      "P2O5_kg_ha": 85.50,
      "K2O_kg_ha": 95.75,
      "Zn_kg_ha": 12.30,
      "S_kg_ha": 35.20
    },
    "npk_ratio": {
      "N": 44.5,
      "P": 26.2,
      "K": 29.3
    },
    "alerts": [
      {
        "type": "info",
        "nutrient": "Zinc",
        "message": "Good zinc levels for grape cultivation."
      }
    ],
    "input": {
      "district": "Nashik",
      "soil_type": "Red",
      "crop_name": "Grapes",
      "weather": "Winter",
      "zone": "North Maharashtra"
    }
  }
}
```

---

### 3. Water Quality Analysis
Analyze water quality parameters for irrigation.

**Endpoint**: `POST /water-quality-analysis`

**Request Body**:
```json
{
  "District": "Mumbai City",
  "Weather": "Monsoon",
  "Soil_Type": "Laterite"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "water_parameters": {
      "recommended_pH": 6.8,
      "turbidity_NTU": 12.5,
      "water_temp_C": 27.3
    },
    "analysis": {
      "pH": {
        "status": "Neutral",
        "advice": "pH level is optimal for most crops."
      },
      "turbidity": {
        "status": "Moderate",
        "advice": "Consider filtration or sedimentation for sensitive crops."
      },
      "temperature": {
        "status": "Optimal",
        "advice": "Water temperature suitable for irrigation."
      }
    },
    "input": {
      "district": "Mumbai City",
      "weather": "Monsoon",
      "soil_type": "Laterite",
      "zone": "Konkan"
    }
  }
}
```

---

### 4. Fertilizer Recommendation
Get optimal fertilizer recommendations.

**Endpoint**: `POST /fertilizer-recommendation`

**Request Body**:
```json
{
  "Crop_Name": "Cotton",
  "Soil_Type": "Black",
  "N_kg_ha": 120,
  "P2O5_kg_ha": 60,
  "K2O_kg_ha": 70
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "recommendations": [
      {
        "fertilizer": "DAP",
        "confidence": 78.45,
        "cost_per_hectare": 1400,
        "is_primary": true
      },
      {
        "fertilizer": "NPK 12-32-16",
        "confidence": 65.20,
        "cost_per_hectare": 1300,
        "is_primary": false
      },
      {
        "fertilizer": "Urea",
        "confidence": 55.80,
        "cost_per_hectare": 800,
        "is_primary": false
      }
    ],
    "input": {
      "crop_name": "Cotton",
      "soil_type": "Black",
      "nutrients": {
        "N": 120,
        "P": 60,
        "K": 70
      }
    }
  }
}
```

---

### 5. Crop Comparison
Compare multiple crops side-by-side.

**Endpoint**: `POST /compare-crops`

**Request Body**:
```json
{
  "crops": ["Cotton", "Soybean", "Wheat"],
  "District": "Nagpur",
  "Soil_Type": "Black",
  "Weather": "Monsoon"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "comparison": [
      {
        "crop_name": "Cotton",
        "nutrients": {
          "N": 130.5,
          "P": 65.2,
          "K": 75.8,
          "Zn": 8.5,
          "S": 28.3
        },
        "economics": {
          "total_cost": 32400,
          "expected_yield": 18,
          "market_rate": 6500,
          "gross_income": 117000,
          "net_income": 84600,
          "roi_percentage": 261.11
        },
        "risk_assessment": {
          "risk_level": "Low",
          "water_requirement": "Medium",
          "zone_suitability": "Vidarbha"
        }
      },
      {
        "crop_name": "Soybean",
        "nutrients": {
          "N": 95.3,
          "P": 55.8,
          "K": 60.2,
          "Zn": 6.5,
          "S": 22.1
        },
        "economics": {
          "total_cost": 30400,
          "expected_yield": 25,
          "market_rate": 4200,
          "gross_income": 105000,
          "net_income": 74600,
          "roi_percentage": 245.39
        },
        "risk_assessment": {
          "risk_level": "Low",
          "water_requirement": "Medium",
          "zone_suitability": "Vidarbha"
        }
      },
      {
        "crop_name": "Wheat",
        "nutrients": {
          "N": 125.0,
          "P": 60.0,
          "K": 70.0,
          "Zn": 7.0,
          "S": 25.0
        },
        "economics": {
          "total_cost": 29400,
          "expected_yield": 35,
          "market_rate": 2500,
          "gross_income": 87500,
          "net_income": 58100,
          "roi_percentage": 197.62
        },
        "risk_assessment": {
          "risk_level": "Medium",
          "water_requirement": "Medium",
          "zone_suitability": "Vidarbha"
        }
      }
    ],
    "recommendation": {
      "best_crop": "Cotton",
      "reason": "Highest ROI of 261.11%",
      "roi": 261.11
    },
    "input": {
      "district": "Nagpur",
      "soil_type": "Black",
      "weather": "Monsoon",
      "zone": "Vidarbha"
    }
  }
}
```

---

## ❌ Error Responses

All endpoints return errors in this format:

```json
{
  "success": false,
  "error": "Error message here",
  "traceback": "Detailed traceback (in debug mode)"
}
```

**Common HTTP Status Codes**:
- `200` - Success
- `400` - Bad Request (missing or invalid parameters)
- `404` - Not Found (district not found)
- `500` - Internal Server Error

---

## 📊 Data Models

### Districts (36 total)
Pune, Nagpur, Mumbai City, Mumbai Suburban, Thane, Raigad, Ratnagiri, Sindhudurg, Nashik, Dhule, Jalgaon, Nandurbar, Ahmednagar, Aurangabad, Jalna, Parbhani, Hingoli, Nanded, Latur, Osmanabad, Beed, Wardha, Chandrapur, Gadchiroli, Gondia, Bhandara, Amravati, Akola, Yavatmal, Buldhana, Washim, Satara, Sangli, Kolhapur, Solapur

### Soil Types (7)
Black, Clay, Red, Laterite, Alluvial, Sandy, Loamy

### Crops (19)
Cotton, Soybean, Rice, Wheat, Sugarcane, Sorghum, Pearl Millet, Maize, Chickpea, Pigeon Pea, Green Gram, Black Gram, Groundnut, Sunflower, Grapes, Pomegranate, Banana, Mango, Coconut

### Weather Conditions (10)
Monsoon, Post-Monsoon, Winter, Summer, Semi-Arid, Coastal Humid, Tropical, Moderate, Dry, Humid

### Fertilizers (10)
DAP, Urea, NPK 10-26-26, NPK 12-32-16, NPK 20-20-20, NPK 19-19-19, Organic Compost, Vermicompost, Bio-Fertilizer, Liquid Fertilizer

---

## 🧪 Testing with cURL

### Test Health Check
```bash
curl http://localhost:5000/health
```

### Test Crop Recommendation
```bash
curl -X POST http://localhost:5000/recommend-crop \
  -H "Content-Type: application/json" \
  -d '{"District":"Pune","Soil_Type":"Black","Weather":"Post-Monsoon"}'
```

### Test Nutrient Prediction
```bash
curl -X POST http://localhost:5000/predict-nutrients \
  -H "Content-Type: application/json" \
  -d '{"District":"Nashik","Soil_Type":"Red","Crop_Name":"Grapes","Weather":"Winter"}'
```

---

## 📝 Notes

- All POST endpoints require `Content-Type: application/json` header
- Numeric values are returned as floats rounded to 2 decimal places
- Confidence scores are percentages (0-100)
- Economic values are in Indian Rupees (₹)
- Nutrient values are in kg/ha (kilograms per hectare)
- Water temperature is in Celsius
- pH values range from 5.0 to 8.5
- Turbidity is measured in NTU (Nephelometric Turbidity Units)

---

## 🔄 API Versioning

Current Version: **v1.0**

Future versions may include:
- Authentication endpoints
- User management
- Historical data tracking
- Real-time weather integration
- Mobile-specific endpoints

---

Built with Flask and Machine Learning 🚀
